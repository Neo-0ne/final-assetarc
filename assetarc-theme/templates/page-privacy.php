<?php
/*
Template Name: Privacy Policy
*/
get_header(); ?>

<main class="p-8 text-white max-w-4xl mx-auto">
  <?php if( get_field('privacy_headline') ): ?>
    <h1 class="text-4xl font-bold mb-6"><?php the_field('privacy_headline'); ?></h1>
  <?php endif; ?>

  <?php if( get_field('privacy_content') ): ?>
    <section class="prose prose-invert max-w-none text-sm leading-7">
      <?php the_field('privacy_content'); ?>
    </section>
  <?php endif; ?>
</main>

<?php get_footer(); ?>
