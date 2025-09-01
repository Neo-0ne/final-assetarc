<?php
/**
 * Template Name: Consultation
 */

get_header();
?>

<main class="consultation-page bg-black text-white py-16 px-6 lg:px-24">
    <div class="max-w-screen-xl mx-auto">
        <?php if( get_field('consultation_headline') ): ?>
            <h1 class="text-4xl lg:text-5xl font-semibold text-gold mb-10"><?php the_field('consultation_headline'); ?></h1>
        <?php endif; ?>

        <section class="mb-10">
            <?php if( get_field('consultation_intro') ): ?>
                <p class="text-lg text-gray-300 max-w-2xl">
                    <?php the_field('consultation_intro'); ?>
                </p>
            <?php endif; ?>
        </section>

        <?php if( have_rows('consultation_paths') ): ?>
            <div class="bg-gray-900 p-6 rounded-xl shadow mb-16">
                <h2 class="text-2xl text-gold font-semibold mb-4"><?php the_field('paths_headline'); ?></h2>
                <ul class="space-y-6 text-gray-300">
                    <?php while( have_rows('consultation_paths') ): the_row(); ?>
                        <li>✔ <?php the_sub_field('path_item'); ?></li>
                    <?php endwhile; ?>
                </ul>
            </div>
        <?php endif; ?>

        <section class="bg-gray-950 p-6 rounded-xl shadow-xl mb-16">
            <?php if( get_field('schedule_headline') ): ?>
                <h2 class="text-xl text-white font-semibold mb-4">📅 <?php the_field('schedule_headline'); ?></h2>
            <?php endif; ?>
            <?php if( get_field('calendly_url') ): ?>
                <div class="calendly-inline-widget" data-url="<?php the_field('calendly_url'); ?>" style="min-width:320px;height:700px;"></div>
                <script type="text/javascript" src="https://assets.calendly.com/assets/external/widget.js" async></script>
            <?php endif; ?>
        </section>

        <section class="text-center mt-20">
            <?php if( get_field('token_cta_headline') ): ?>
                <h2 class="text-2xl lg:text-3xl font-bold text-white mb-4"><?php the_field('token_cta_headline'); ?></h2>
            <?php endif; ?>
            <?php if( get_field('token_cta_text') ): ?>
                <p class="text-gray-400 mb-6 max-w-2xl mx-auto"><?php the_field('token_cta_text'); ?></p>
            <?php endif; ?>
            <?php
            $token_cta_link = get_field('token_cta_link');
            if( $token_cta_link ): ?>
                <a href="<?php echo esc_url($token_cta_link['url']); ?>" class="inline-block bg-gold text-black font-semibold px-6 py-3 rounded-full hover:bg-yellow-400 transition">
                    <?php echo esc_html($token_cta_link['title']); ?>
                </a>
            <?php endif; ?>
        </section>

    </div>
</main>

<?php
get_footer();
?>
