import json
import subprocess
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

connected_users = set()  # Store connected user info

# real_real_time_app/consumers.py

class CodeCollabConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = "code_collab_room"  # Set the room group name here

    async def connect(self):
        # Check if the session exists and contains the username
        if "session" not in self.scope or not self.scope["session"].get("username"):
            await self.close(code=403)  # Reject the connection if not authenticated
            return

        # Get the username from the session
        self.username = self.scope["session"].get("username", "Guest")

        # Add user to connected users
        connected_users.add(self.username)

        # Join WebSocket group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Broadcast updated user list
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_update",
                "users": list(connected_users)
            }
        )

    async def disconnect(self, close_code):
        # Remove user from connected users if username is set
        if hasattr(self, "username") and self.username in connected_users:
            connected_users.discard(self.username)

            # Leave WebSocket group
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

            # Broadcast updated user list
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "user_update",
                    "users": list(connected_users)
                }
            )
    @database_sync_to_async
    def get_connected_users(self):
        # Get the list of connected users from the database or another source
        return list(connected_users)  # Replace with your logic

    @database_sync_to_async
    def get_session(self, session_key):
        # Import the Session model here to avoid AppRegistryNotReady
        from django.contrib.sessions.models import Session
        try:
            return Session.objects.get(session_key=session_key)
        except Session.DoesNotExist:
            # Handle the case where the session does not exist
            return None

    async def receive(self, text_data):
        data = json.loads(text_data)
        event_type = data.get("type")
        
        if event_type == "code_update":
            # Broadcast code update
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "code_update",
                    "code": data["code"]
                }
            )
        elif event_type == "run_code":
            # Execute C++ code and capture output
            code = data["code"]
            output = await self.execute_cpp_code(code)  # Execute the C++ code
            
            # Broadcast output update
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "output_update",
                    "output": output
                }
            )
        elif event_type == "send_message":
            # Broadcast message to all users
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "message_update",
                    "sender": self.username,  # Use the sender's name
                    "message": data["message"]
                }
            )
    
    async def execute_cpp_code(self, code):
        try:
            # Write the C++ code to a temporary file
            with open("temp.cpp", "w") as file:
                file.write(code)
            
            # Compile the C++ code
            compile_process = await sync_to_async(subprocess.run)(
                ["g++", "temp.cpp", "-o", "temp"],
                capture_output=True,
                text=True
            )
            
            # Check if compilation was successful
            if compile_process.returncode != 0:
                return f"Compilation Error:\n{compile_process.stderr}"
            
            # Execute the compiled C++ program
            run_process = await sync_to_async(subprocess.run)(
                ["./temp"],
                capture_output=True,
                text=True
            )
            
            # Return the output of the program
            return run_process.stdout
        except Exception as e:
            return f"Execution Error:\n{str(e)}"
    
    async def code_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "code_update",
            "code": event["code"]
        }))
    
    async def output_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "output_update",
            "output": event["output"]
        }))

    async def message_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "message_update",
            "sender": event["sender"],  # Use the sender's name
            "message": event["message"]
        }))
    
    async def user_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "user_update",
            "users": event["users"]
        }))