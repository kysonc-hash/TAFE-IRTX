# client.py
import socket
import threading
import json
import sys

try:
    import pygame
except ImportError:
    print("[!] Error: Pygame dependency missing.")
    sys.exit(1)

SERVER_IP = '192.168.1.10'
PORT = 65432

# Terminal-Based User Authentication Prompt Sequence
print("==================================================")
print("       THE GRID INTERNAL AUTHENTICATION LINK       ")
print("==================================================")
user_input = input("Enter System Identity (Username): ")
pass_input = input("Enter Access Authentication (Password): ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((SERVER_IP, PORT))
except Exception as e:
    print(f"[!] Target Core Server Offline or Inaccessible: {e}")
    sys.exit(1)

# Package and dispatch credentials over network pipeline
login_packet = json.dumps({'type': 'login', 'username': user_input, 'password': pass_input}) + "\n"
client_socket.sendall(login_packet.encode('utf-8'))

# Wait for server authentication evaluation response
buffer = ""
authenticated = False
while not authenticated:
    data = client_socket.recv(1024).decode('utf-8')
    if not data:
        print("[!] Network handshake dropped by remote host.")
        sys.exit(1)
    buffer += data
    if "\n" in buffer:
        line, buffer = buffer.split("\n", 1)
        response = json.loads(line)
        if response.get('type') == 'auth_success':
            print("[+] ACCESS GRANTED. Loading graphics subsystem...")
            authenticated = True
        else:
            print("[-] ACCESS DENIED: Invalid identity credentials profile matching.")
            client_socket.close()
            sys.exit(1)

# Graphics Environment Configurations
pygame.init()
font = pygame.font.SysFont('courier', 16)
clock = pygame.time.Clock()

my_id = None
grid_size = 80
window_size = 640
scale = window_size // grid_size
screen = pygame.display.set_mode((window_size, window_size))
pygame.display.set_caption("The Grid // Light Cycle Terminal")

game_state = {}
state_lock = threading.Lock()

def network_ingress_worker():
    global my_id, grid_size, scale, game_state, buffer
    while True:
        try:
            data = client_socket.recv(4096).decode('utf-8')
            if not data: break
            buffer += data
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                msg = json.loads(line)
                
                if msg.get('type') == 'init':
                    my_id = msg['id']
                    grid_size = msg['grid_size']
                    scale = window_size // grid_size
                elif msg.get('type') == 'state':
                    with state_lock:
                        game_state = msg['players']
        except Exception:
            break

threading.Thread(target=network_ingress_worker, daemon=True).start()

def send_move(dx, dy):
    packet = json.dumps({'type': 'move', 'dx': dx, 'dy': dy}) + "\n"
    try:
        client_socket.sendall(packet.encode('utf-8'))
    except Exception:
        pass

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, pygame.K_w]:    send_move(0, -1)
            elif event.key in [pygame.K_DOWN, pygame.K_s]:  send_move(0, 1)
            elif event.key in [pygame.K_LEFT, pygame.K_a]:  send_move(-1, 0)
            elif event.key in [pygame.K_RIGHT, pygame.K_d]: send_move(1, 0)

    screen.fill((2, 8, 19))
    for x in range(0, window_size, scale * 2):
        pygame.draw.line(screen, (10, 30, 50), (x, 0), (x, window_size), 1)
        pygame.draw.line(screen, (10, 30, 50), (0, x), (window_size, x), 1)

    with state_lock:
        for pid_str, p in game_state.items():
            color = tuple(p['color'])
            if len(p['trail']) > 1:
                scaled_trail = [(pt * scale + scale//2, pt * scale + scale//2) for pt in p['trail']]
                pygame.draw.lines(screen, color, False, scaled_trail, max(2, scale - 2))
            if p['alive']:
                pygame.draw.rect(screen, (255, 255, 255), (p['x'] * scale, p['y'] * scale, scale, scale))
                pygame.draw.rect(screen, color, (p['x'] * scale, p['y'] * scale, scale, scale), 1)
            if str(my_id) == pid_str and not p['alive']:
                txt = font.render("CYCLE DEREGISTERED // DISCONNECTED", True, (255, 0, 85))
                screen.blit(txt, (20, 20))

    pygame.display.flip()

pygame.quit()
client_socket.close()
