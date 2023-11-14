from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from .models import Lumber, Length, Invitation, Sale, ChangeLog
from .forms import LumberForm, LengthForm, QuantityForm, CustomUserCreationForm, LumberTypeFilterForm, SellForm, CutForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import FileResponse
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

#Home List of all objects
@login_required
def home(request):
    selected_type = request.GET.get('lumber_type', None)
    if selected_type:
        lumber_list = Lumber.objects.filter(lumber_type=selected_type)
    else:
        lumber_list = Lumber.objects.all()

    length_list = Length.objects.all()

    form = LumberTypeFilterForm()
    context = {'lumber_list': lumber_list, 'length_list': length_list, 'form': form}
    return render(request, 'inventory/home.html', context)

@login_required
def change_log(request):
    change_log_entries = ChangeLog.objects.all().order_by('-datetime')

    paginator = Paginator(change_log_entries, 25)  # Show 25 entries per page
    page = request.GET.get('page')
    entries = paginator.get_page(page)
    
    return render(request, 'inventory/change_log.html', {'entries': entries})

@login_required
def change_details(request, change_code):
    change_log_entry = get_object_or_404(ChangeLog, change_code=change_code)
    return render(request, 'inventory/change_details.html', {'change_log_entry': change_log_entry})

#Salesmen Pages
@login_required
def sell(request, ref_id, length):
    selected_length = get_object_or_404(Length, lumber__ref_id=ref_id, length=length)

    if request.method == 'POST':
        form = SellForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            if selected_length.quantity < quantity:
                raise ValueError("The selected length does not have enough quantity available.")

            sale = Sale(
                user=request.user,
                changetype='sale',
                product_id=selected_length.lumber,
                length=selected_length,
                quantity=quantity
            )
            sale.save()

            selected_length.quantity -= quantity
            selected_length.save()

            change_log = ChangeLog(
                sale_user=request.user,
                changetype='sale',
                description=f"{selected_length.lumber.ref_id}: Sold {quantity} - {selected_length.length}'"
            )

            change_log.save()

            return redirect('home')
    else:
        form = SellForm(initial={'quantity': selected_length.quantity})

    return render(request, 'inventory/sell_view.html', {'form': form, 'selected_length': selected_length})

@login_required
def cut(request, ref_id, length):
    selected_length = get_object_or_404(Length, lumber__ref_id=ref_id, length=length)

    if request.method == 'POST':
        form = CutForm(request.POST)
        if form.is_valid():
            desired_length = form.cleaned_data['desired_length']
            quantity = form.cleaned_data['quantity']

            sale = Sale(user=request.user)
            sale.cut_from(request.user, selected_length.lumber.ref_id, selected_length.length, desired_length, quantity)

            change_log = ChangeLog(
                sale_user=request.user,
                changetype='adjustment',
                description=f"{selected_length.lumber.ref_id}: Cut {quantity} - {selected_length.length}' to {desired_length}'"
            )
            change_log.save()

            return redirect('home')
    else:
        form = CutForm()

    return render(request, 'inventory/cut_view.html', {'form': form, 'selected_length': selected_length})

#Views for CRUD operations of Lumber types
@login_required
def add_lumber(request):
    if request.method == 'POST':
        form = LumberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = LumberForm()
    return render(request, 'inventory/lumber_create.html', {'form': form})

class LumberUpdate(LoginRequiredMixin, UpdateView):
    template_name = "inventory/lumber_update.html"
    model = Lumber
    form_class = LumberForm
    success_url = reverse_lazy('home')

class LumberDelete(LoginRequiredMixin, DeleteView):
    template_name = "inventory/lumber_delete.html"
    model = Lumber
    form_class = LumberForm
    success_url = reverse_lazy('home')

#Views for CRUD operations of the lengths
@login_required
def add_length(request):
    if request.method == 'POST':
        form = LengthForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = LengthForm()
    return render(request, 'inventory/length_create.html', {'form': form})

@login_required
def change_quantity(request, ref_id, length):
    length_instance = Length.objects.get(lumber__ref_id=ref_id, length=length)
    if request.method == 'POST':
        form = QuantityForm(request.POST, instance=length_instance)
        if form.is_valid():
            form.save()

            change_log = ChangeLog(
                length_user=request.user,
                changetype='adjustment',
                description=f" {length_instance.lumber.ref_id}- {length}': Changed Quantity to {length_instance.quantity} "
            )
            change_log.save()

            return redirect('home')
    else:
        form = QuantityForm(initial={'quantity': length_instance.quantity})
    return render(request, 'inventory/quantity_update.html', {'form': form})

class LengthUpdate(LoginRequiredMixin, UpdateView):
    template_name = "inventory/length_update.html"
    model = Length
    form_class = LengthForm
    success_url = reverse_lazy('home')

@login_required
def length_delete(request, ref_id, length):
    length_instance = get_object_or_404(Length, lumber__ref_id=ref_id, length=length)

    if request.method == 'POST':
        length_instance.delete()
        
        change_log = ChangeLog(
            length_user=request.user,
            changetype='adjustment',
            description=f"{length_instance.lumber.ref_id}: Deleted {length}"
        )
        change_log.save()

        return redirect('home')

    return render(request, 'inventory/length_delete.html', {'length': length_instance})

@login_required
def inventory_count(request):
    download = request.GET.get('download', False)
    selected_type = request.GET.get('lumber_type', None)
    if selected_type:
        lumber_list = Lumber.objects.filter(lumber_type=selected_type)
    else:
        lumber_list = Lumber.objects.all()

    length_list = Length.objects.all()

    form = LumberTypeFilterForm()
    context = {'lumber_list': lumber_list, 'length_list': length_list, 'form': form}
    if download:
        return render_to_pdf('inventory/inventory_count_table.html', context)
    return render(request, 'inventory/inventory_count.html', context)

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)

    if pdf.err:
        return HttpResponse("Invalid PDF", status_code=400, content_type='text/plain')
    return HttpResponse(result.getvalue(), content_type='application/pdf')

#User Registration and Login
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            invitation_code = form.cleaned_data['invitation_code']
            invitation = Invitation.objects.get(code=invitation_code)
            invitation.used = True
            invitation.save()
            login(request, user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'authenticator/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'authenticator/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')