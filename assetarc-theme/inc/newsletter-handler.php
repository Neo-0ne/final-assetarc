<?php
// newsletter-handler.php

// Exit if accessed directly
if (!defined('ABSPATH')) {
  exit;
}

// Check if POST request and nonce are set
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['newsletter_email'])) {
  $email = sanitize_email($_POST['newsletter_email']);

  if (!is_email($email)) {
    wp_send_json_error(['message' => 'Invalid email address.']);
    exit;
  }

  // Connect to the backend lifecycle service
  $endpoint = 'http://eng-lifecycle/api/v1/subscribe';
  $api_key = get_option('assetarc_api_key');

  $response = wp_remote_post($endpoint, [
    'method' => 'POST',
    'timeout' => 15,
    'headers' => [
      'Content-Type' => 'application/json',
      'x-api-key' => $api_key
    ],
    'body' => json_encode(['email' => $email]),
  ]);

  if (is_wp_error($response)) {
    wp_send_json_error(['message' => 'Subscription failed. Could not connect to service.']);
  } else {
    $response_code = wp_remote_retrieve_response_code($response);
    if ($response_code === 200) {
      wp_send_json_success(['message' => 'You are now subscribed.']);
    } else {
      $body = wp_remote_retrieve_body($response);
      $data = json_decode($body, true);
      $error_message = $data['error'] ?? 'An unknown error occurred.';
      wp_send_json_error(['message' => 'Subscription failed: ' . $error_message]);
    }
  }
  exit;
}
?>
