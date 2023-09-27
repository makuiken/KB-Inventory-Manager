from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('lumber/new', views.add_lumber, name='lumbercreate'),
    path('lumber/<str:pk>/edit', views.LumberUpdate.as_view(), name='lumberupdate'),
    path('lumber/<str:pk>/delete', views.LumberDelete.as_view(), name='lumberdelete'),
    path('lengths/new', views.add_length, name='lengthcreate'),
    path('lengths/<str:pk>/edit', views.LengthUpdate.as_view(), name='lengthupdate'),
    path('lengths/<str:ref_id>/<int:length>/delete', views.length_delete, name='lengthdelete'),
    path('lengths/<str:ref_id>/<int:length>/quantity/edit', views.change_quantity, name='changequantity'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('sell/<int:length_id>/<str:ref_id>/', views.sell, name='sell'),
    path('lengths/<str:ref_id>/<int:length>/cut', views.cut, name='cut'),
]