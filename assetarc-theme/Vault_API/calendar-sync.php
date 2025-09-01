<?php
// calendar-sync.php

header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = json_decode(file_get_contents("php://input"), true);
    $email = isset($input['email']) ? $input['email'] : '';

    if (!$email || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        echo json_encode(['success' => false, 'message' => 'Invalid email']);
        exit;
    }

    // Forward to backend Flask API
    $api_url = 'https://your-flask-endpoint.com/api/calendar-sync'; // 🔁 Replace with actual backend URL

    $response = wp_remote_post($api_url, [
        'method' => 'POST',
        'headers' => ['Content-Type' => 'application/json'],
        'body' => json_encode(['email' => $email]),
    ]);

    if (is_wp_error($response)) {
        echo json_encode(['success' => false, 'message' => 'Connection error']);
        exit;
    }

    $body = wp_remote_retrieve_body($response);
    echo $body;
    exit;
} else {
    echo json_encode(['success' => false, 'message' => 'Invalid method']);
    exit;
}
?>
