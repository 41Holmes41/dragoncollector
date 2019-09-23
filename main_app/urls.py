from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('dragons/', views.dragons_index, name='index'),
  path('dragons/<int:dragon_id>', views.dragons_detail, name='detail'),
  path('dragons/create/', views.DragonCreate.as_view(), name="dragons_create"),
  path('dragons/<int:pk>/update', views.DragonUpdate.as_view(), name="dragons_update"),
  path('dragons/<int:pk>/delete', views.DragonDelete.as_view(), name="dragons_delete"),
  path('dragons/<int:dragon_id>/add_burning/', views.add_burning, name='add_burning'),
  path('dragons/<int:dragon_id>/assoc_toy/<int:toy_id>/', views.assoc_toy, name='assoc_toy'),
  path('dragons/<int:dragon_id>/add_photo/', views.add_photo, name='add_photo'),
  path('toys/', views.ToyList.as_view(), name='toys_index'),
  path('toys/<int:pk>/', views.ToyDetail.as_view(), name='toys_detail'),
  path('toys/create/', views.ToyCreate.as_view(), name='toys_create'),
  path('toys/<int:pk>/update/', views.ToyUpdate.as_view(), name='toys_update'),
  path('toys/<int:pk>/delete/', views.ToyDelete.as_view(), name='toys_delete'),
  path('accounts/signup', views.signup, name='signup'),
]