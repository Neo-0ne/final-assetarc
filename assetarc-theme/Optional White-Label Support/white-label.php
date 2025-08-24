<?php
// white-label.php

function get_advisor_branding() {
    $branding = [
        'default' => [
            'logo' => get_template_directory_uri() . '/assets/logo-default.svg',
            'color' => '#FFD700',
            'company_name' => 'AssetArc',
            'tagline' => 'Protect. Structure. Endure.',
        ],
        'advisor123' => [
            'logo' => get_template_directory_uri() . '/assets/logo-advisor123.svg',
            'color' => '#0099CC',
            'company_name' => 'Summit Wealth Advisors',
            'tagline' => 'Global Wealth Structuring',
        ],
        // Add more advisor mappings as needed...
    ];

    // Option 1: Detect by subfolder (e.g. /advisor123/)
    $request_uri = $_SERVER['REQUEST_URI'];
    preg_match('/\/([^\/]+)\//', $request_uri, $matches);
    $subfolder = isset($matches[1]) ? $matches[1] : 'default';

    return isset($branding[$subfolder]) ? $branding[$subfolder] : $branding['default'];
}

function render_dynamic_logo() {
    $brand = get_advisor_branding();
    echo '<img src="' . esc_url($brand['logo']) . '" alt="' . esc_attr($brand['company_name']) . '" class="advisor-logo" />';
}

function render_dynamic_styles() {
    $brand = get_advisor_branding();
    echo '<style>
        body {
            --accent-color: ' . esc_attr($brand['color']) . ';
        }
        .tagline {
            font-style: italic;
            color: var(--accent-color);
        }
    </style>';
}
?>
