<?php get_header(); ?>

<main class="p-8 text-white">
  <h1 class="text-3xl font-bold mb-4"><?php the_archive_title(); ?></h1>

  <?php if (have_posts()) : ?>
    <ul class="space-y-6">
      <?php while (have_posts()) : the_post(); ?>
        <li>
          <a href="<?php the_permalink(); ?>" class="text-gold text-2xl hover:underline"><?php the_title(); ?></a>
          <p class="text-sm"><?php the_excerpt(); ?></p>
        </li>
      <?php endwhile; ?>
    </ul>
    <div class="mt-6">
      <?php the_posts_navigation(); ?>
    </div>
  <?php else : ?>
    <p>No posts available in this archive.</p>
  <?php endif; ?>
</main>

<?php get_footer(); ?>
