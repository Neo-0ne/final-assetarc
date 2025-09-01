<?php
// token-request-handler.php

// Exit if accessed directly
if (!defined('ABSPATH')) {
  exit;
}

// Check if the form has been submitted
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['name']) && isset($_POST['email']) && isset($_POST['reason'])) {
  // Verify the nonce
  if (!isset($_POST['_wpnonce']) || !wp_verify_nonce($_POST['_wpnonce'], 'token_request_nonce')) {
    assetarc_display_message('Invalid nonce.', 'error');
    return;
  }

  $name = sanitize_text_field($_POST['name']);
  $email = sanitize_email($_POST['email']);
  $reason = sanitize_textarea_field($_POST['reason']);

  if (!is_email($email)) {
    assetarc_display_message('Invalid email address.', 'error');
  } else {
    // Send the request to the eng-identity service
    $api_url = 'http://eng-identity/api/v1/advisor/request-client-token';
    $access_token = isset($_COOKIE['access_token']) ? $_COOKIE['access_token'] : '';

    if (empty($access_token)) {
        assetarc_display_message('You must be logged in as an advisor to request tokens.', 'error');
        return;
    }

    $response = wp_remote_post($api_url, [
        'method' => 'POST',
        'timeout' => 20,
        'headers' => [
            'Content-Type' => 'application/json',
        ],
        'cookies' => [
            'access_token' => $access_token
        ],
        'body' => json_encode([
            'client_name' => $name,
            'client_email' => $email,
            'reason' => $reason,
        ]),
    ]);

    if (is_wp_error($response)) {
        assetarc_display_message('Request failed. Could not connect to the identity service.', 'error');
    } else {
        $response_code = wp_remote_retrieve_response_code($response);
        if ($response_code === 200) {
            assetarc_display_message('Client token request submitted successfully.');
        } else {
            assetarc_display_message('Failed to submit token request. Please try again.', 'error');
        }
    }
  }
}
?>
