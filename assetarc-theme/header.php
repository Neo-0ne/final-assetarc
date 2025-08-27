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
      // Attempt to get white-label brand assets
      $brand_assets = get_assetarc_brand_assets();

      if (isset($brand_assets['logo_url']) && !empty($brand_assets['logo_url'])) {
          // If a white-label logo exists, display it
          echo '<a href="' . esc_url(home_url('/')) . '" rel="home">';
          echo '<img src="' . esc_url($brand_assets['logo_url']) . '" alt="' . esc_attr($brand_assets['name']) . ' Logo" style="height: 60px; width: auto;">';
          echo '</a>';
      } else {
          // Fallback to the default WordPress custom logo or site title
          if (has_custom_logo()) {
              the_custom_logo();
          } else {
              echo '<a href="' . esc_url(home_url('/')) . '" rel="home">';
              echo '<img src="/Photos/Logo.png" alt="' . esc_attr(get_bloginfo('name')) . ' Logo" style="height: 60px; width: auto;">';
              echo '</a>';
          }
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
