<?php
// favicon.php - Controls favicon display
$favicon_url = get_theme_mod('assetarc_favicon');

if (!$favicon_url) {
    $favicon_url = get_template_directory_uri() . '/favicon.ico'; // fallback
}
?>

<link rel="shortcut icon" href="<?php echo esc_url($favicon_url); ?>" type="image/x-icon">
<link rel="icon" href="<?php echo esc_url($favicon_url); ?>" type="image/x-icon">
