<?php
/*
Template Name: Testimonials Page
*/
get_header(); ?>

<main class="p-8 text-white max-w-4xl mx-auto">
  <?php if( get_field('testimonials_headline') ): ?>
    <h1 class="text-4xl font-bold mb-6"><?php the_field('testimonials_headline'); ?></h1>
  <?php endif; ?>

  <?php if( have_rows('testimonial_items') ): ?>
    <div class="space-y-8">
      <?php while( have_rows('testimonial_items') ): the_row(); ?>
        <div class="bg-gray-800 p-6 rounded shadow">
          <p class="italic">“<?php the_sub_field('quote'); ?>”</p>
          <p class="text-gold mt-2 font-semibold">— <?php the_sub_field('attribution'); ?></p>
        </div>
      <?php endwhile; ?>
    </div>
  <?php endif; ?>
</main>

<?php get_footer(); ?>
