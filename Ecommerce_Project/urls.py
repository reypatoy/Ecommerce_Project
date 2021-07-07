"""Ecommerce_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Ecommerce_App import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_login/', views.admin_login_view, name="admin_login"),
    path('admin_dashboard/', views.admin_dashboard_view, name="admin_dashboard"),
    path('admin_login_process/', views.admin_login_process,
         name="admin_login_process"),
    path('admin_logout_process/', views.admin_logout_process,
         name="admin_logout_process"),
    # Categories
    path('category_list/', views.categories_list_view.as_view(), name="category_list"),
    path('category_create/', views.category_create_view.as_view(),
         name="category_create"),
    path('category_update/<slug:pk>',
         views.category_update_view.as_view(), name="category_update"),
    # Subcategories
    path('sub_category_list/', views.sub_categories_list_view.as_view(),
         name="sub_category_list"),
    path('sub_category_create/', views.sub_category_create_view.as_view(),
         name="sub_category_create"),
    path('sub_category_update/<slug:pk>',
         views.sub_category_update_view.as_view(), name="sub_category_update"),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
