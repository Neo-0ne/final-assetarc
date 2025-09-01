<?php
/*
Template for displaying a single video.
*/
get_header(); ?>

<main class="p-8 text-white max-w-4xl mx-auto">
    <?php if (have_posts()) : while (have_posts()) : the_post(); ?>
        <article>
            <h1 class="text-4xl font-bold mb-8"><?php the_title(); ?></h1>

            <!-- Placeholder for the embedded video player -->
            <div class="video-player-wrapper mb-8">
                <div class="aspect-w-16 aspect-h-9">
                    <iframe src="https://www.youtube.com/embed/placeholder" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                </div>
            </div>

            <div class="prose prose-invert max-w-none">
                <?php the_content(); ?>
            </div>
        </article>
    <?php endwhile; endif; ?>
</main>

<?php get_footer(); ?>
