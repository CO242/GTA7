from ursina import *
import socket
import threading

app = Ursina()

# Networking
HOST = input("Enter server IP (or 127.0.0.1 for localhost): ")
PORT = 5050

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Players
player = Entity(model='cube', color=color.orange, scale=(1,2,1), position=(0,1,0), collider='box')
remote_player = Entity(model='cube', color=color.azure, scale=(1,2,1), position=(2,1,0), collider='box')

ground = Entity(model='plane', scale=50, color=color.green, collider='box', texture='white_cube', texture_scale=(50, 50))
platforms = []

# Parkour platforms
for i in range(10):
    platform = Entity(model='cube', color=color.gray, scale=(3, 0.5, 3), position=(i*5, 2+(i%3), 0), collider='box')
    platforms.append(platform)

camera.parent = player
camera.position = (0, 10, -20)
camera.rotation_x = 30

speed = 5
jump_height = 8
velocity_y = 0
gravity = -20

def update():
    global velocity_y
    move = Vec3(
        held_keys['d'] - held_keys['a'],
        0,
        held_keys['w'] - held_keys['s']
    ).normalized() * time.dt * speed

    player.position += player.forward * move.z + player.right * move.x

    # Gravity
    velocity_y += gravity * time.dt
    player.y += velocity_y * time.dt

    # Ground collision
    hit_info = player.intersects()
    if hit_info.hit:
        player.y += 0.01
        velocity_y = 0
        if held_keys['space']:
            velocity_y = jump_height

    # Send position to other player
    send_data = f"{player.x:.2f},{player.y:.2f},{player.z:.2f}"
    try:
        client.send(send_data.encode())
    except:
        pass

def receive_data():
    while True:
        try:
            data = client.recv(1024).decode()
            x, y, z = map(float, data.split(','))
            remote_player.position = (x, y, z)
        except:
            break

threading.Thread(target=receive_data, daemon=True).start()

app.run()
