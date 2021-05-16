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
import numpy as np
import math
import json


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

def sel(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/sel.html',
        {
            'title':'Sistema de Ecuaciones Lineales',
            'message':'Your contact page.',
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


# METODOS NUMERICOS RAICES
def biseccion(request):
    msg=""
    cnv=1
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
    try:
        Es = (0.5*(10**(2-n)))
        #expr = expr.replace("ln","math.log")
        expr = parse_expr(expr)
    
        Fxi = round(expr.subs(a,Xi),n)#expr.subs(a,Xi)
        Fxu = round(expr.subs(a,Xu),n)

        if Fxi > 0 < Fxu or Fxu < 0 > Fxi:
            msg = ("<p>Segun el teorema de bolzano, existe una raiz si la funcion evaluada tanto en Xi como Xu tienen signo diferente.</p><p>F(Xi)="+str(Fxi)+"</p><p>F(Xu)="+str(Fxu)+"</p>"+
            "<p>Pruebe otro intervalo o cambie la funcion.</p>")
            cnv = 0
        elif Xi > Xu :
            msg = "Xi no puede ser mayor que Xu."
            cnv = 0
        elif n < 2:
            msg = "Cambie el valor de n, recomendamos que sea minimo 2."
            cnv = 0
        if cnv == 1:
            while Ea > Es:
                Xr_old = Xr
                Xu_old = Xu
                Xi_old = Xi
                try:
                    Xr = float((Xi+Xu)/2)
                    if math.isnan(Xr):
                        Ea=0
                except ZeroDivisionError:
                     Xr = 0
                try:
                    Fxi = expr.subs(a,Xi)
                    if math.isnan(Fxi):
                        Fxi=0
                except ZeroDivisionError:
                    Fxi = 0
                try:
                    Fxu = expr.subs(a,Xr)
                    if math.isnan(Fxu):
                            Fxu=0
                except ZeroDivisionError:
                    Fxu = 0
                prodF = Fxi*Fxu
                if prodF < 0:
                    Xi = Xi
                    Xu = Xr  
                elif prodF > 0:
                    Xi = Xr
                    Xu = Xu        
                if i >= 1:
                    try:
                        Ea = abs((Xr_old-Xr)/Xr_old)*100
                        if math.isnan(Ea):
                            Ea=0
                    except ZeroDivisionError:
                        Ea = 0
                i=i+1  
                data.append([str(i),str(Xi_old),str(Xu_old),str(Xr),str(Fxi),str(Fxu),str(prodF),str(Ea)])
                if i == 100:
                    msg = "Se ha detectado divergencia con los valores ingresados. Puede probar otro metodo."
                    return JsonResponse({'msg':msg,'code':1})
                    break
            root = Xr
            f = latex(expr)
            #data = request.POST.get("f")
            return JsonResponse({'result':[{'root':root,'Es':Es,'f':f}],'rows':data,'code':0})
        else:
            return JsonResponse({'msg':msg,'code':1})
    except Exception as e:
        msg = ("<p>Se ha detectado una indeterminacion con los valores ingresados. Puede probar otro metodo u otro intervalo.</p>"+
               "<p>"+str(e)+"</p>"
               )
        return JsonResponse({'msg':msg,'code':1})

def regla_falsa(request):
    msg=""
    cnv=1
    a= symbols('x')
    Xi = float(request.POST.get('Xi'))
    Xu = float(request.POST.get('Xu'))
    expr = request.POST.get('f')
    #fx = lambda x: request.POST.get('f')
    n = int(request.POST.get('n'))
    i = 0
    tabla = []
    try:
        Es = (0.5*(10**(2-n)))
        expr = parse_expr(expr)
        tramo = abs(Xu-Xi)
        #Fxi = expr.subs(a,Xi)
        fa = expr.subs(a,Xi)
        fb = expr.subs(a,Xu)
        if fa > 0 < fb or fb < 0 > fa:
            msg = ("<p>Segun el teorema de bolzano, existe una raiz si la funcion evaluada tanto en Xi como Xu tienen signo diferente.</p><p>F(Xi)="+str(fa)+"</p><p>F(Xu)="+str(fb)+"</p>"+
                   "<p>Pruebe otro intervalo o cambie la funcion.</p>")
            cnv = 0
        elif n < 2:
            msg = "Cambie el valor de n, recomendamos que sea minimo 2."
            cnv = 0
        if Xi > Xu :
            msg = "Xi no puede ser mayor que Xu."
            cnv = 0
        if cnv == 1:
            while not(tramo<=Es):    
                i = i+1
                try:
                    c = float(Xu-fb*(Xi-Xu)/(fa-fb))
                    if math.isnan(c):
                        c=0
                except ZeroDivisionError:
                    c == 0
                try:
                    fc = expr.subs(a,c)
                    if math.isnan(fc):
                        fc=0
                except ZeroDivisionError:
                    c == 0
                tabla.append([str(i),str(Xi),str(Xu),str(fa),str(fb),str(c),str(fc),str(tramo)])
                cambio = np.sign(fa)*np.sign(fc)
                if cambio>0:
                    tramo = abs(c-Xi)
                    Xi = c
                    fa = fc
                else:
                    tramo = abs(Xu-c)
                    Xu = c
                    fb = fc
                if i == 100:
                    msg = "Se ha detectado divergencia con los valores ingresados. Puede probar otro metodo."
                    return JsonResponse({'msg':msg,'code':1})
                    break
            root = c
            f = latex(expr)
            return JsonResponse({'result':[{'root':root,'Es':Es,'f':f}],'rows':tabla,'code':0})
        else:
            return JsonResponse({'msg':msg,'code':1})
    except Exception as e:
        msg = ("<p>Se ha detectado una indeterminacion con los valores ingresados. Puede probar otro metodo u otro intervalo.</p>"+
               "<p>"+str(e)+"</p>"
               )
        return JsonResponse({'msg':msg,'code':1})

def rapshon_newton(request):
    msg=""
    cnv=1
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
    try:
        Es = (0.5*(10**(2-n)))
        expr = parse_expr(expr)
        expr_diff = diff(expr,a)
    
        if n < 2:
            msg = "Cambie el valor de n, recomendamos que sea minimo 2."
            cnv = 0
        if cnv == 1:
            while Ea > Es:
                Xi_old = Xi
                try:
                    Fxi = expr.subs(a,Xi)
                    if math.isnan(Fxi):
                        Fxi=0
                except ZeroDivisionError:
                    Fxi = 0
                try:
                    Fprim_xi = expr_diff.subs(a,Xi)
                    if math.isnan(Fprim_xi):
                        Fprim_xi=0
                except ZeroDivisionError:
                    Fprim_xi = 0

                try:
                    Xi_nxt = Xi-(Fxi/Fprim_xi)
                    if math.isnan(Xi_nxt):
                        Xi_nxt=0
                except ZeroDivisionError:
                    Xi_nxt = 0
                   
                if i >= 1:
                    try:
                        Ea = abs(((Xi_nxt-Xi)/Xi_nxt))*100
                        if math.isnan(Ea):
                            Ea=0
                    except ZeroDivisionError:
                        Ea = 0
                Xi = Xi_nxt
                i=i+1  
                data.append([str(i),str(Xi_old),str(Fxi),str(Fprim_xi),str(Xi_nxt),str(Ea)])
                if i == 100:
                    msg = "Se ha detectado divergencia con los valores ingresados. Puede probar otro metodo."
                    return JsonResponse({'msg':msg,'code':1})
                    break
            root = Xi_nxt
            f = latex(expr)
            expr_diff = latex(expr_diff)
            return JsonResponse({'result':[{'root':str(root),'Es':str(Es),"f":f,"fprim":str(expr_diff)}],'rows':data})
        else:
            return JsonResponse({'msg':msg,'code':1})
    except Exception as e:
        msg = ("<p>Se ha detectado una indeterminacion con los valores ingresados. Puede probar otro valor.</p>"+
               "<p>"+str(e)+"</p>"
               )
        return JsonResponse({'msg':msg,'code':1})

def secante(request):
    msg=""
    cnv=1
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
    try:
        Es = (0.5*(10**(2-n)))
        expr = parse_expr(expr)
    
        if n < 2:
            msg = "Cambie el valor de n, recomendamos que sea minimo 2."
            cnv = 0
        if cnv == 1:
            while Ea > Es:
                if i < 1:
                    Xi_ant = Xi-1
                elif i > 0 :
                    Xi_ant = Xi_old
                Xi_old = Xi
                Xi_nxt_old = Xi_nxt
                try:
                    Fxi = expr.subs(a,Xi)
                    if math.isnan(Fxi):
                        Fxi=0
                except ZeroDivisionError:
                    Fxi = 0
                try: 
                    Fxi_ant = expr.subs(a,Xi_ant)
                    if math.isnan(Fxi_ant):
                        Fxi_ant=0
                except ZeroDivisionError:
                    Fxi_ant = 0
                try:
                    Xi_nxt = Xi-((Fxi*(Xi_ant-Xi))/(Fxi_ant-Fxi))
                    if math.isnan(Xi_nxt):
                        Xi_nxt=0
                except ZeroDivisionError:
                    Xi_ant = 0
                Xi = Xi_nxt
                if i >= 1:
                    try:
                        Ea = abs(((Xi_nxt_old-Xi_nxt)/Xi_nxt))*100
                        if math.isnan(Ea):
                            Ea=0
                    except ZeroDivisionError:
                        Ea = 0
                i=i+1  
                data.append([str(i),str(Xi_old),str(Xi_ant),str(Xi_nxt),str(Fxi),str(Fxi_ant),str(Ea)])
                if i == 100:
                    msg = "Se ha detectado divergencia con los valores ingresados. Puede probar otro metodo."
                    return JsonResponse({'msg':msg,'code':1})
                    break
            root = Xi_nxt
            f = latex(expr)
            return JsonResponse({'result':[{'root':str(root),'Es':str(Es),"f":f}],'rows':data})
        else:
            return JsonResponse({'msg':msg,'code':1})
    except Exception as e:
        msg = ("<p>Se ha detectado una indeterminacion con los valores ingresados. Puede probar otro valor.</p>"+
               "<p>"+str(e)+"</p>"
               )
        return JsonResponse({'msg':msg,'code':1})

def punto_fijo(request):
    msg=""
    cnv= 1
    Xi = float(request.POST.get('Xi'))
    expr = request.POST.get('f')
    expr2 = request.POST.get('g')
    n =  int(request.POST.get('n'))
    a= symbols("x")
    Ea = 100
    i = 0
    iteramax = 100
    respuesta = 0
    data = []
    expr = parse_expr(expr)
    expr2 = parse_expr(expr2)
    expr2_diff = diff(expr2,a)
    cnv_val = expr2_diff.subs(a,Xi)
    try:
        Es = (0.5*(10**(2-n)))
        try:
            b = expr2.subs(a,Xi)
            if math.isnan(b):
                b=0
        except ZeroDivisionError:
            b = 0
        tramo = abs(b-Xi)
        if cnv_val >= 1:
            msg = ("<p>Con los datos ingresados se detecta una divergencia.</p>"+
                   "<p>La derivada de g'(Xi) debe ser menor a 1 para determinar una solucion</p>"+
                   "<p>g'(Xi)="+str(cnv_val)+"</p>"+
                   "<p>Puede probar otro metodo</p>"
                  )
            cnv = 0
        if n < 2:
            msg = "Cambie el valor de n, recomendamos que sea minimo 2."
            cnv = 0
        if cnv == 1:
            while tramo>=Es :
                Xi = b
                try:
                    b = float(expr2.subs(a,Xi))
                    if math.isnan(b):
                        b=0
                except ZeroDivisionError:
                    b = 0
                tramo = abs((Xi-b)/b)*100
                i = i + 1
                data.append([str(i),str(b),str(tramo)])
                if (i==iteramax ):
                    msg = "Se ha detectado divergencia con los valores ingresados. Puede probar otro metodo."
                    return JsonResponse({'msg':msg,'code':1})
                    break
            respuesta = b
           

            root = respuesta
            f = latex(expr)
            g = latex(expr2)
            return JsonResponse({'result':[{'root':str(root),'Es':str(Es),"f":f,"g":g}],'rows':data})
        else:
             return JsonResponse({'msg':msg,'code':1})
    except Exception as e:
        msg = ("<p>Se ha detectado una indeterminacion con los valores ingresados. Puede probar otro valor.</p>"+
               "<p>"+str(e)+"</p>"
               )
        return JsonResponse({'msg':msg,'code':1})


# METODOS NUMERICOS SEL
def eliminacion_gauss(request):
    msg=""
    code = 0
    expr_i = ""  
    expr_a = ""
    expr_x = ""
    n = int(request.POST.get('n'))
    x = np.zeros(n)
    a = np.zeros((n,n+1))
    for i in range(n):
        a[i] = request.POST.getlist('x['+str(i)+'][]')

    a = a.astype(np.float)
    a, code = matrix_adjust(n,a)
    expr_i = matrix_latex(a,n)
    for i in range(n):            
        for j in range(i+1, n):
            try:
                ratio = a[j][i]/a[i][i]
            except ZeroDivisionError:
                ratio = 0         
            for k in range(n+1):
                a[j][k] = a[j][k] - ratio * a[i][k]

    # Back Substitution
    x[n-1] = a[n-1][n]/a[n-1][n-1]
    for i in range(n-2,-1,-1):
        x[i] = a[i][n]
        for j in range(i+1,n):     
            x[i] = x[i] - a[i][j]*x[j]

        x[i] = x[i]/a[i][i]
    if np.isnan(a).any():
        msg = "No hay solucion con el sistema de ecuaciones ingresado."
        return JsonResponse({'msg':msg,'code':1})

    expr_a = matrix_latex(a,n)
    expr_x = result_latex(x,n)
   
    #return JsonResponse({'result':[{'x':str(x),'a':str(a)}]})
    return JsonResponse({'result':[{'i':str(expr_i),'a':str(expr_a),'x':str(expr_x)}], 'code':code})

def gauss_jordan(request):
    msg=""
    code = 0
    expr_i = ""  
    expr_a = ""
    expr_x = ""
    n = int(request.POST.get('n'))
    x = np.zeros(n)
    a = np.zeros((n,n+1))
    for i in range(n):
        a[i] = request.POST.getlist('x['+str(i)+'][]')

    a = a.astype(np.float)
    a, code = matrix_adjust(n,a)
    expr_i = matrix_latex(a,n)
    for i in range(n):
        piv = a[i][i]
        for j in range(n+1):
            if a[i][j] == 0:
                a[i][j] = 0
            else:
                a[i][j] = a[i][j]/piv

        for k in range(n):
            if k != i:
                ration = a[k][i]

                for l in range(n+1):
                    a[k][l]=a[k][l]-a[i][l]*ration

    for i in range(n):
        x[i] = a[i][n]
    if np.isnan(a).any():
        msg = "No hay solucion con el sistema de ecuaciones ingresado."
        return JsonResponse({'msg':msg,'code':1})
    expr_a = matrix_latex(a,n)
    expr_x = result_latex(x,n)
    return JsonResponse({'result':[{'i':str(expr_i),'a':str(expr_a),'x':str(expr_x)}], 'code':code})

def matrix_adjust(n,a):
    code = 0
    for i in range(n):
        if a[i][i]==0:
            for j in range (n):
                if a[j][i] != 0:
                    a[[i,j]] = a[[j,i]]
            code = 2

    return a, code

def matrix_latex(a,n):
    txt=('\['+
        '\left['+
        '\\begin{'+'array}{')
    for i in range(n):
        txt= txt+'c'
    txt = txt+'|c}'
    for i in range(n):     
        for j in range(n+1):
            if j == n:
                txt = txt + str(a[i][j])
            else:
                txt = txt + str(a[i][j])+'&'

        txt = txt + r'\\' 
            
    txt = txt + ('\end{'+'array}'+
        '\\right]'+
        '\\]')
    return txt

def result_latex(x,n):
    txt =('\['+
        '\left\{\\begin{matrix}')
    for i in range(n):
        txt = txt + 'X_{'+str(i)+'} = '+ str(x[i]) 
        if i < n:
            txt = txt + r'\\'
    txt = txt + ('\end{'+'matrix}\\right.\]')
    return txt
