from django.urls import path
from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path("login", views.login_view, name="login"),
  path("logout", views.logout_view, name="logout"),
  path("register", views.register, name="register"),
  path("startedNew_stage", views.startedNew_stage, name="startedNew_stage"),
  path("proceedingNew_stage", views.proceedingNew_stage, name="proceedingNew_stage"),
  path("completedNew_stage", views.completedNew_stage, name="completedNew_stage"),
  path("cancelledNew_stage", views.cancelledNew_stage, name="cancelledNew_stage"),
  path("load_stage", views.load_stage, name="load_stage"),
  path("new_item_save", views.new_item_save, name="new_item_save"),
]