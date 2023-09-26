from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Lumber, Length, Invitation, Sale, ChangeLog
from .forms import LumberForm, LengthForm, QuantityForm, CustomUserCreationForm, LumberTypeFilterForm, SellForm, CutForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView 

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

#Salesmen Pages
@login_required
def sell(request, length_id, ref_id):
    selected_length = get_object_or_404(Length, id=length_id)

    if request.method == 'POST':
        form = SellForm(request.POST)
        if form.is_valid():
            selected_length = form.cleaned_data['length']

            sale = Sale(
                user=request.user,
                changetype='sale',
                product_id=selected_length.lumber,
                length=selected_length,
                quantity=1
            )
            sale.save()

            selected_length.quantity -= 1
            selected_length.save()

            return redirect('home')
    else:
        form = SellForm(initial={'length': selected_length})

    return render(request, 'inventory/sell_view.html', {'form': form})
@login_required
def cut(request, length_id, ref_id):
    selected_length = get_object_or_404(Length, id=length_id)
    product_id = selected_length.lumber

    if request.method == 'POST':
        form = CutForm(request.POST)
        if form.is_valid():
            desired_length = form.cleaned_data['desired_length']

            sale = Sale(user=request.user)
            sale.cut_from(request.user, product_id, selected_length.length, desired_length)

            return redirect('home')
    else:
        form = CutForm(initial={'length': selected_length})

    return render(request, 'cut.html', {'form': form})
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
            return redirect('home')
    else:
        form = QuantityForm()
    return render(request, 'inventory/quantity_update.html', {'form': form})

class LengthUpdate(LoginRequiredMixin, UpdateView):
    template_name = "inventory/length_update.html"
    model = Length
    form_class = LengthForm
    success_url = reverse_lazy('home')

class LengthDelete(LoginRequiredMixin, DeleteView):
    template_name = "inventory/length_delete.html"
    model = Length
    form_class = LengthForm
    success_url = reverse_lazy('home')

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