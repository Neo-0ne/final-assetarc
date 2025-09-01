<?php get_header(); ?>

<main class="homepage-content text-white bg-black">

  <!-- Hero Section with Video -->
  <section class="hero-section py-20 px-6">
    <div class="container mx-auto grid md:grid-cols-2 gap-8 items-center">
      <div class="hero-left text-center md:text-left">
        <?php if( get_field('hero_headline') ): ?>
          <h1 class="text-4xl md:text-6xl font-semibold mb-4"><?php the_field('hero_headline'); ?></h1>
        <?php endif; ?>
        <?php if( get_field('hero_subheading') ): ?>
          <p class="text-base md:text-lg text-gray-300 max-w-xl mx-auto md:mx-0 mb-6"><?php the_field('hero_subheading'); ?></p>
        <?php endif; ?>
        <?php
        $hero_primary_cta = get_field('hero_primary_cta');
        if( $hero_primary_cta ): ?>
          <a href="<?php echo esc_url($hero_primary_cta['url']); ?>" class="btn btn-gold"><?php echo esc_html($hero_primary_cta['title']); ?></a>
        <?php endif; ?>
        <?php
        $hero_secondary_cta = get_field('hero_secondary_cta');
        if( $hero_secondary_cta ): ?>
          <a href="<?php echo esc_url($hero_secondary_cta['url']); ?>" class="btn btn-outline ml-4"><?php echo esc_html($hero_secondary_cta['title']); ?></a>
        <?php endif; ?>
      </div>
      <div class="hero-right mt-8 md:mt-0">
        <div class="hero-video-wrapper">
          <?php if( get_field('hero_video') ): ?>
            <video autoplay muted loop playsinline class="hero-video rounded-lg shadow-lg">
              <source src="<?php the_field('hero_video'); ?>" type="video/mp4">
            </video>
          <?php endif; ?>
        </div>
      </div>
    </div>
  </section>

  <!-- How It Works Section -->
  <section id="how-it-works" class="how-it-works-section py-20 px-6 bg-neutral-950">
    <div class="container mx-auto text-center">
      <?php if( get_field('how_it_works_headline') ): ?>
        <h2 class="text-3xl font-semibold mb-12"><?php the_field('how_it_works_headline'); ?></h2>
      <?php endif; ?>
      <?php if( have_rows('how_it_works_steps') ): ?>
        <div class="grid md:grid-cols-4 gap-8">
          <?php while( have_rows('how_it_works_steps') ): the_row(); ?>
            <div class="step-card">
              <div class="step-number text-gold text-4xl font-bold mb-4"><?php echo get_row_index(); ?></div>
              <h3 class="text-xl font-semibold mb-2"><?php the_sub_field('step_title'); ?></h3>
              <p class="text-gray-400"><?php the_sub_field('step_description'); ?></p>
            </div>
          <?php endwhile; ?>
        </div>
      <?php endif; ?>
    </div>
  </section>

  <!-- Trust Strip -->
  <section class="trust-strip bg-neutral-900 py-8 text-center">
    <div class="container mx-auto">
      <?php if( get_field('trust_strip_text') ): ?>
        <p class="text-sm text-gray-400 tracking-wide uppercase mb-4"><?php the_field('trust_strip_text'); ?></p>
      <?php endif; ?>
      <?php if( have_rows('trust_strip_badges') ): ?>
        <div class="flex justify-center space-x-8">
          <?php while( have_rows('trust_strip_badges') ): the_row(); ?>
            <span class="text-xs font-semibold text-gold"><?php the_sub_field('badge_text'); ?></span>
          <?php endwhile; ?>
        </div>
      <?php endif; ?>
    </div>
  </section>

  <!-- Choose Your Path Section -->
  <section class="choose-your-path-section py-20 px-6">
    <div class="container mx-auto text-center">
      <?php if( get_field('path_section_headline') ): ?>
        <h2 class="text-3xl font-semibold mb-12"><?php the_field('path_section_headline'); ?></h2>
      <?php endif; ?>
      <div class="grid md:grid-cols-2 gap-8">
        <div class="path-card bg-neutral-800 p-8 rounded-lg text-center">
          <?php if( get_field('client_path_title') ): ?>
            <h3 class="text-2xl font-semibold mb-4"><?php the_field('client_path_title'); ?></h3>
          <?php endif; ?>
          <?php if( get_field('client_path_description') ): ?>
            <p class="text-gray-400 mb-6"><?php the_field('client_path_description'); ?></p>
          <?php endif; ?>
          <?php
          $client_path_cta = get_field('client_path_cta');
          if( $client_path_cta ): ?>
            <a href="<?php echo esc_url($client_path_cta['url']); ?>" class="btn btn-gold"><?php echo esc_html($client_path_cta['title']); ?></a>
          <?php endif; ?>
        </div>
        <div class="path-card bg-neutral-800 p-8 rounded-lg text-center">
          <?php if( get_field('advisor_path_title') ): ?>
            <h3 class="text-2xl font-semibold mb-4"><?php the_field('advisor_path_title'); ?></h3>
          <?php endif; ?>
          <?php if( get_field('advisor_path_description') ): ?>
            <p class="text-gray-400 mb-6"><?php the_field('advisor_path_description'); ?></p>
          <?php endif; ?>
          <?php
          $advisor_path_cta = get_field('advisor_path_cta');
          if( $advisor_path_cta ): ?>
            <a href="<?php echo esc_url($advisor_path_cta['url']); ?>" class="btn btn-outline"><?php echo esc_html($advisor_path_cta['title']); ?></a>
          <?php endif; ?>
        </div>
      </div>
    </div>
  </section>

  <!-- Featured Workflows Section -->
  <section class="featured-workflows-section py-20 px-6 bg-neutral-950">
    <div class="container mx-auto text-center">
      <?php if( get_field('workflows_headline') ): ?>
        <h2 class="text-3xl font-semibold mb-12"><?php the_field('workflows_headline'); ?></h2>
      <?php endif; ?>
      <?php if( have_rows('workflows') ): ?>
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8">
          <?php while( have_rows('workflows') ): the_row(); ?>
            <div class="bot-card bg-neutral-800 p-6 rounded-lg">
              <h4 class="font-semibold text-lg"><?php the_sub_field('workflow_title'); ?></h4>
              <p class="text-xs text-gray-400 mt-1"><?php the_sub_field('workflow_description'); ?></p>
            </div>
          <?php endwhile; ?>
        </div>
      <?php endif; ?>
    </div>
  </section>

  <!-- Feature Cards Section Removed -->

  <!-- Lead Magnet Section -->
  <section class="lead-magnet-section py-20 px-6">
    <div class="container mx-auto text-center bg-neutral-800 p-12 rounded-lg">
      <?php if( get_field('lead_magnet_headline') ): ?>
        <h2 class="text-3xl font-semibold mb-4"><?php the_field('lead_magnet_headline'); ?></h2>
      <?php endif; ?>
      <?php if( get_field('lead_magnet_description') ): ?>
        <p class="text-gray-400 mb-8"><?php the_field('lead_magnet_description'); ?></p>
      <?php endif; ?>
      <form id="lead-magnet-form" class="max-w-md mx-auto" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" method="post">
        <input type="hidden" name="action" value="assetarc_newsletter_signup">
        <div class="flex items-center">
          <input type="email" name="newsletter_email" class="w-full p-3 rounded-l-md bg-neutral-700 text-white border-neutral-600" placeholder="Enter your email" required>
          <button type="submit" class="btn btn-gold rounded-r-md">Get Access</button>
        </div>
        <p class="text-xs text-gray-500 mt-2">Join our mailing list to receive your starter pack.</p>
      </form>
    </div>
  </section>

  <!-- Compliance & Security Section -->
  <section class="compliance-security-section py-20 px-6">
    <div class="container mx-auto grid md:grid-cols-2 gap-12 items-center">
      <div>
        <?php if( get_field('compliance_headline') ): ?>
          <h3 class="text-2xl font-semibold mb-4"><?php the_field('compliance_headline'); ?></h3>
        <?php endif; ?>
        <?php if( have_rows('compliance_points') ): ?>
          <ul class="list-disc list-inside text-gray-400 space-y-2">
            <?php while( have_rows('compliance_points') ): the_row(); ?>
              <li><?php the_sub_field('point'); ?></li>
            <?php endwhile; ?>
          </ul>
        <?php endif; ?>
      </div>
      <div>
        <?php if( get_field('security_headline') ): ?>
          <h3 class="text-2xl font-semibold mb-4"><?php the_field('security_headline'); ?></h3>
        <?php endif; ?>
        <?php if( have_rows('security_points') ): ?>
          <ul class="list-disc list-inside text-gray-400 space-y-2">
            <?php while( have_rows('security_points') ): the_row(); ?>
              <li><?php the_sub_field('point'); ?></li>
            <?php endwhile; ?>
          </ul>
        <?php endif; ?>
      </div>
    </div>
  </section>

  <!-- Social Proof Section -->
  <section class="testimonials-section py-20 px-6 bg-neutral-950">
    <div class="container mx-auto text-center">
      <?php if( get_field('social_proof_headline') ): ?>
        <h2 class="text-3xl font-semibold mb-12"><?php the_field('social_proof_headline'); ?></h2>
      <?php endif; ?>
      <?php if( have_rows('testimonials') ): ?>
        <div class="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          <?php while( have_rows('testimonials') ): the_row(); ?>
            <div class="testimonial-card bg-neutral-800 p-6 rounded-lg">
              <h4 class="font-semibold text-gold mb-2"><?php the_sub_field('testimonial_title'); ?></h4>
              <p class="text-gray-300"><?php the_sub_field('testimonial_quote'); ?></p>
              <?php if( get_sub_field('testimonial_attribution') ): ?>
                <p class="text-xs text-gray-500 mt-3">– <?php the_sub_field('testimonial_attribution'); ?></p>
              <?php endif; ?>
            </div>
          <?php endwhile; ?>
        </div>
      <?php endif; ?>
    </div>
  </section>

  <!-- Pricing Snapshot Section -->
  <section class="pricing-snapshot-section py-20 px-6">
    <div class="container mx-auto text-center">
      <?php if( get_field('pricing_snapshot_headline') ): ?>
        <h2 class="text-3xl font-semibold mb-12"><?php the_field('pricing_snapshot_headline'); ?></h2>
      <?php endif; ?>
      <?php if( have_rows('pricing_tiers') ): ?>
        <div class="grid md:grid-cols-3 gap-8">
          <?php while( have_rows('pricing_tiers') ): the_row();
            $tier_cta = get_sub_field('tier_cta');
          ?>
            <div class="pricing-card bg-neutral-800 p-8 rounded-lg">
              <h4 class="text-xl font-semibold text-gold"><?php the_sub_field('tier_name'); ?></h4>
              <p class="text-gray-400"><?php the_sub_field('tier_description'); ?></p>
              <?php if( $tier_cta ): ?>
                <a href="<?php echo esc_url($tier_cta['url']); ?>" class="text-gold mt-4 inline-block"><?php echo esc_html($tier_cta['title']); ?></a>
              <?php endif; ?>
            </div>
          <?php endwhile; ?>
        </div>
      <?php endif; ?>
      <?php if( get_field('pricing_snapshot_note') ): ?>
        <p class="text-xs text-gray-500 mt-8"><?php the_field('pricing_snapshot_note'); ?></p>
      <?php endif; ?>
    </div>
  </section>

  <!-- Resource Highlights Section -->
  <section class="resource-highlights-section py-20 px-6 bg-neutral-950">
    <div class="container mx-auto text-center">
      <?php if( get_field('resources_headline') ): ?>
        <h2 class="text-3xl font-semibold mb-12"><?php the_field('resources_headline'); ?></h2>
      <?php endif; ?>
      <?php if( have_rows('resource_highlights') ): ?>
        <div class="grid md:grid-cols-3 gap-8">
          <?php while( have_rows('resource_highlights') ): the_row(); ?>
            <div class="resource-card">
              <h4 class="text-xl font-semibold text-gold"><?php the_sub_field('resource_title'); ?></h4>
              <p class="text-gray-400"><?php the_sub_field('resource_description'); ?></p>
            </div>
          <?php endwhile; ?>
        </div>
      <?php endif; ?>
      <?php
      $resources_cta = get_field('resources_cta');
      if( $resources_cta ): ?>
        <a href="<?php echo esc_url($resources_cta['url']); ?>" class="btn btn-outline mt-12"><?php echo esc_html($resources_cta['title']); ?></a>
      <?php endif; ?>
    </div>
  </section>

  <!-- Final CTA Strip -->
  <section class="final-cta-section py-16">
    <div class="container mx-auto text-center">
      <?php if( get_field('final_cta_headline') ): ?>
        <h2 class="text-3xl font-semibold mb-4"><?php the_field('final_cta_headline'); ?></h2>
      <?php endif; ?>
      <?php
      $final_cta_primary = get_field('final_cta_primary');
      if( $final_cta_primary ): ?>
        <a href="<?php echo esc_url($final_cta_primary['url']); ?>" class="btn btn-gold mr-4"><?php echo esc_html($final_cta_primary['title']); ?></a>
      <?php endif; ?>
      <?php
      $final_cta_secondary = get_field('final_cta_secondary');
      if( $final_cta_secondary ): ?>
        <a href="<?php echo esc_url($final_cta_secondary['url']); ?>" class="btn btn-outline"><?php echo esc_html($final_cta_secondary['title']); ?></a>
      <?php endif; ?>
    </div>
  </section>

</main>

<?php get_footer(); ?>
