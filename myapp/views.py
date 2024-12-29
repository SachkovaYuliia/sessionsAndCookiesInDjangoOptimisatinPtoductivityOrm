from django.shortcuts import render,redirect
from django.http import HttpResponse 

def login_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')

        response = redirect('greeting')
        response.set_cookie('name', name, max_age=60 * 15)  

        request.session['age'] = age
        return response

    return render(request, 'login.html')

def greeting_view(request):
    name = request.COOKIES.get('name')
    age = request.session.get('age')

    if not name or not age:
        return redirect('login')
    """Автоподовження cookies"""
    response = render(request, 'greeting.html', {'name': name, 'age': age})
    response.set_cookie('name', name, max_age=60 * 60 * 24 * 7) 
    return response

def logout_view(request):
    """Видаляємо cookies"""
    response = redirect('login')
    response.delete_cookie('name')
    
    """Видаляємо сесійні дані"""
    request.session.flush()
    return response
