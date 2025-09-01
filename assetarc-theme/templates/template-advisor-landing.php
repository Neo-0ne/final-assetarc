<?php
/*
Template Name: Advisor Landing Page
*/
get_header(); ?>

<main class="advisor-page bg-black text-white py-16 px-6 lg:px-24">
    <div class="max-w-screen-xl mx-auto text-center">
        <?php if( get_field('advisor_headline') ): ?>
            <h1 class="text-4xl lg:text-5xl font-semibold mb-6 text-gold"><?php the_field('advisor_headline'); ?></h1>
        <?php endif; ?>
        <?php if( get_field('advisor_intro') ): ?>
            <p class="text-lg text-gray-300 max-w-3xl mx-auto mb-12">
                <?php the_field('advisor_intro'); ?>
            </p>
        <?php endif; ?>
    </div>

    <div class="max-w-screen-xl mx-auto grid md:grid-cols-2 gap-12 items-center mb-16">
        <div>
            <?php
            $advisor_image = get_field('advisor_image');
            if( $advisor_image ): ?>
                <img src="<?php echo esc_url($advisor_image['url']); ?>" alt="<?php echo esc_attr($advisor_image['alt']); ?>" class="rounded-lg shadow-lg">
            <?php endif; ?>
        </div>
        <?php if( have_rows('advisor_features') ): ?>
            <div class="space-y-8">
                <?php while( have_rows('advisor_features') ): the_row(); ?>
                    <div>
                        <h3 class="text-2xl font-bold text-gold mb-3"><?php the_sub_field('feature_title'); ?></h3>
                        <p class="text-gray-400"><?php the_sub_field('feature_description'); ?></p>
                    </div>
                <?php endwhile; ?>
            </div>
        <?php endif; ?>
    </div>

    <div class="text-center">
        <?php
        $advisor_cta = get_field('advisor_cta');
        if( $advisor_cta ): ?>
            <a href="<?php echo esc_url($advisor_cta['url']); ?>" class="btn btn-gold"><?php echo esc_html($advisor_cta['title']); ?></a>
        <?php endif; ?>
    </div>
</main>

<?php get_footer(); ?>
