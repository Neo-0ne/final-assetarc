<?php
/*
Template for displaying video archive.
*/
get_header(); ?>

<main class="p-8 text-white max-w-6xl mx-auto">
    <div class="text-center mb-16">
        <h1 class="text-4xl font-bold mb-4">Videos</h1>
        <p class="text-lg text-gray-400">Tutorials and explainers on complex structuring topics.</p>
    </div>

    <?php if (have_posts()) : ?>
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <?php while (have_posts()) : the_post(); ?>
                <div class="bg-gray-800 p-6 rounded-lg shadow-lg">
                    <!-- Placeholder for video thumbnail -->
                    <a href="<?php the_permalink(); ?>">
                        <img src="<?php echo get_template_directory_uri(); ?>/assets/video-placeholder.jpg" alt="<?php the_title_attribute(); ?>" class="mb-4 rounded-lg">
                    </a>
                    <h2 class="text-2xl text-gold mb-3"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
                </div>
            <?php endwhile; ?>
        </div>
    <?php else : ?>
        <p class="text-center">No videos found.</p>
    <?php endif; ?>
</main>

<?php get_footer(); ?>
