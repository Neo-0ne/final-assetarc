<?php
/**
 * Template Name: Services
 */

get_header();
?>

<main class="services-page bg-black text-white py-16 px-6 lg:px-24">
    <div class="max-w-screen-xl mx-auto text-center">
        <?php if( get_field('services_headline') ): ?>
            <h1 class="text-4xl lg:text-5xl font-semibold mb-6 text-gold"><?php the_field('services_headline'); ?></h1>
        <?php endif; ?>
        <?php if( get_field('services_intro') ): ?>
            <p class="text-lg text-gray-300 max-w-3xl mx-auto mb-12">
                <?php the_field('services_intro'); ?>
            </p>
        <?php endif; ?>

        <?php if( have_rows('service_cards') ): ?>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                <?php while( have_rows('service_cards') ): the_row();
                    $service_cta = get_sub_field('service_cta_link');
                ?>
                    <div class="bg-neutral-900 rounded-lg p-6 text-left">
                        <h3 class="text-2xl font-bold text-gold mb-3"><?php the_sub_field('service_title'); ?></h3>
                        <p class="text-gray-400 mb-4"><?php the_sub_field('service_description'); ?></p>
                        <?php if( $service_cta ): ?>
                            <a href="<?php echo esc_url($service_cta['url']); ?>" class="btn btn-outline-gold"><?php echo esc_html($service_cta['title']); ?></a>
                        <?php endif; ?>
                    </div>
                <?php endwhile; ?>
            </div>
        <?php endif; ?>
    </div>
</main>

<?php
get_footer();
?>
