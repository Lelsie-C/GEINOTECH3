from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib import messages


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        code = request.POST.get("code")
        
        # Check if the code is correct
        if code == "12500":  # Admin Code
            user = authenticate(request, username=username, password="admin_password")  # Use a secure password
            if user is not None:
                login(request, user)
                request.session["is_admin"] = True
                return redirect("main/")
        elif code == "15425":  # User Code
            user = authenticate(request, username=username, password="user_password")  # Use a secure password
            if user is not None:
                login(request, user)
                request.session["is_admin"] = False
                return redirect("main/")
        else:
            # Display custom error message for wrong password
            messages.error(request, "Wrong password, contact CHEGHE😎😎 for the password")
            return render(request, "real_real_time_app/login.html", {"error": "Wrong password, contact CHEGHE for the password"})
    
    return render(request, "real_real_time_app/login.html")

def main_page(request):
    if not request.user.is_authenticated:
        return redirect("/")
    return render(request, "real_real_time_app/main.html", {"is_admin": request.session.get("is_admin", False), "username": request.user.username})

@csrf_exempt
def websocket_connect(request):
    global connected_users
    username = request.session.get("username")
    if username:
        connected_users.add(username)
        send_user_list_update()
    return JsonResponse({"status": "connected", "users": list(connected_users)})

@csrf_exempt
def websocket_disconnect(request):
    global connected_users
    username = request.session.get("username")
    if username and username in connected_users:
        connected_users.remove(username)
        send_user_list_update()
    return JsonResponse({"status": "disconnected", "users": list(connected_users)})

def send_user_list_update():
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "code_collab_room",  # Use the same group name as in consumers.py
        {
            "type": "user_update",  # Match the type in consumers.py
            "users": list(connected_users)
        }
    )