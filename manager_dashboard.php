<?php
session_start();

// Enforce access control verification
if (!isset($_SESSION['loggedin']) || $_SESSION['loggedin'] !== true || $_SESSION['role'] !== 'manager') {
    // If not authenticated as manager, reject and redirect to login
    header("Location: login.php");
    exit;
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Manager Dashboard</title>
    <style>
        body { background-color: #000; color: #00ffcc; font-family: monospace; padding: 50px; }
        .container { border: 2px solid #00ffcc; padding: 20px; }
        a { color: #ff3333; }
    </style>
</head>
<body>

<div class="container">
    <h1>Welcome to the ENCOM Central Network</h1>
    <p>System Status: ONLINE</p>
    <p>Security Level: RESTRICTED (Manager Session Active)</p>
    <hr>
    <h3>Administrative Signing Keys</h3>
    <p>[SECURE_KEY_BLOCK_OS12-SEC4]</p>
    <hr>
    <p><a href="logout.php">Terminate Session (Logout)</a></p>
</div>

</body>
</html>
