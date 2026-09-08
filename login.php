<?php
// Start a secure session
session_start();

// Dynamically generate uncorrupted, perfectly formatted hashes directly inside server memory
$users = [
    "m.anager" => [
        "password_hash" => password_hash("SecuredGrid2026!", PASSWORD_BCRYPT),
        "role" => "manager"
    ],
    "kyson" => [
        "password_hash" => password_hash("GridMaster77!", PASSWORD_BCRYPT),
        "role" => "employee"
    ]
];

$error_message = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Sanitize input to mitigate basic injection risks
    $username = filter_input(INPUT_POST, 'username', FILTER_SANITIZE_SPECIAL_CHARS);
    $password = $_POST['password'] ?? '';

    // Standard absolute verification loop
    if (array_key_exists($username, $users) && password_verify($password, $users[$username]["password_hash"])) {
        // Regenerate session ID to prevent Session Fixation attacks
        session_regenerate_id(true);
        
        // Store session variables dynamically based on the authenticated user
        $_SESSION['loggedin'] = true;
        $_SESSION['username'] = $username;
        $_SESSION['role'] = $users[$username]["role"];
        
        // Role-based routing
        if ($_SESSION['role'] === 'manager') {
            header("Location: manager_dashboard.php");
        } else {
            header("Location: employee.php");
        }
        exit;
    } else {
        // Fallback Debug message block to identify variables if authentication fails
        $stored_hash = $users[$username]["password_hash"] ?? 'N/A';
        $error_message = "DEBUG LOGIFail:<br>" .
                        "• Captured User: [" . htmlspecialchars($username) . "]<br>" .
                        "• Input Password Length: " . strlen($password) . " chars<br>" .
                        "• Generated Hash: <code>" . $stored_hash . "</code> (Length: " . strlen($stored_hash) . ")<br>" .
                        "• Crypt Match Status: <strong>FALSE</strong>";
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
