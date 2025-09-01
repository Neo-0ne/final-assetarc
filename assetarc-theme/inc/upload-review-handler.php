<?php
// upload-review-handler.php

// Exit if accessed directly
if (!defined('ABSPATH')) {
  exit;
}

// Check if the form has been submitted
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_FILES['review_file'])) {
  // Verify the nonce
  if (!isset($_POST['_wpnonce']) || !wp_verify_nonce($_POST['_wpnonce'], 'upload_review_nonce')) {
    assetarc_display_message('Invalid nonce.', 'error');
    return;
  }

  $uploaded = $_FILES['review_file'];
  $allowed_types = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
  $max_size = 5 * 1024 * 1024; // 5MB

  if (!in_array($uploaded['type'], $allowed_types)) {
    assetarc_display_message('Invalid file type. Only PDF and DOCX files are allowed.', 'error');
  } elseif ($uploaded['size'] > $max_size) {
    assetarc_display_message('File is too large. Maximum size is 5MB.', 'error');
  } else {
    // Send the file to the eng-vault service
    $api_url = 'http://eng-vault/vault/upload';
    $access_token = isset($_COOKIE['access_token']) ? $_COOKIE['access_token'] : '';

    if (empty($access_token)) {
        assetarc_display_message('You must be logged in to upload files.', 'error');
        return;
    }

    $boundary = '----' . microtime(true);
    $body = '';
    $body .= '--' . $boundary . "\r\n";
    $body .= 'Content-Disposition: form-data; name="file"; filename="' . basename($uploaded['name']) . '"' . "\r\n";
    $body .= 'Content-Type: ' . $uploaded['type'] . "\r\n\r\n";
    $body .= file_get_contents($uploaded['tmp_name']);
    $body .= "\r\n";
    $body .= '--' . $boundary . '--' . "\r\n";

    $response = wp_remote_post($api_url, [
        'method' => 'POST',
        'timeout' => 45,
        'headers' => [
            'Content-Type' => 'multipart/form-data; boundary=' . $boundary,
        ],
        'cookies' => [
            'access_token' => $access_token
        ],
        'body' => $body,
    ]);

    if (is_wp_error($response)) {
        assetarc_display_message('Upload failed. Could not connect to the vault service.', 'error');
    } else {
        $response_code = wp_remote_retrieve_response_code($response);
        if ($response_code === 200) {
            $response_body = json_decode(wp_remote_retrieve_body($response), true);
            $file_id = $response_body['file_id'] ?? 'unknown';
            assetarc_display_message('Upload successful! File ID: ' . esc_html($file_id));
        } else {
            assetarc_display_message('Upload failed with status code: ' . $response_code, 'error');
        }
    }
  }
}
?>
