from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view, name='home'),
    path('lumber/new', views.LumberCreate.as_view, name='lumbercreate'),
    path('lumber/edit', views.LumberUpdate.as_view, name='lumberupdate'),
    path('lumber/delete', views.LumberDelete.as_view, name='lumberdelete'),
    path('length/new', views.LengthCreate.as_view, name='lengthcreate'),
    path('length/edit', views.LengthCreate.as_view, name='lengthcreate'),
    path('length/delete', views.LengthCreate.as_view, name='lengthdelete'),

]