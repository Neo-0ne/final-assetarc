<?php
/*
Template Name: About Page
*/
get_header(); ?>

<main class="p-8 text-white max-w-5xl mx-auto">
  <?php if( get_field('about_page_headline') ): ?>
    <h1 class="text-4xl font-bold mb-8 text-center text-gold"><?php the_field('about_page_headline'); ?></h1>
  <?php endif; ?>

  <section class="grid md:grid-cols-3 gap-12 items-center">
    <div class="md:col-span-1">
      <?php
      $founder_image = get_field('founder_image');
      if( $founder_image ): ?>
        <img src="<?php echo esc_url($founder_image['url']); ?>" alt="<?php echo esc_attr($founder_image['alt']); ?>" class="rounded-lg shadow-lg w-full">
      <?php endif; ?>
    </div>
    <div class="md:col-span-2">
      <?php if( get_field('founder_note_headline') ): ?>
        <h2 class="text-3xl font-semibold mb-4"><?php the_field('founder_note_headline'); ?></h2>
      <?php endif; ?>
      <?php if( get_field('founder_note_content') ): ?>
        <div class="prose prose-invert text-gray-300"><?php the_field('founder_note_content'); ?></div>
      <?php endif; ?>
      <?php if( get_field('founder_name') ): ?>
        <p class="mt-4 font-semibold text-gold">- <?php the_field('founder_name'); ?></p>
      <?php endif; ?>
    </div>
  </section>

  <section class="mt-16">
    <?php if( get_field('why_section_headline') ): ?>
      <h2 class="text-3xl font-semibold mb-6 text-center"><?php the_field('why_section_headline'); ?></h2>
    <?php endif; ?>
    <?php if( have_rows('why_section_cards') ): ?>
      <div class="grid md:grid-cols-2 gap-8 text-center">
        <?php while( have_rows('why_section_cards') ): the_row(); ?>
          <div class="card p-6">
            <h3 class="text-xl font-bold text-gold mb-2"><?php the_sub_field('card_title'); ?></h3>
            <p><?php the_sub_field('card_content'); ?></p>
          </div>
        <?php endwhile; ?>
      </div>
    <?php endif; ?>
  </section>

  <section class="mt-16">
    <?php if( get_field('team_section_headline') ): ?>
      <h2 class="text-3xl font-semibold mb-6 text-center"><?php the_field('team_section_headline'); ?></h2>
    <?php endif; ?>
    <?php if( have_rows('team_members') ): ?>
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        <?php while( have_rows('team_members') ): the_row();
          $member_photo = get_sub_field('member_photo');
        ?>
          <div class="team-card text-center">
            <?php if( $member_photo ): ?>
              <img src="<?php echo esc_url($member_photo['url']); ?>" alt="<?php echo esc_attr($member_photo['alt']); ?>" class="rounded-full w-32 h-32 mx-auto mb-4 border-2 border-gold">
            <?php endif; ?>
            <h4 class="text-xl font-semibold"><?php the_sub_field('member_name'); ?></h4>
            <p class="text-gold"><?php the_sub_field('member_title'); ?></p>
            <p class="text-sm text-gray-400 mt-2"><?php the_sub_field('member_blurb'); ?></p>
          </div>
        <?php endwhile; ?>
      </div>
    <?php endif; ?>
  </section>
</main>

<?php get_footer(); ?>
