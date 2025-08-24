<?php
/*
Template for displaying podcast archive.
*/
get_header(); ?>

<main class="p-8 text-white max-w-6xl mx-auto">
    <div class="text-center mb-16">
        <h1 class="text-4xl font-bold mb-4">Podcast</h1>
        <p class="text-lg text-gray-400">"Unseen Shields": Expert insights on strategic structuring.</p>
    </div>

    <?php if (have_posts()) : ?>
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <?php while (have_posts()) : the_post(); ?>
                <div class="bg-gray-800 p-6 rounded-lg shadow-lg">
                    <h2 class="text-2xl text-gold mb-3"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
                    <div class="text-gray-300">
                        <?php the_excerpt(); ?>
                    </div>
                </div>
            <?php endwhile; ?>
        </div>
    <?php else : ?>
        <p class="text-center">No podcast episodes found.</p>
    <?php endif; ?>
</main>

<?php get_footer(); ?>
