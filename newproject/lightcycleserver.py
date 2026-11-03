import socket
import threading
import time
import json
import random

HOST = '0.0.0.0'  # Binds to all network interfaces on the machine
PORT = 65432
GRID_SIZE = 80
TICK_RATE = 0.1  # Update interval (seconds) per tick loop iteration

players = {}  # Format: { conn: { 'id', 'x', 'y', 'dx', 'dy', 'color', 'alive', 'trail' } }
colors = [(0, 229, 255), (255, 0, 85), (255, 255, 0), (0, 255, 102)]
color_idx = 0
game_running = False
lock = threading.Lock()

def handle_client(conn, addr, player_id):
    global color_idx, game_running
    print(f"[+] Operational Inbound Node Hooked: {addr} Assigned ID: {player_id}")
    
    with lock:
        my_color = colors[color_idx % len(colors)]
        color_idx += 1
        players[conn] = {
            'id': player_id,
            'x': random.randint(10, GRID_SIZE - 10),
            'y': random.randint(10, GRID_SIZE - 10),
            'dx': 1, 'dy': 0,
            'color': my_color,
            'alive': True,
            'trail': []
        }
    
    # Handshake packet mapping environment constraints
    handshake = {'type': 'init', 'id': player_id, 'grid_size': GRID_SIZE}
    conn.sendall((json.dumps(handshake) + "\n").encode('utf-8'))

    buffer = ""
    while True:
        try:
            data = conn.recv(1024).decode('utf-8')
            if not data: break
            buffer += data
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                msg = json.loads(line)
                if msg.get('type') == 'move':
                    with lock:
                        p = players[conn]
                        if p['alive']:
                            # Guard against 180-degree immediate self-collisions
                            if msg['dx'] == -p['dx'] and msg['dx'] != 0: continue
                            if msg['dy'] == -p['dy'] and msg['dy'] != 0: continue
                            p['dx'], p['dy'] = msg['dx'], msg['dy']
        except ConnectionResetError:
            break

    print(f"[-] Client Node Severed: {addr}")
    with lock:
        del players[conn]
    conn.close()

def game_loop():
    global game_running
    print("[SYSTEM] Light Cycle State Engine Spinning Up...")
    while game_running:
        time.sleep(TICK_RATE)
        with lock:
            if not players: continue
            
            # Step 1: Step heads forward and update trail arrays
            for conn, p in players.items():
                if not p['alive']: continue
                p['trail'].append([p['x'], p['y']])
                p['x'] += p['dx']
                p['y'] += p['dy']
                
                # Check grid boundary failures
                if p['x'] < 0 or p['x'] >= GRID_SIZE or p['y'] < 0 or p['y'] >= GRID_SIZE:
                    p['alive'] = False

            # Step 2: Calculate path intersection and crash updates
            for conn1, p1 in players.items():
                if not p1['alive']: continue
                
                for conn2, p2 in players.items():
                    # Evaluate grid intersection overlap
                    for tx, ty in p2['trail']:
                        if p1['x'] == tx and p1['y'] == ty:
                            p1['alive'] = False
                    # Direct nose-to-nose impact resolution
                    if p1['id'] != p2['id'] and p1['x'] == p2['x'] and p1['y'] == p2['y']:
                        p1['alive'] = False
                        p2['alive'] = False

            # Step 3: Broadcast updated state vectors to clients
            serializable_state = {
                'type': 'state',
                'players': {p['id']: {'x': p['x'], 'y': p['y'], 'color': p['color'], 'alive': p['alive'], 'trail': p['trail']} for p in players.values()}
            }
            packet = (json.dumps(serializable_state) + "\n").encode('utf-8')
            for conn in list(players.keys()):
                try:
                    conn.sendall(packet)
                except Exception:
                    pass

def main():
    global game_running
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SYSTEM] Authoritative Core daemon operational on network port {PORT}")
    
    game_running = True
    threading.Thread(target=game_loop, daemon=True).start()
    
    pid_counter = 0
    try:
        while True:
            conn, addr = server.accept()
            pid_counter += 1
            threading.Thread(target=handle_client, args=(conn, addr, pid_counter), daemon=True).start()
    except KeyboardInterrupt:
        print("\n[!] Halting Simulation Frame.")
    finally:
        server.close()

if __name__ == '__main__':
    main()
