<?php
// Theme Setup
function assetarc_theme_setup() {
  // Add support for featured images
  add_theme_support('post-thumbnails');

  // Register nav menu
  register_nav_menus(array(
    'primary' => __('Primary Menu', 'assetarc'),
  ));

  // Add support for custom logo
  add_theme_support('custom-logo', array(
    'height' => 60,
    'flex-height' => true,
    'flex-width' => true,
  ));
}
add_action('after_setup_theme', 'assetarc_theme_setup');

// Enqueue styles and scripts
function assetarc_enqueue_assets() {
  wp_enqueue_style('assetarc-style', get_stylesheet_uri());
  wp_enqueue_script('assetarc-scripts', get_template_directory_uri() . '/assets/main.js', array('jquery'), false, true);
}
add_action('wp_enqueue_scripts', 'assetarc_enqueue_assets');

// Load security functions
require get_template_directory() . '/inc/functions-security.php';

// Load Customizer settings
require get_template_directory() . '/inc/customizer.php';

// Load newsletter handler logic
require get_template_directory() . '/inc/newsletter-handler.php';

// Load contact form handler logic
require get_template_directory() . '/inc/contact-handler.php';

// Load upload review handler logic
require get_template_directory() . '/inc/upload-review-handler.php';

// Load token request handler logic
require get_template_directory() . '/inc/token-request-handler.php';

// Load any optional review routing logic
require get_template_directory() . '/parts/review-flag-router.php';

// Register Custom Post Types for Education Hub
function assetarc_register_post_types() {
    // Podcasts
    register_post_type('podcast', array(
        'labels' => array('name' => 'Podcasts', 'singular_name' => 'Podcast'),
        'public' => true,
        'has_archive' => true,
        'rewrite' => array('slug' => 'education/podcast'),
        'supports' => array('title', 'editor', 'thumbnail', 'excerpt'),
        'menu_icon' => 'dashicons-microphone',
    ));

    // Videos
    register_post_type('video', array(
        'labels' => array('name' => 'Videos', 'singular_name' => 'Video'),
        'public' => true,
        'has_archive' => true,
        'rewrite' => array('slug' => 'education/videos'),
        'supports' => array('title', 'editor', 'thumbnail', 'excerpt'),
        'menu_icon' => 'dashicons-video-alt3',
    ));
}
add_action('init', 'assetarc_register_post_types');

// Add rewrite rule for vault downloads
function assetarc_add_rewrite_rules() {
    add_rewrite_rule('^vault/download/([^/]+)/?$', 'index.php?assetarc_download_file=$matches[1]', 'top');
}
add_action('init', 'assetarc_add_rewrite_rules');

// Add the query var so WordPress recognizes it
function assetarc_add_query_vars($vars) {
    $vars[] = 'assetarc_download_file';
    return $vars;
}
add_filter('query_vars', 'assetarc_add_query_vars');

// Template redirect to handle the download
function assetarc_template_redirect() {
    if (get_query_var('assetarc_download_file')) {
        require get_template_directory() . '/inc/download-handler.php';
        exit;
    }
}
add_action('template_redirect', 'assetarc_template_redirect');

// Display styled messages
function assetarc_display_message($message, $type = 'success') {
  $class = $type === 'success' ? 'text-green-400' : 'text-red-400';
  echo "<p class='$class mt-4'>$message</p>";
}

// Hook for newsletter signup
function assetarc_handle_newsletter_signup() {
    require get_template_directory() . '/inc/newsletter-handler.php';
}
add_action('admin_post_nopriv_assetarc_newsletter_signup', 'assetarc_handle_newsletter_signup');
add_action('admin_post_assetarc_newsletter_signup', 'assetarc_handle_newsletter_signup');
