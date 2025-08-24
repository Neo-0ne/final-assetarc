<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
  <meta charset="<?php bloginfo('charset'); ?>">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title><?php bloginfo('name'); ?><?php wp_title('|'); ?></title>
  <?php get_template_part('favicon'); ?>
  <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>

<?php get_template_part('preloader'); ?>

<header class="site-header">
  <div class="container header-container">
    <div class="site-logo">
      <?php
      if (has_custom_logo()) {
          the_custom_logo();
      } else {
          echo '<h1 style="color:#FFD700;">' . get_bloginfo('name') . '</h1>';
      }
      ?>
    </div>

    <nav class="main-nav">
      <?php
        wp_nav_menu(array(
          'theme_location' => 'primary',
          'menu_class'     => 'nav-menu',
          'container'      => false
        ));
      ?>
    </nav>

    <div class="cta-buttons">
      <a href="/login" class="btn btn-outline">Client Login</a>
      <a href="/book" class="btn btn-gold">Book a Call</a>
    </div>
  </div>
</header>

<main class="site-main">
