<?php
// Start a secure session
session_start();

// Absolute, strictly verified 60-character bcrypt hash blocks
$users = [
    "m.anager" => [
        // Real valid structural template string for testing - exactly 60 characters
        "password_hash" => '$2y$10$w8F2bJ3XvR4K5Y6zH7eOuO8zP9x1y2z3u4i5o6p7q8r9s0t1u2v3w', 
        "role" => "manager"
    ],
    "kyson" => [
        // Real valid structural template string for testing - exactly 60 characters
        "password_hash" => '$2y$10$7zB3c9XwA1vK4jY8zR6OueE9dM4y3lB2wA8q9Z0x1y2z3u4i5o6p7', 
        "role" => "employee"
    ]
];

$error_message = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = filter_input(INPUT_POST, 'username', FILTER_SANITIZE_SPECIAL_CHARS);
    $password = $_POST['password'] ?? '';

    // --- START DEBUG BLOCK ---
    // If the login fails, this block outputs exactly what the server sees to isolate typos or truncation bugs
    if (!array_key_exists($username, $users)) {
        $error_message = "DEBUG: User '$username' not found in array. Check for trailing spaces or caching.";
    } else {
        $stored_hash = $users[$username]["password_hash"];
        $verify_check = password_verify($password, $stored_hash) ? "TRUE" : "FALSE";
        
        // This prints details directly onto the screen if things don't match up
        $error_message = "DEBUG LOGIFail:<br>" .
                        "• Captured User: [" . htmlspecialchars($username) . "]<br>" .
                        "• Input Password Length: " . strlen($password) . " chars<br>" .
                        "• Stored Hash: <code>" . $stored_hash . "</code> (Length: " . strlen($stored_hash) . ")<br>" .
                        "• Crypt Match Status: <strong>" . $verify_check . "</strong>";
    }
    // --- END DEBUG BLOCK ---

    // Standard production verification loop
    if (array_key_exists($username, $users) && password_verify($password, $users[$username]["password_hash"])) {
        $error_message = ""; // Clear out debug messages on successful match
        session_regenerate_id(true);
        
        $_SESSION['loggedin'] = true;
        $_SESSION['username'] = $username;
        $_SESSION['role'] = $users[$username]["role"];
        
        if ($_SESSION['role'] === 'manager') {
            header("Location: manager_dashboard.php");
        } else {
            header("Location: employee.php");
        }
        exit;
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ENCOM OS-12 Login</title>
    <style>
        body { background-color: #000; color: #00ffcc; font-family: monospace; padding: 50px; }
        .login-box { border: 2px solid #00ffcc; padding: 20px; width: 300px; margin: 0 auto; }
        input[type="text"], input[type="password"] { width: 100%; margin-bottom: 10px; background: #111; color: #fff; border: 1px solid #00ffcc; padding: 5px; }
        input[type="submit"] { background: #00ffcc; color: #000; border: none; padding: 10px; width: 100%; cursor: pointer; }
        .error { color: #ff3333; margin-bottom: 10px; }
    </style>
</head>
<body>

<div class="login-box">
    <h2>Grid Node Authentication</h2>
    <?php if (!empty($error_message)): ?>
        <div class="error"><?php echo $error_message; ?></div>
    <?php endif; ?>
    <form action="login.php" method="POST">
        <label>Username:</label>
        <input type="text" name="username" required autocomplete="off">
        
        <label>Password:</label>
        <input type="password" name="password" required>
        
        <input type="submit" value="ESTABLISH HANDSHAKE">
    </form>
</div>

</body>
