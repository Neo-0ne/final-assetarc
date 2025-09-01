<?php
/*
Template for displaying a single podcast.
*/
get_header(); ?>

<main class="p-8 text-white max-w-4xl mx-auto">
    <?php if (have_posts()) : while (have_posts()) : the_post(); ?>
        <article>
            <h1 class="text-4xl font-bold mb-4"><?php the_title(); ?></h1>

            <!-- Placeholder for the embedded audio player -->
            <div class="podcast-player bg-gray-800 p-6 rounded-lg mb-8">
                <p class="text-center">Audio player will be embedded here.</p>
            </div>

            <div class="prose prose-invert max-w-none">
                <?php the_content(); ?>
            </div>
        </article>
    <?php endwhile; endif; ?>
</main>

<?php get_footer(); ?>
