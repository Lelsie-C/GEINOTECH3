import json
import subprocess
from channels.generic.websocket import AsyncWebsocketConsumer

connected_users = set()  # Store connected user info

class CodeCollabConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Access session information from the scope
        self.username = self.scope["session"].get("username", "Guest")  # Get username from session

        # Add user to connected users
        connected_users.add(self.username)

        # Join WebSocket group
        self.room_group_name = "code_collab_room"
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
        # Remove user from connected users
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
            compile_process = subprocess.run(
                ["g++", "temp.cpp", "-o", "temp"],
                capture_output=True,
                text=True
            )
            
            # Check if compilation was successful
            if compile_process.returncode != 0:
                return f"Compilation Error:\n{compile_process.stderr}"
            
            # Execute the compiled C++ program
            run_process = subprocess.run(
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