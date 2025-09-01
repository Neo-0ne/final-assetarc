<?php get_header(); ?>

<main class="p-8 text-white">
  <h1 class="text-3xl font-bold mb-4">Search Results for: "<?php echo get_search_query(); ?>"</h1>

  <?php if (have_posts()) : ?>
    <ul class="space-y-4">
      <?php while (have_posts()) : the_post(); ?>
        <li>
          <a href="<?php the_permalink(); ?>" class="text-gold text-xl hover:underline"><?php the_title(); ?></a>
          <p class="text-sm"><?php echo get_the_excerpt(); ?></p>
        </li>
      <?php endwhile; ?>
    </ul>
  <?php else : ?>
    <p>No results found. Please try again.</p>
  <?php endif; ?>
</main>

<?php get_footer(); ?>
