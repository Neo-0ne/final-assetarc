<?php
/*
Template Name: Education Hub
*/
get_header(); ?>

<main class="p-8 text-white max-w-6xl mx-auto">
    <div class="text-center mb-16">
        <h1 class="text-4xl font-bold mb-4">Learn, Apply, and Stay Compliant</h1>
        <p class="text-lg text-gray-400">Guides, webinars, and FAQs to help you stay ahead of compliance requirements.</p>
    </div>

    <section class="space-y-12">
        <!-- Guides Section -->
        <div>
            <h2 class="text-3xl font-semibold text-gold mb-6 border-b border-gold pb-2">Guides</h2>
            <p class="text-gray-300">Downloadable structuring PDFs. <!-- Placeholder for guide list --></p>
        </div>

        <!-- Webinars Section -->
        <div>
            <h2 class="text-3xl font-semibold text-gold mb-6 border-b border-gold pb-2">Webinars</h2>
            <p class="text-gray-300">Upcoming dates + registration links. <!-- Placeholder for webinar list --></p>
        </div>

        <!-- FAQ Section -->
        <div>
            <h2 class="text-3xl font-semibold text-gold mb-6 border-b border-gold pb-2">FAQ</h2>
            <div class="space-y-4">
                <div class="faq-item">
                    <h4 class="text-xl font-semibold">What is Section 47?</h4>
                    <p class="text-gray-400">A provision in the Income Tax Act dealing with tax-neutral asset-for-share transactions.</p>
                </div>
                <div class="faq-item">
                    <h4 class="text-xl font-semibold">What is a PEP?</h4>
                    <p class="text-gray-400">A Politically Exposed Person, which requires enhanced due diligence under FICA.</p>
                </div>
            </div>
        </div>
    </section>
</main>

<?php get_footer(); ?>
