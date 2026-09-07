<?php
session_start();

// If the user has an active session, automatically route them past the landing page
if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] === true) {
    if ($_SESSION['role'] === 'manager') {
        header("Location: manager_dashboard.php");
        exit;
    } else {
        header("Location: employee.php");
        exit;
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ENCOM OS-12 // Terminal Main</title>
    <style>
        body { background-color: #000; color: #00ffcc; font-family: monospace; padding: 50px; text-align: center; }
        .container { border: 2px solid #00ffcc; padding: 40px; max-width: 600px; margin: 0 auto; box-shadow: 0 0 15px #00ffcc; }
        .btn-connect { display: inline-block; background-color: #00ffcc; color: #000; padding: 15px 30px; font-weight: bold; text-decoration: none; border: 2px solid #00ffcc; cursor: pointer; margin-top: 20px; transition: background 0.3s ease; }
        .btn-connect:hover { background-color: #000; color: #00ffcc; }
        .notice { color: #ff3366; margin-top: 20px; font-size: 0.9em; }
        .footer { margin-top: 40px; font-size: 0.8em; color: #666; }
    </style>
</head>
<body>

<div class="container">
    <h1>ENCOM</h1>
    <h3>Mainframe Access Portal // OS-12</h3>
    <hr style="border-color: #00ffcc;">
    
    <p>SYSTEM: ONLINE</p>
    <p>GRID STATUS: STABLE</p>
    <p>SECURITY LEVEL: RESTRICTED</p>
    
    <p>Welcome to the ENCOM Central Network. This terminal tracks corporate sector migration, localized grid protocols, and upcoming internal simulation upgrades. Unauthorized digital footprints inside the system grid are strictly monitored and logged by the security daemon.</p>

    <div class="notice">
        NOTICE: LOCAL ASSET STAGING DIRECTORY ACTIVE. DO NOT DEPLOY ENCRYPTION KEYS TO UNSECURED BLOCKS.
    </div>

    <!-- Links directly to the centralized login portal -->
    <a href="login.php" class="btn-connect">[ Connect to Mainframe Grid ]</a>
    
    <div class="footer">
        © 1982-2026 ENCOM International. All Users Subject to Grid Protocol monitoring.
    </div>
</div>

</body>
</html>
