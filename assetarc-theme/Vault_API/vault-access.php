<?php
// vault-access.php — handles secure token-based access to the Vault

// Load WordPress core to allow redirect and utility functions
require_once('../../../wp-load.php');

// Sanitize the token from POST
$submitted_token = isset($_POST['access_token']) ? sanitize_text_field($_POST['access_token']) : '';

// Define valid tokens and their redirects (to be customized as needed)
$valid_tokens = array(
    'advisor-123' => '/advisor-dashboard',
    'client-456'  => '/client-portal',
    'vault-demo'  => '/vault-preview',
    'arc2025'     => '/downloads/arc-package.zip',
    // Add more token => redirect_path mappings here
);

// Check if token is valid
if (array_key_exists($submitted_token, $valid_tokens)) {
    // Redirect to the mapped path
    wp_redirect(home_url($valid_tokens[$submitted_token]));
    exit;
} else {
    // Invalid token — redirect back to vault with error message
    $redirect_url = add_query_arg('vault_error', '1', home_url('/vault'));
    wp_redirect($redirect_url);
    exit;
}
