from django.db import connection
from django.shortcuts import render
from django.http import HttpResponse
from .models import UserProfile

# EJEMPLO DE APLICACIÓN VULNERABLE PARA TESTEAR DJANGO-SHIELD

def profile_view(request):
    # HALLAZGO 1: IDOR (MEASURE-2)
    # No verifica si el profile pertenece al request.user
    user_id = request.GET.get('id')
    profile = UserProfile.objects.get(id=user_id) 
    
    return render(request, 'profile.html', {'profile': profile})

def search_logs(request):
    # HALLAZGO 2: SQL Injection (MEASURE-2)
    # Uso de Raw Query con f-string (Taint Flow: GET -> cursor.execute)
    query = request.GET.get('q')
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM logs WHERE message LIKE '%{query}%'")
        row = cursor.fetchone()
    
    return HttpResponse(f"Resultado: {row}")

def dangerous_display(request):
    # HALLAZGO 3: XSS (MEASURE-2)
    # Uso de mark_safe con input de usuario
    from django.utils.safestring import mark_safe
    user_input = request.GET.get('name')
    safe_name = mark_safe(f"<h1>Hola, {user_input}</h1>")
    
    return render(request, 'hello.html', {'name': safe_name})
