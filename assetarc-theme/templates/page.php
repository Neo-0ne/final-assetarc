<?php
// page.php - Template for static pages
get_header(); ?>

<main class="container mx-auto py-16 text-white">
    <?php if (have_posts()) : while (have_posts()) : the_post(); ?>
        <article class="prose lg:prose-xl max-w-3xl mx-auto">
            <h1 class="text-4xl font-bold mb-4"><?php the_title(); ?></h1>
            <?php the_content(); ?>
        </article>
    <?php endwhile; endif; ?>
</main>

<?php get_footer(); ?>
