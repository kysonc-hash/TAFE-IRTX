# server.py
import socket
import threading
import time
import json
import random
import sqlite3

HOST = '0.0.0.0'
PORT = 65432
GRID_SIZE = 80
TICK_RATE = 0.1
DB_FILE = 'grid_system.db'

players = {}  # Format: { conn: { 'id', 'username', 'x', 'y', 'dx', 'dy', 'color', 'alive', 'trail' } }
colors = [(0, 229, 255), (255, 0, 85), (255, 255, 0), (0, 255, 102)]
color_idx = 0
game_running = False
lock = threading.Lock()

# Initialize the SQLite Database and define core table schemas
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create the user identity table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Insert mock testing records matching your playbook narrative if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        # Example records (Pre-calculated strings for your testing window)
        mock_users = [
            ('admin', 'GridControl2026'),
            ('alan', 'SecOpsShield99'),
            ('Bowie', 'MTUxdmJGUnZkVzVsTkRreA==') # Dog tag numeric ID converted to Base64
        ]
        cursor.executemany("INSERT INTO users (username, password) VALUES (?, ?)", mock_users)
        conn.commit()
        print("[DATABASE] Default user registry templates initialized.")
        
    conn.close()

# Verify client credentials against stored hashes/records
def verify_credentials(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username.lower().strip(),))
    row = cursor.fetchone()
    conn.close()
    
    if row and row[0] == password:
        return True
    return False

def handle_client(conn, addr):
    global color_idx
    print(f"[*] Connection vector detected from network node: {addr}")
    
    authenticated = False
    username = None
    buffer = ""

    # Authentication Phase Loop
    while not authenticated:
        try:
            data = conn.recv(1024).decode('utf-8')
            if not data: return
            buffer += data
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                msg = json.loads(line)
                
                if msg.get('type') == 'login':
                    user_input = msg.get('username', '')
                    pass_input = msg.get('password', '')
                    
                    if verify_credentials(user_input, pass_input):
                        print(f"[+] Node Authenticated. Identity: {user_input} ({addr})")
                        authenticated = True
                        username = user_input
                        # Send access verification approval to terminal
                        conn.sendall((json.dumps({'type': 'auth_success'}) + "\n").encode('utf-8'))
                    else:
                        print(f"[-] Unauthorized identity sequence rejected for username: {user_input}")
                        conn.sendall((json.dumps({'type': 'auth_failed'}) + "\n").encode('utf-8'))
        except (ConnectionResetError, json.JSONDecodeError):
            conn.close()
            return

    # Post-Authentication: Deploy Light Cycle to active memory grid
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
            'trail': []
        }
    
    # Complete initial handshake
    handshake = {'type': 'init', 'id': username, 'grid_size': GRID_SIZE}
    conn.sendall((json.dumps(handshake) + "\n").encode('utf-8'))

    # Active Game Input Processing Loop
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
                        p = players.get(conn)
                        if p and p['alive']:
                            if msg['dx'] == -p['dx'] and msg['dx'] != 0: continue
                            if msg['dy'] == -p['dy'] and msg['dy'] != 0: continue
                            p['dx'], p['dy'] = msg['dx'], msg['dy']
        except ConnectionResetError:
            break

    print(f"[-] Terminal Session Severed: {username} ({addr})")
    with lock:
        if conn in players: del players[conn]
    conn.close()

def game_loop():
    while game_running:
        time.sleep(TICK_RATE)
        with lock:
            if not players: continue
            
            for conn, p in players.items():
                if not p['alive']: continue
                p['trail'].append([p['x'], p['y']])
                p['x'] += p['dx']
                p['y'] += p['dy']
                if p['x'] < 0 or p['x'] >= GRID_SIZE or p['y'] < 0 or p['y'] >= GRID_SIZE:
                    p['alive'] = False

            for conn1, p1 in players.items():
                if not p1['alive']: continue
                for conn2, p2 in players.items():
                    for tx, ty in p2['trail']:
                        if p1['x'] == tx and p1['y'] == ty:
                            p1['alive'] = False
                    if p1['id'] != p2['id'] and p1['x'] == p2['x'] and p1['y'] == p2['y']:
                        p1['alive'] = False
                        p2['alive'] = False

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
    init_db()  # Validate database schemas on startup
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SYSTEM] Identity Authoritative Grid Daemon listening on port {PORT}...")
    
    game_running = True
    threading.Thread(target=game_loop, daemon=True).start()
    
    try:
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\n[!] System shutting down.")
    finally:
        server.close()

if __name__ == '__main__':
    main()
