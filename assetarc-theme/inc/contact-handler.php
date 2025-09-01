<?php
// contact-handler.php

// Exit if accessed directly
if (!defined('ABSPATH')) {
  exit;
}

// Check if the form has been submitted
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['name']) && isset($_POST['email']) && isset($_POST['message'])) {
  // Verify the nonce
  if (!isset($_POST['_wpnonce']) || !wp_verify_nonce($_POST['_wpnonce'], 'contact_form_nonce')) {
    assetarc_display_message('Invalid nonce.', 'error');
    return;
  }

  // Sanitize the input
  $name = sanitize_text_field($_POST['name']);
  $email = sanitize_email($_POST['email']);
  $message = sanitize_textarea_field($_POST['message']);

  // Validate the input
  if (!is_email($email)) {
    assetarc_display_message('Invalid email address.', 'error');
    return;
  }

  // Send the data to the backend service
  $api_url = 'http://eng-lifecycle/api/v1/contact'; // Use the internal service name
  $api_key = get_option('assetarc_api_key'); // An API key for service-to-service auth

  $response = wp_remote_post($api_url, array(
    'method'    => 'POST',
    'headers'   => array(
      'Content-Type' => 'application/json',
      'x-api-key' => $api_key
    ),
    'body'      => json_encode(array(
      'name'    => $name,
      'email'   => $email,
      'message' => $message,
    )),
    'timeout'   => 15,
  ));

  if (is_wp_error($response)) {
    assetarc_display_message('There was an error sending your message. Please try again later.', 'error');
  } else {
    $response_code = wp_remote_retrieve_response_code($response);
    if ($response_code === 200) {
      assetarc_display_message('Your message has been sent successfully!');
    } else {
      assetarc_display_message('There was an error sending your message. Please try again later.', 'error');
    }
  }
}
?>
