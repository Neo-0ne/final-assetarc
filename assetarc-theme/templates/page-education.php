<?php
/*
Template Name: Education Hub
*/
get_header(); ?>

<main class="p-8 text-white max-w-6xl mx-auto">
    <div class="text-center mb-16">
        <?php if( get_field('education_headline') ): ?>
            <h1 class="text-4xl font-bold mb-4"><?php the_field('education_headline'); ?></h1>
        <?php endif; ?>
        <?php if( get_field('education_intro') ): ?>
            <p class="text-lg text-gray-400"><?php the_field('education_intro'); ?></p>
        <?php endif; ?>
    </div>

    <section class="space-y-12">
        <!-- Guides Section -->
        <div>
            <?php if( get_field('guides_headline') ): ?>
                <h2 class="text-3xl font-semibold text-gold mb-6 border-b border-gold pb-2"><?php the_field('guides_headline'); ?></h2>
            <?php endif; ?>
            <?php if( get_field('guides_content') ): ?>
                <div class="text-gray-300"><?php the_field('guides_content'); ?></div>
            <?php endif; ?>
        </div>

        <!-- Webinars Section -->
        <div>
            <?php if( get_field('webinars_headline') ): ?>
                <h2 class="text-3xl font-semibold text-gold mb-6 border-b border-gold pb-2"><?php the_field('webinars_headline'); ?></h2>
            <?php endif; ?>
            <?php if( get_field('webinars_content') ): ?>
                <div class="text-gray-300"><?php the_field('webinars_content'); ?></div>
            <?php endif; ?>
        </div>

        <!-- FAQ Section -->
        <div>
            <?php if( get_field('faq_headline') ): ?>
                <h2 class="text-3xl font-semibold text-gold mb-6 border-b border-gold pb-2"><?php the_field('faq_headline'); ?></h2>
            <?php endif; ?>
            <?php if( have_rows('faq_items') ): ?>
                <div class="space-y-4">
                    <?php while( have_rows('faq_items') ): the_row(); ?>
                        <div class="faq-item">
                            <h4 class="text-xl font-semibold"><?php the_sub_field('question'); ?></h4>
                            <div class="text-gray-400"><?php the_sub_field('answer'); ?></div>
                        </div>
                    <?php endwhile; ?>
                </div>
            <?php endif; ?>
        </div>
    </section>
</main>

<?php get_footer(); ?>
