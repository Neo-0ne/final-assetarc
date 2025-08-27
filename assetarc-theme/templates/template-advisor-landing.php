<?php
/*
Template Name: Advisor Landing Page
*/
get_header(); ?>

<main class="advisor-page bg-black text-white py-16 px-6 lg:px-24">
    <div class="max-w-screen-xl mx-auto text-center">
        <h1 class="text-4xl lg:text-5xl font-semibold mb-6 text-gold">Power Your Advisory Practice with Automation</h1>
        <p class="text-lg text-gray-300 max-w-3xl mx-auto mb-12">
            White-label the AssetArc system, deliver branded outputs, and manage your clients with tokenized access.
        </p>
    </div>

    <div class="max-w-screen-xl mx-auto grid md:grid-cols-2 gap-12 items-center mb-16">
        <div>
            <img src="<?php echo get_template_directory_uri(); ?>/assets/images/hanno-bekker-headshot.jpg" alt="Advisor presenting" class="rounded-lg shadow-lg">
        </div>
        <div class="space-y-8">
            <div>
                <h3 class="text-2xl font-bold text-gold mb-3">Manage Tokens</h3>
                <p class="text-gray-400">Allocate, track, and recycle unused tokens for maximum efficiency and client billing.</p>
            </div>
            <div>
                <h3 class="text-2xl font-bold text-gold mb-3">Branded Portals</h3>
                <p class="text-gray-400">Add your logo, headers, and custom disclaimers to provide a seamless, white-glove experience for your clients.</p>
            </div>
            <div>
                <h3 class="text-2xl font-bold text-gold mb-3">Profitability Dashboard</h3>
                <p class="text-gray-400">Track revenue per client, cost per lead, and conversion rates to understand your business better.</p>
            </div>
            <div>
                <h3 class="text-2xl font-bold text-gold mb-3">Compliance Built-in</h3>
                <p class="text-gray-400">Leverage our Section 42–47 and FICA checks, with all outputs verified by a human professional.</p>
            </div>
        </div>
    </div>

    <div class="text-center">
        <a href="/contact" class="btn btn-gold">Book a Demo</a>
    </div>
</main>

<?php get_footer(); ?>
