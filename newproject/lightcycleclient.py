# client.py
import socket
import threading
import json
import sys

try:
    import pygame
except ImportError:
    print("[!] Error: dependency required. Run: pip install pygame")
    sys.exit(1)

SERVER_IP = '192.168.1.10'
PORT = 65432

print("==================================================")
print("      THE GRID: PROTOCOL DISPATCH INTERFACE       ")
print("==================================================")
input_user = input("System Node Identity Access (Username): ")
input_pass = input("SecOps Operational Authentication (Password): ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((SERVER_IP, PORT))
except Exception as e:
    print(f"[!] Access Path Failure: {e}")
    sys.exit(1)

auth_payload = json.dumps({'type': 'login', 'username': input_user, 'password': input_pass}) + "\n"
client_socket.sendall(auth_payload.encode('utf-8'))

auth_buffer = ""
access_authorized = False
while not access_authorized:
    data = client_socket.recv(1024).decode('utf-8')
    if not data: sys.exit(1)
    auth_buffer += data
    if "\n" in auth_buffer:
        line, auth_buffer = auth_buffer.split("\n", 1)
        response = json.loads(line)
        if response.get('type') == 'auth_success':
            print("[+] ACCESS VECTOR ESTABLISHED.")
            access_authorized = True
        else:
            print("[-] ACCESS EXCLUDED.")
            client_socket.close()
            sys.exit(1)

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
my_ready_status = False

def network_ingress_worker():
    global my_id, grid_size, scale, game_state
    buffer = ""
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

running = True
blink_timer = 0

while running:
    clock.tick(60)
    blink_timer = (blink_timer + 1) % 60
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not my_ready_status:
                my_ready_status = True
                # Dispatch authorization packet indicating initialization trigger
                client_socket.sendall((json.dumps({'type': 'ready'}) + "\n").encode('utf-8'))
            
            elif my_ready_status:
                if event.key in [pygame.K_UP, pygame.K_w]:     packet = {'type': 'move', 'dx': 0, 'dy': -1}
                elif event.key in [pygame.K_DOWN, pygame.K_s]:  packet = {'type': 'move', 'dx': 0, 'dy': 1}
                elif event.key in [pygame.K_LEFT, pygame.K_a]:  packet = {'type': 'move', 'dx': -1, 'dy': 0}
                elif event.key in [pygame.K_RIGHT, pygame.K_d]: packet = {'type': 'move', 'dx': 1, 'dy': 0}
                else: continue
                client_socket.sendall((json.dumps(packet) + "\n").encode('utf-8'))

    screen.fill((2, 8, 19))
    
    # Draw backdrop grids
    for x in range(0, window_size, scale * 2):
        pygame.draw.line(screen, (10, 30, 50), (x, 0), (x, window_size), 1)
        pygame.draw.line(screen, (10, 30, 50), (0, x), (window_size, x), 1)

    with state_lock:
        # Check server data for current player's live presence parameters
        current_player_data = game_state.get(str(my_id))
        
        for pid_str, p in game_state.items():
            if not p.get('ready', False): continue # Keep unready loops invisible
            
            color = tuple(p['color'])
            if len(p['trail']) > 1:
                scaled_trail = [(pt * scale + scale//2, pt * scale + scale//2) for pt in p['trail']]
                pygame.draw.lines(screen, color, False, scaled_trail, max(2, scale - 2))
            
            if p['alive']:
                pygame.draw.rect(screen, (255, 255, 255), (p['x'] * scale, p['y'] * scale, scale, scale))
                pygame.draw.rect(screen, color, (p['x'] * scale, p['y'] * scale, scale, scale), 1)

        # Overlay Menu Graphics for Pre-Flight Hold Phase
        if current_player_data and not current_player_data.get('ready', False):
            overlay = pygame.Surface((window_size, window_size), pygame.SRCALPHA)
            overlay.fill((2, 8, 19, 200)) # Clean dimming transparency backdrop tint
            screen.blit(overlay, (0, 0))
            if blink_timer < 30:
                txt = font.render("GRID ON HOLD // PRESS SPACEBAR TO DEPLOY CYCLE", True, (0, 229, 255))
                screen.blit(txt, (window_size//2 - txt.get_width()//2, window_size//2 - 10))
                
        elif current_player_data and not current_player_data['alive']:
            txt = font.render("CYCLE DEREGISTERED // DISCONNECTED", True, (255, 0, 85))
            screen.blit(txt, (20, 20))

    pygame.display.flip()

pygame.quit()
client_socket.close()
