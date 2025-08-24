<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
  <meta charset="<?php bloginfo('charset'); ?>">
  <meta name="viewport" content="width=device-width, initial-scale=1">
   <!-- Jules: Added dynamic title and meta description logic for SEO -->
    <?php if (is_front_page() || is_home()) : ?>
        <title><?php bloginfo('name'); ?> | Automated Legal & Tax Structuring</title>
        <meta name="description" content="AssetArc provides automated workflows for asset protection, tax efficiency, and corporate structuring. Generate compliant legal documents with human review.">
    <?php elseif (is_page()) : ?>
        <title><?php the_title(); ?> | <?php bloginfo('name'); ?></title>
        <?php if (has_excerpt()) : ?>
            <meta name="description" content="<?php echo esc_attr(get_the_excerpt()); ?>">
        <?php endif; ?>
    <?php else : ?>
        <title><?php wp_title('|', true, 'right'); ?><?php bloginfo('name'); ?></title>
    <?php endif; ?>
   <!-- End SEO logic -->
  <?php get_template_part('favicon'); ?>
  <?php wp_head(); ?>
  <script src="https://cdn.tailwindcss.com"></script>
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
