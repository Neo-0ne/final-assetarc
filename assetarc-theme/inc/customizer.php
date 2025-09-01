<?php
// customizer.php – for future custom controls

function assetarc_customize_register($wp_customize) {
    // Custom color scheme (Optional)
    $wp_customize->add_setting('theme_color_primary', array(
        'default'   => '#FFD700',
        'transport' => 'refresh',
    ));

    $wp_customize->add_control(new WP_Customize_Color_Control($wp_customize, 'theme_color_primary', array(
        'label'    => __('Primary Gold Color', 'assetarc'),
        'section'  => 'colors',
        'settings' => 'theme_color_primary',
    )));
}
add_action('customize_register', 'assetarc_customize_register');
