<?php
/**
 * Template Name: Pricing
 */

get_header();
?>

<main class="pricing-page bg-black text-white py-16 px-6 lg:px-24">
    <div class="max-w-screen-xl mx-auto">
        <h1 class="text-4xl lg:text-5xl font-semibold mb-10 text-gold">Pricing & Access</h1>

        <!-- Jules: Synthesized content for review -->
        <p class="text-lg mb-10 max-w-3xl">
            Our pricing is designed for two distinct paths: direct structuring for founders and HNWIs, and a scalable, recurring model for professional advisors who wish to leverage our platform for their own clients.
        </p>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-12 text-white">

            <!-- Private Clients -->
            <div class="card p-6 flex flex-col">
                <h2 class="text-2xl font-bold text-gold mb-4">For Founders & Individuals</h2>
                <p class="mb-6 flex-grow">
                    Engage with our automated workflows to design your structure. You only pay for the generation of final, human-reviewed document packs or for dedicated consultations with structuring professionals.
                </p>
                <ul class="space-y-2 mb-6 list-disc list-inside text-gray-300">
                    <li>Free access to explore all structuring workflows</li>
                    <li>Pay-per-document generation with transparent pricing</li>
                    <li>Direct access to book one-on-one consultations</li>
                    <li>A secure, personal vault for all your final documents</li>
                </ul>
                <a href="/assessment" class="btn btn-gold mt-auto">
                    Start Your Free Assessment
                </a>
            </div>

            <!-- Advisor Subscriptions -->
            <div class="card p-6 flex flex-col">
                <h2 class="text-2xl font-bold text-gold mb-4">For Advisors & Firms</h2>
                <p class="mb-6 flex-grow">
                    Transform your practice with our "Structuring-as-a-Service" model. Move beyond one-off fees to a scalable, recurring revenue stream, powered by our compliant, white-label ready platform.
                </p>
                <ul class="space-y-2 mb-6 list-disc list-inside text-gray-300">
                    <li>Subscription tiers for predictable, recurring revenue</li>
                    <li>Token packs for client document generation</li>
                    <li>A fully white-labeled portal with your firm's branding</li>
                    <li>Integrated compliance and client management tools</li>
                </ul>
                <a href="/advisor" class="btn btn-outline mt-auto">
                    Learn About the Advisor Platform
                </a>
            </div>
        </div>

        <!-- Advisor Pricing Table -->
        <section class="advisor-pricing-table mt-16">
            <h2 class="text-3xl font-semibold text-center mb-12">Advisor Subscription Tiers</h2>
            <div class="grid md:grid-cols-3 gap-8">
                <!-- Tier 1: Starter -->
                <div class="card p-8 text-center flex flex-col">
                    <h4 class="text-xl font-semibold text-gold">Starter Advisor</h4>
                    <p class="text-4xl font-bold my-4">R499<span class="text-lg font-normal">/mo</span></p>
                    <ul class="text-left space-y-2 mb-6 flex-grow">
                        <li>Up to 10 structure generations/month</li>
                        <li>Shared Client Vault Access</li>
                        <li>Standard Email Support</li>
                    </ul>
                    <a href="/subscribe/starter" class="btn btn-outline mt-auto">Subscribe</a>
                </div>
                <!-- Tier 2: Professional -->
                <div class="card p-8 text-center border-2 border-gold shadow-lg flex flex-col">
                    <h4 class="text-xl font-semibold text-gold">Professional</h4>
                    <p class="text-4xl font-bold my-4">R999<span class="text-lg font-normal">/mo</span></p>
                    <ul class="text-left space-y-2 mb-6 flex-grow">
                        <li>Up to 50 structure generations/month</li>
                        <li>Advisor Profitability Dashboard</li>
                        <li>Priority Support & Onboarding</li>
                    </ul>
                    <a href="/subscribe/professional" class="btn btn-gold mt-auto">Subscribe</a>
                </div>
                <!-- Tier 3: White-Label -->
                <div class="card p-8 text-center flex flex-col">
                    <h4 class="text-xl font-semibold text-gold">White-Label Partner</h4>
                    <p class="text-4xl font-bold my-4">R1999<span class="text-lg font-normal">/mo</span></p>
                    <ul class="text-left space-y-2 mb-6 flex-grow">
                        <li>Unlimited structure generations</li>
                        <li>Custom Branding & Domain</li>
                        <li>Client Token & Access Management</li>
                    </ul>
                    <a href="/subscribe/white-label" class="btn btn-outline mt-auto">Subscribe</a>
                </div>
            </div>
            <p class="text-center text-sm text-gray-500 mt-8">* Premium services like cross-jurisdictional structuring are billed on a pay-per-use basis. All prices are VAT exclusive.</p>
        </section>

        <div class="mt-16 max-w-4xl mx-auto text-center">
            <h3 class="text-2xl font-bold text-white mb-4">Bespoke Structuring for Family Offices & HNWIs</h3>
        <!-- End synthesized content -->
            <p class="mb-6 text-gray-400">
                We work with high-net-worth individuals, family offices, and specialist firms on bespoke structuring and legacy projects.
            </p>
            <a href="/contact" class="inline-block border border-gold text-gold px-6 py-3 rounded-full hover:bg-gold hover:text-black transition">
                Contact Our Team
            </a>
        </div>
    </div>
</main>

<?php
get_footer();
?>
