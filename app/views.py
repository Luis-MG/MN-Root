"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse 
from django.http import JsonResponse
from django.http import QueryDict
from sympy import *



def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )


def biseccion(request):
    a= symbols('x')
    Xi = float(request.POST.get('Xi'))
    Xu = float(request.POST.get('Xu'))
    expr = request.POST.get('f')
    n = int(request.POST.get('n'))
    Xr = 0
    Ea = 100
    Et = 0
    Es = 0
    i = 0
    Fxi = 0
    Fxu = 0
    prodF = 0
    Xr_old = 0

    Es = (0.5*(10**(2-n)))
    #expr = expr.replace("ln","math.log")
    expr = parse_expr(expr)

    while Ea > Es:
        Xr_old = Xr
        Xu_old = Xu
        Xi_old = Xi
        Xr = float((Xi+Xu)/2)
        Fxi = expr.subs(a,Xi)
        Fxu = expr.subs(a,Xr)
        prodF = Fxi*Fxu
        if prodF < 0:
            Xi = Xi
            Xu = Xr  
        elif prodF > 0:
            Xi = Xr
            Xu = Xu        

        if i >= 1:
            Ea = abs((Xr_old-Xr)/Xr_old)*100
        i=i+1  
        data = Xr

    #data = request.POST.get("f")
    return JsonResponse({'data':data})

