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
    data = []
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
        data.append([str(i),str(Xi_old),str(Xu_old),str(Xr),str(Fxi),str(Fxu),str(prodF),str(Ea)])
    root = Xr
    f = latex(expr)
    #data = request.POST.get("f")
    return JsonResponse({'result':[{'root':root,'Es':Es,'f':f}],'rows':data})

def rapshon_newton(request):
    a= symbols("x")
    Xi = float(request.POST.get('Xi'))
    expr = request.POST.get('f')
    n =  int(request.POST.get('n'))
    Ea = 100
    i = 0
    Xi_nxt = 0
    Fxi = 0
    Fprim_xi = 0
    data = []
    Es = (0.5*(10**(2-n)))
    expr = parse_expr(expr)
    expr_diff = diff(expr,a) 
    while Ea > Es:
        Xi_old = Xi
        Fxi = expr.subs(a,Xi)
        Fprim_xi = expr_diff.subs(a,Xi)
        Xi_nxt = Xi-(Fxi/Fprim_xi)
        Ea = abs(((Xi_nxt-Xi)/Xi_nxt))*100
        Xi = Xi_nxt
        i=i+1  
        data.append([str(i),str(Xi_old),str(Fxi),str(Fprim_xi),str(Xi_nxt),str(Ea)])
    root = Xi_nxt
    f = latex(expr)
    expr_diff = latex(expr_diff)
    return JsonResponse({'result':[{'root':str(root),'Es':str(Es),"f":f,"fprim":str(expr_diff)}],'rows':data})

def secante(request):
    Xi = float(request.POST.get('Xi'))
    expr = request.POST.get('f')
    n =  int(request.POST.get('n'))
    a= symbols("x")
    Xi_nxt = 0
    Xi_nxt_old = 0
    Xi_ant = 0
    Ea = 100
    i = 0
    Fxi = 0
    Fxi_ant = 0
    data = []
    Es = (0.5*(10**(2-n)))
    expr = parse_expr(expr)
    while Ea > Es:
        if i < 1:
            Xi_ant = Xi-1
        elif i > 0 :
            Xi_ant = Xi_old
        Xi_old = Xi
        Xi_nxt_old = Xi_nxt
        Fxi = expr.subs(a,Xi)
        Fxi_ant = expr.subs(a,Xi_ant)
        Xi_nxt = Xi-((Fxi*(Xi_ant-Xi))/(Fxi_ant-Fxi))
        Xi = Xi_nxt
        if i >= 1:
            Ea = abs(((Xi_nxt_old-Xi_nxt)/Xi_nxt))*100
        i=i+1  
        data.append([str(i),str(Xi_old),str(Xi_ant),str(Xi_nxt),str(Fxi),str(Fxi_ant),str(Ea)])
    root = Xi_nxt
    f = latex(expr)
    return JsonResponse({'result':[{'root':str(root),'Es':str(Es),"f":f}],'rows':data})