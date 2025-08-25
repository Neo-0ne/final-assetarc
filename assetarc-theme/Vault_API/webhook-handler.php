<?php
/**
 * Webhook handler for external services like payment gateways.
 */

// It's better to include WordPress functions if available, but this can run standalone.
// We won't use wp_remote_post here to keep it simple and dependency-free, using cURL instead.

header("Content-Type: application/json");

// --- Configuration ---
// This should be a secure, long, random string.
$webhook_secret = 'your-shared-secret-token'; // This should match what the payment gateway sends.
$internal_api_key = 'mock-internal-api-key'; // API key for communicating with our backend services.
$lifecycle_service_url = 'http://localhost:5005/api/v1/internal/enroll';
$course_id_to_enroll = 1;

// --- Security Check ---
$headers = getallheaders();
$signature = isset($headers['X-Webhook-Signature']) ? $headers['X-Webhook-Signature'] : '';

if (!hash_equals($webhook_secret, $signature)) {
    http_response_code(403);
    echo json_encode(['error' => 'Forbidden: Invalid signature']);
    exit();
}

// --- Parse Input ---
$input = json_decode(file_get_contents('php://input'), true);

if (!$input || !isset($input['event']) || !isset($input['client_id'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid payload']);
    exit();
}

// --- Event Handling ---
$event_type = $input['event'];
$user_email = $input['client_id']; // Assuming client_id holds the user's email.

if ($event_type === 'course_paid') {
    error_log("Received 'course_paid' event for user: " . $user_email);

    $payload = json_encode([
        'user_email' => $user_email,
        'course_id'  => $course_id_to_enroll,
    ]);

    $ch = curl_init($lifecycle_service_url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',
        'x-api-key: ' . $internal_api_key,
    ]);

    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($http_code >= 200 && $http_code < 300) {
        error_log("Successfully enrolled user " . $user_email . " in course " . $course_id_to_enroll);
        http_response_code(200);
        echo json_encode(['status' => 'success', 'message' => 'User enrollment processed.']);
    } else {
        error_log("Error enrolling user " . $user_email . ". Lifecycle service returned status " . $http_code . " and response: " . $response);
        http_response_code(502); // Bad Gateway, indicates an issue with the downstream service
        echo json_encode(['error' => 'Failed to process enrollment due to an internal error.']);
    }

} else {
    // Handle other events or just acknowledge them
    error_log("Received unhandled event type: " . $event_type);
    http_response_code(200);
    echo json_encode(['status' => 'success', 'message' => 'Event received but not actioned.']);
}
