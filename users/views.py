
# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from django.contrib import messages

# Function to execute raw SQL queries
def execute_query(query, params=()):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()

# Signup view
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if user already exists
        existing_user = execute_query("SELECT * FROM users WHERE username = %s", [username])
        if existing_user:
            messages.error(request, "Username already exists!")
            return redirect('signup')

        # Insert the new user into the database
        execute_query("INSERT INTO users (username, password) VALUES (%s, %s)", [username, password])
        messages.success(request, "Account created successfully!")
        return redirect('login')

    return render(request, 'signup.html')

# Login view
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if the user exists in the database
        user = execute_query("SELECT * FROM users WHERE username = %s AND password = %s", [username, password])
        if user:
            request.session['username'] = username
            return redirect('welcome')
        else:
            messages.error(request, "Invalid login credentials!")
            return redirect('login')

    return render(request, 'login.html')

# Welcome view
def welcome(request):
    username = request.session.get('username')
    if username:
        return HttpResponse(f"Welcome to {username}")
    else:
        return redirect('login')
