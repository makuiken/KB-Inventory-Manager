from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Lumber, Length
from .forms import LumberForm, LengthForm
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView 

#Home List of all objects
def home(request):
    lumber_list = Lumber.objects.all()
    context = {'lumber_list': lumber_list}
    return render(request, 'inventory/home.html', context)

#Views for CRUD operations of Lumber types
def add_lumber(request):
    if request.method == 'POST':
        form = LumberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = LumberForm()
    return render(request, 'inventory/lumber_create.html', {'form': form})

class LumberUpdate(UpdateView):
    template_name = "inventory/lumber_update.html"
    model = Lumber
    form_class = LumberForm
    success_url = reverse_lazy('home')

class LumberDelete(DeleteView):
    template_name = "inventory/lumber_delete.html"
    model = Lumber
    form_class = LumberForm
    success_url = reverse_lazy('home')

#Views for CRUD operations of the lengths
def add_length(request):
    if request.method == 'POST':
        form = LengthForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = LengthForm()
    return render(request, 'inventory/length_create.html', {'form': form})

class LengthUpdate(UpdateView):
    template_name = "inventory/length_update.html"
    model = Length
    form_class = LengthForm
    success_url = reverse_lazy('home')

class LengthDelete(DeleteView):
    template_name = "inventory/length_delete.html"
    model = Length
    form_class = LengthForm
    success_url = reverse_lazy('home')