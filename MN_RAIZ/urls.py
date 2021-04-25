"""
Definition of urls for MN_RAIZ.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views


urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('biseccion/', views.biseccion, name='biseccion' ),
    path('regla_falsa/', views.regla_falsa, name='regla_falsa' ),
    path('rapshon_newton/', views.rapshon_newton, name='rapshon_newton' ),
    path('secante/', views.secante, name='secante' ),
    path('punto_fijo/', views.punto_fijo, name='punto_fijo' ),
]
