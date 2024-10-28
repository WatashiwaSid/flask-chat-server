from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
socketio = SocketIO(app)

# This dictionary stores user objects who connect to the server
users = {}

@app.route("/")
def index():
    return render_template("index.html")

# Listening to the connect event
@socketio.on("connect")
def handleConnect():
    username = f"user{random.randint(11,1000)}"
    gender = random.choice(["girl", "boy"])
    # API gets random avatars based on gender. It takes girl or boy as argument.
    avatarUrl = f"https://avatar.iran.liara.run/public/{gender}?username={username}"
    users[request.sid] = {"username": username, "avatar": avatarUrl}

    # Emit the new user joined and the current online count
    emit("user_joined", {"username": username, "avatar": avatarUrl}, broadcast=True)
    emit("set_username", {"username": username})
    emit("update_online_count", {"count": len(users)}, broadcast=True)

# Listening to the disconnect event
@socketio.on("disconnect")
def handleDisconnect():
    # Return None if the user does not exist.
    user = users.pop(request.sid, None)
    if user:
        emit("user_left", {"username": user["username"]}, broadcast=True)
        emit("update_online_count", {"count": len(users)}, broadcast=True)

# Handle messages
@socketio.on("send_message")
def sendMessage(data):
    user = users.get(request.sid)
    if user:
        emit("new_message", 
            {"username": user["username"], 
             "avatar": user["avatar"], 
             "message": data["message"]
            }, broadcast=True)

# Handle username updates
@socketio.on("username_update")
def usernameUpdate(data):
    oldUsername = users[request.sid]["username"]
    newUsername = data["username"]
    
    # Update the username in the user dictionary
    users[request.sid]["username"] = newUsername
    
    emit("username_updated", 
         {"oldUsername": oldUsername, "newUsername": newUsername}, 
         broadcast=True)

if __name__ == "__main__":
    socketio.run(app) 