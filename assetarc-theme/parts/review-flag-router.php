<?php
// review-flag-router.php

// Ensure this file only handles POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
  http_response_code(405);
  echo json_encode(['error' => 'Method not allowed']);
  exit;
}

// Validate incoming request
if (!isset($_POST['doc_id']) || !isset($_POST['flag_reason']) || !isset($_POST['user_token'])) {
  http_response_code(400);
  echo json_encode(['error' => 'Missing required parameters']);
  exit;
}

$docId = sanitize_text_field($_POST['doc_id']);
$flagReason = sanitize_text_field($_POST['flag_reason']);
$userToken = sanitize_text_field($_POST['user_token']);

// Forward request to Flask backend (assumes secure internal API)
$flask_url = 'https://backend.assetarc.com/review/flag';

$response = wp_remote_post($flask_url, [
  'headers' => ['Content-Type' => 'application/json'],
  'body'    => json_encode([
    'doc_id'      => $docId,
    'flag_reason' => $flagReason,
    'user_token'  => $userToken
  ]),
  'timeout' => 10
]);

if (is_wp_error($response)) {
  http_response_code(502);
  echo json_encode(['error' => 'Failed to reach review queue']);
  exit;
}

$body = wp_remote_retrieve_body($response);
http_response_code(200);
echo $body;
