<?php
/**
 * Template Name: Services
 */

get_header();
?>

<main class="services-page bg-black text-white py-16 px-6 lg:px-24">
    <div class="max-w-screen-xl mx-auto text-center">
        <h1 class="text-4xl lg:text-5xl font-semibold mb-6 text-gold">Explore Our Structuring Workflows</h1>
        <p class="text-lg text-gray-300 max-w-3xl mx-auto mb-12">
            Each workflow is designed to handle compliance-sensitive processes, automatically applying checks before human review.
        </p>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div class="bg-neutral-900 rounded-lg p-6 text-left">
                <h3 class="text-2xl font-bold text-gold mb-3">Trust Setup</h3>
                <p class="text-gray-400 mb-4">Draft deeds, compliant with SARS & FICA.</p>
                <a href="/tool/trust-setup" class="btn btn-outline-gold">Start Now</a>
            </div>
            <div class="bg-neutral-900 rounded-lg p-6 text-left">
                <h3 class="text-2xl font-bold text-gold mb-3">Company Registration</h3>
                <p class="text-gray-400 mb-4">SA CIPC & offshore jurisdictions.</p>
                <a href="/tool/company-setup" class="btn btn-outline-gold">Start Now</a>
            </div>
            <div class="bg-neutral-900 rounded-lg p-6 text-left">
                <h3 class="text-2xl font-bold text-gold mb-3">Section 47 Compliance</h3>
                <p class="text-gray-400 mb-4">Test restructures against legislation.</p>
                <a href="/tool/sars-s47-check" class="btn btn-outline-gold">Start Now</a>
            </div>
            <div class="bg-neutral-900 rounded-lg p-6 text-left">
                <h3 class="text-2xl font-bold text-gold mb-3">FICA Intake</h3>
                <p class="text-gray-400 mb-4">Collect, flag, and store KYC/AML securely.</p>
                <a href="/tool/fica-intake" class="btn btn-outline-gold">Start Now</a>
            </div>
            <div class="bg-neutral-900 rounded-lg p-6 text-left">
                <h3 class="text-2xl font-bold text-gold mb-3">International Structuring</h3>
                <p class="text-gray-400 mb-4">USD-based with FX lock guarantee.</p>
                <a href="/tool/ibc-structuring" class="btn btn-outline-gold">Start Now</a>
            </div>
            <div class="bg-neutral-900 rounded-lg p-6 text-left">
                <h3 class="text-2xl font-bold text-gold mb-3">Quote Generator</h3>
                <p class="text-gray-400 mb-4">Instant ZAR/USD/crypto conversion.</p>
                <a href="/tool/quote-generator" class="btn btn-outline-gold">Start Now</a>
            </div>
        </div>
    </div>
</main>

<?php
get_footer();
?>
