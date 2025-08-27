<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
  <meta charset="<?php bloginfo('charset'); ?>">
  <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- SEO and Meta Tags -->
    <?php
    // --- Basic Meta ---
    $title = '';
    $description = '';
    $canonical_url = get_permalink();

    if (is_front_page() || is_home()) {
        $title = get_bloginfo('name') . ' | Automated Legal & Tax Structuring';
        $description = 'AssetArc provides automated workflows for asset protection, tax efficiency, and corporate structuring. Generate compliant legal documents with human review.';
        $canonical_url = home_url('/');
    } elseif (is_singular()) { // For single posts, pages, and custom post types
        $title = get_the_title() . ' | ' . get_bloginfo('name');
        if (has_excerpt()) {
            $description = get_the_excerpt();
        } else {
            $description = wp_trim_words(strip_shortcodes(strip_tags(get_the_content())), 25, '...');
        }
    } else { // For archives, search results, etc.
        $title = wp_title('|', false, 'right') . get_bloginfo('name');
        $description = get_the_archive_description();
        if (is_category() || is_tag() || is_tax()) {
            $canonical_url = get_term_link(get_queried_object());
        } elseif (is_post_type_archive()) {
            $canonical_url = get_post_type_archive_link(get_post_type());
        } else {
            $canonical_url = home_url('/'); // Fallback for other archive types
        }
    }

    // --- Image for Open Graph ---
    $og_image_url = '';
    if (is_singular() && has_post_thumbnail()) {
        $og_image_url = get_the_post_thumbnail_url(get_the_ID(), 'full');
    } else {
        // Fallback image - using the logo
        $og_image_url = home_url('/Photos/Logo.png');
    }

    // --- OG Type ---
    $og_type = is_singular() ? 'article' : 'website';

    ?>
    <title><?php echo esc_html($title); ?></title>
    <meta name="description" content="<?php echo esc_attr(strip_tags($description)); ?>">
    <link rel="canonical" href="<?php echo esc_url($canonical_url); ?>" />

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="<?php echo esc_attr($og_type); ?>" />
    <meta property="og:title" content="<?php echo esc_html($title); ?>" />
    <meta property="og:description" content="<?php echo esc_attr(strip_tags($description)); ?>" />
    <meta property="og:image" content="<?php echo esc_url($og_image_url); ?>" />
    <meta property="og:url" content="<?php echo esc_url($canonical_url); ?>" />
    <meta property="og:site_name" content="<?php bloginfo('name'); ?>" />

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="<?php echo esc_html($title); ?>">
    <meta name="twitter:description" content="<?php echo esc_attr(strip_tags($description)); ?>">
    <meta name="twitter:image" content="<?php echo esc_url($og_image_url); ?>">
    <!-- End SEO and Meta Tags -->
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
