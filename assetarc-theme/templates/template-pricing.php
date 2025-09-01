<?php
/**
 * Template Name: Pricing
 */

get_header();
?>

<main class="pricing-page bg-black text-white py-16 px-6 lg:px-24">
    <div class="max-w-screen-xl mx-auto text-center">
        <?php if( get_field('pricing_headline') ): ?>
            <h1 class="text-4xl lg:text-5xl font-semibold mb-6 text-gold"><?php the_field('pricing_headline'); ?></h1>
        <?php endif; ?>
        <?php if( get_field('pricing_intro') ): ?>
            <p class="text-lg text-gray-300 max-w-3xl mx-auto mb-12">
                <?php the_field('pricing_intro'); ?>
            </p>
        <?php endif; ?>

        <?php if( have_rows('pricing_tiers') ): ?>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <?php while( have_rows('pricing_tiers') ): the_row();
                    $tier_cta = get_sub_field('tier_cta');
                    $is_featured = get_sub_field('is_featured');
                ?>
                    <div class="card <?php if($is_featured){ echo 'bg-neutral-800 border-2 border-gold'; } else { echo 'bg-neutral-900'; } ?> p-8 rounded-lg flex flex-col">
                        <h3 class="text-2xl font-bold text-gold mb-4"><?php the_sub_field('tier_name'); ?></h3>
                        <p class="text-3xl font-bold mb-4"><?php the_sub_field('tier_price'); ?></p>
                        <?php if( have_rows('tier_features') ): ?>
                            <ul class="text-left space-y-2 mb-6 flex-grow text-gray-400">
                                <?php while( have_rows('tier_features') ): the_row(); ?>
                                    <li class="flex items-center"><span class="text-gold mr-2">&#10003;</span> <?php the_sub_field('feature_item'); ?></li>
                                <?php endwhile; ?>
                            </ul>
                        <?php endif; ?>
                        <?php if( $tier_cta ): ?>
                            <a href="<?php echo esc_url($tier_cta['url']); ?>" class="btn <?php if($is_featured){ echo 'btn-gold'; } else { echo 'btn-outline-gold'; } ?> mt-auto"><?php echo esc_html($tier_cta['title']); ?></a>
                        <?php endif; ?>
                    </div>
                <?php endwhile; ?>
            </div>
        <?php endif; ?>

        <?php if( get_field('pricing_surcharges') ): ?>
            <div class="mt-12 text-sm text-gray-500">
                <p><?php the_field('pricing_surcharges'); ?></p>
            </div>
        <?php endif; ?>
    </div>
</main>

<?php
get_footer();
?>
