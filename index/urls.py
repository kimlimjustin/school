from django.urls import path
from . import views
urlpatterns = [
	path('', views.index, name="index"),
	path('dashboard', views.dashboard, name="dashboard"),
	path('logout', views.logout_view, name="logout"),
	path('dashboard/class/<str:classlevel>/<str:classname>', views.edit_class, name="edit_class"),
	path('class', views.class_view, name="class"),
	path('register', views.register, name="register"),
	path('blog', views.blog, name="blog"),
	path("edit", views.edit_blog, name="edit"),
	path('remove_teacher', views.remove_teacher, name="remove_teacher"),
	path("add_teacher", views.add_teacher, name="add_teacher"),
	path("add_stream", views.add_stream, name="add_stream"),
	path("assignment/<int:id>", views.see_assignment, name="assignment"),
	path("add_assignment", views.add_assignment, name="add_assignment"),
	path("delete", views.delete, name="delete")
]