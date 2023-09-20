from django.shortcuts import render
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
class LumberCreate(CreateView):
    template_name = "inventory/lumber_create.html"
    model = Lumber
    form_class = LumberForm
class LumberUpdate(UpdateView):
    template_name = "inventory/lumber_update.html"
    model = Lumber
    form_class = LumberForm
class LumberDelete(DeleteView):
    template_name = "inventory/lumber_delete.html"
    model = Lumber
    form_class = LumberForm

#Views for CRUD operations of the lengths
class LengthCreate(CreateView):
    template_name = "inventory/length_create.html"
    model = Length
    form_class = LengthForm
class LengthUpdate(UpdateView):
    template_name = "inventory/length_update.html"
    model = Length
    form_class = LengthForm
class LengthDelete(DeleteView):
    template_name = "inventory/length_delete.html"
    model = Length
    form_class = LengthForm