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
    path('sel/', views.sel, name='sel'),
    
    # FUNCIONES RAICES
    path('biseccion/', views.biseccion, name='biseccion' ),
    path('regla_falsa/', views.regla_falsa, name='regla_falsa' ),
    path('rapshon_newton/', views.rapshon_newton, name='rapshon_newton' ),
    path('secante/', views.secante, name='secante' ),
    path('punto_fijo/', views.punto_fijo, name='punto_fijo' ),
    
    #FUNCIONES SEL
    path('sel/eliminacion_gauss/', views.eliminacion_gauss, name='eliminacion_gauss' ),
    path('sel/gauss_jordan/', views.gauss_jordan, name='gauss_jordan' ),
    path('sel/gauss_seidel/', views.gauss_seidel, name='gauss_seidel' ),
]
