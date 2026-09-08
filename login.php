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
