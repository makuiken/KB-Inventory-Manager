from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('lumber/new', views.LumberCreate.as_view(), name='lumbercreate'),
    path('lumber/edit', views.LumberUpdate.as_view(), name='lumberupdate'),
    path('lumber/delete', views.LumberDelete.as_view(), name='lumberdelete'),
    path('lengths/new', views.LengthCreate.as_view(), name='lengthcreate'),
    path('lengths/edit', views.LengthCreate.as_view(), name='lengthcreate'),
    path('lengths/delete', views.LengthCreate.as_view(), name='lengthdelete'),

]