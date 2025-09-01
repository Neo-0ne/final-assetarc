<?php
// functions-security.php - Security hardening

// Remove WordPress version from head
remove_action('wp_head', 'wp_generator');

// Disable XML-RPC
add_filter('xmlrpc_enabled', '__return_false');

// Remove login error messages
function assetarc_no_login_errors() {
    return 'Access denied.';
}
add_filter('login_errors', 'assetarc_no_login_errors');

// Disable file editing from WP dashboard
define('DISALLOW_FILE_EDIT', true);
