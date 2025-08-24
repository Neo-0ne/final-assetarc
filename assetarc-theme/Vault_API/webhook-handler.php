<?php
// webhook-handler.php

$secret = 'your-shared-secret-token'; // Replace with your secure token

// Validate incoming request
$headers = getallheaders();
if (!isset($headers['X-Webhook-Signature']) || $headers['X-Webhook-Signature'] !== $secret) {
    http_response_code(403);
    exit('Forbidden');
}

// Parse JSON input
$input = json_decode(file_get_contents('php://input'), true);

// Handle events
if (isset($input['event']) && $input['event'] === 'bot_completed') {
    $user_email = $input['email'];
    $bot_name = $input['bot'];
    $doc_url = $input['document_url'];

    // Do something (e.g., log or notify user)
    error_log("Bot $bot_name completed for $user_email. Result: $doc_url");

    http_response_code(200);
    echo 'Received';
} else {
    http_response_code(400);
    echo 'Invalid payload';
}
