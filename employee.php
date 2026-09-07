<?php
session_start();

// Basic Access Control: Ensure the user is logged in
if (!isset($_SESSION['loggedin']) || $_SESSION['loggedin'] !== true) {
    header("Location: login.php");
    exit;
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Employee Workspace</title>
    <style>
        body { background-color: #000; color: #00ffcc; font-family: monospace; padding: 50px; }
        .container { border: 2px solid #00ffcc; padding: 20px; }
        a { color: #ff3333; }
    </style>
</head>
<body>

<div class="container">
    <h1>ENCOM Employee Portal</h1>
    <p>System Status: ONLINE</p>
    <p>Welcome back, <strong><?php echo htmlspecialchars($_SESSION['username']); ?></strong>!</p>
    <p>Security Level: STANDARD EMPLOYEE ACCESS</p>
    <hr>
    <h3>Active Tasks</h3>
    <ul>
        <li>Review simulation codebases.</li>
        <li>Compile sector migration logs.</li>
    </ul>
    <hr>
    <p><a href="logout.php">Terminate Session (Logout)</a></p>
</div>

</body>
</html>
