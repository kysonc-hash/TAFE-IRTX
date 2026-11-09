# server.py
import socket
import threading
import time
import json
import random
import sqlite3
import os

HOST = '0.0.0.0'
PORT = 65432
GRID_SIZE = 80
TICK_RATE = 0.1

# =========================================================================
# CONFIGURATION: Set your custom database storage file directory route here
# =========================================================================
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "grid_system.db")

players = {}  # Format: { conn: { 'id', 'username', 'x', 'y', 'dx', 'dy', 'color', 'alive', 'trail', 'ready' } }
colors = [(0, 229, 255), (255, 0, 85), (255, 255, 0), (0, 255, 102)]
color_idx = 0
game_running = False
lock = threading.Lock()

def init_db():
    db_dir = os.path.dirname(DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone() == 0:
        mock_profiles = [
            ('admin', 'GridControl2026'),
            ('alan', 'SecOpsShield99'),
            ('sam', 'MTUxdmJGUnZkVzVsTkRreA==')
        ]
        cursor.executemany("INSERT INTO users (username, password) VALUES (?, ?)", mock_profiles)
        conn.commit()
    conn.close()

def db_authenticate(username, password):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE LOWER(username) = LOWER(?)", (username.strip(),))
        row = cursor.fetchone()
        conn.close()
        if row and row == password:
            return True
    except Exception as e:
        print(f"[!] Database read error: {e}")
    return False

def handle_client(conn, addr):
    global color_idx
    print(f"[*] Node synchronization request observed from: {addr}")
    
    authenticated = False
    username = None
    buffer = ""

    while not authenticated:
        try:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                conn.close()
                return
            buffer += data
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                msg = json.loads(line)
                if msg.get('type') == 'login':
                    user_try = msg.get('username', '')
                    pass_try = msg.get('password', '')
                    if db_authenticate(user_try, pass_try):
                        authenticated = True
                        username = user_try
                        conn.sendall((json.dumps({'type': 'auth_success'}) + "\n").encode('utf-8'))
                    else:
                        conn.sendall((json.dumps({'type': 'auth_failed'}) + "\n").encode('utf-8'))
        except (ConnectionResetError, json.JSONDecodeError):
            conn.close()
            return

    with lock:
        my_color = colors[color_idx % len(colors)]
        color_idx += 1
        players[conn] = {
            'id': username,
            'username': username,
            'x': random.randint(10, GRID_SIZE - 10),
            'y': random.randint(10, GRID_SIZE - 10),
            'dx': 1, 'dy': 0,
            'color': my_color,
            'alive': True,
            'trail': [],
            'ready': False  # Default hold gate position active
        }
    
    handshake = {'type': 'init', 'id': username, 'grid_size': GRID_SIZE}
    conn.sendall((json.dumps(handshake) + "\n").encode('utf-8'))

    while True:
        try:
            data = conn.recv(1024).decode('utf-8')
            if not data: break
            buffer += data
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                msg = json.loads(line)
                
                if msg.get('type') == 'ready':
                    with lock:
                        p = players.get(conn)
                        if p: 
                            p['ready'] = True
                            print(f"[+] Player Grid-Ready Signaled: {username}")
                
                elif msg.get('type') == 'move':
                    with lock:
                        p = players.get(conn)
                        if p and p['alive'] and p['ready']:
                            if msg['dx'] == -p['dx'] and msg['dx'] != 0: continue
                            if msg['dy'] == -p['dy'] and msg['dy'] != 0: continue
                            p['dx'], p['dy'] = msg['dx'], msg['dy']
        except ConnectionResetError:
            break

    with lock:
        if conn in players: del players[conn]
    conn.close()

def game_loop():
    while game_running:
        time.sleep(TICK_RATE)
        with lock:
            if not players: continue
            
            # Step 1: Step heads forward ONLY if player ready validation flag is true
            for conn, p in players.items():
                if not p['alive'] or not p['ready']: continue
                p['trail'].append([p['x'], p['y']])
                p['x'] += p['dx']
                p['y'] += p['dy']
                if p['x'] < 0 or p['x'] >= GRID_SIZE or p['y'] < 0 or p['y'] >= GRID_SIZE:
                    p['alive'] = False

            # Step 2: Calculate intersections
            for conn1, p1 in players.items():
                if not p1['alive'] or not p1['ready']: continue
                for conn2, p2 in players.items():
                    if not p2['ready']: continue
                    for tx, ty in p2['trail']:
                        if p1['x'] == tx and p1['y'] == ty:
                            p1['alive'] = False
                    if p1['id'] != p2['id'] and p1['x'] == p2['x'] and p1['y'] == p2['y']:
                        p1['alive'] = False
                        p2['alive'] = False

            # Step 3: Global sync broadcast mapping ready flags
            serializable_state = {
                'type': 'state',
                'players': {p['id']: {'x': p['x'], 'y': p['y'], 'color': p['color'], 'alive': p['alive'], 'trail': p['trail'], 'ready': p['ready']} for p in players.values()}
            }
            packet = (json.dumps(serializable_state) + "\n").encode('utf-8')
            for conn in list(players.keys()):
                try:
                    conn.sendall(packet)
                except Exception:
                    pass

def main():
    global game_running
    init_db()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SYSTEM] Identity Authoritative Grid Daemon listening on port {PORT}")
    
    game_running = True
    threading.Thread(target=game_loop, daemon=True).start()
    try:
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()

if __name__ == '__main__':
    main()
