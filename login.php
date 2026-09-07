<?php
// Start a secure session
session_start();

// Define user credentials array with secure bcrypt hashes
$users = [
    "m.anager" => [
        "password_hash" => '$2y$10$tMhI2.5vXzW4K5J9.cREkexXJ/f7P7mXn8P4cVYPqW1sX5eEeaT2i', // Hash for "SecuredGrid2026!"
        "role" => "manager"
    ],
    "kyson" => [
        "password_hash" => '$2y$10$7zB3c9XwA1vK4jY8zR6OueE9dM4y3lB2wA8q9Z0x1y2z3u4i5o6p.', // Hash for "GridMaster77!"
        "role" => "employee"
    ]
];

$error_message = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Sanitize input to mitigate basic injection risks
    $username = filter_input(INPUT_POST, 'username', FILTER_SANITIZE_SPECIAL_CHARS);
    $password = $_POST['password'] ?? '';

    // Verify if the user exists and the password matches the stored hash
    if (array_key_exists($username, $users) && password_verify($password, $users[$username]["password_hash"])) {
        // Regenerate session ID to mitigate Session Fixation attacks
        session_regenerate_id(true);
        
        // Store session variables dynamically based on the authenticated user
        $_SESSION['loggedin'] = true;
        $_SESSION['username'] = $username;
        $_SESSION['role'] = $users[$username]["role"];
        
        // Redirect logic based on system roles
        if ($_SESSION['role'] === 'manager') {
            header("Location: manager_dashboard.php");
        } else {
            header("Location: employee_dashboard.php");
        }
        exit;
    } else {
        $error_message = "Invalid username or password.";
    }
}
?>
