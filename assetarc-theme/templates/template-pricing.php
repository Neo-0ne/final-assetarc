<?php
/**
 * Template Name: Pricing
 */

get_header();
?>

<main class="pricing-page bg-black text-white py-16 px-6 lg:px-24">
    <div class="max-w-screen-xl mx-auto text-center">
        <h1 class="text-4xl lg:text-5xl font-semibold mb-6 text-gold">Transparent Pricing, No Surprises</h1>
        <p class="text-lg text-gray-300 max-w-3xl mx-auto mb-12">
            Our pricing is token-based, transparent, and FX-aware. Quotes are valid for 7 days; USD-based quotes are locked for 24h.
        </p>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <!-- Starter Tier -->
            <div class="card bg-neutral-900 p-8 rounded-lg flex flex-col">
                <h3 class="text-2xl font-bold text-gold mb-4">Starter</h3>
                <p class="text-3xl font-bold mb-4">From R1,200</p>
                <ul class="text-left space-y-2 mb-6 flex-grow text-gray-400">
                    <li class="flex items-center"><span class="text-gold mr-2">&#10003;</span> Single process run</li>
                    <li class="flex items-center"><span class="text-gold mr-2">&#10003;</span> Compliance check</li>
                    <li class="flex items-center"><span class="text-gold mr-2">&#10003;</span> Vault delivery</li>
                </ul>
                <a href="/assessment" class="btn btn-outline-gold mt-auto">Get Started</a>
            </div>

            <!-- Professional Tier -->
            <div class="card bg-neutral-800 p-8 rounded-lg flex flex-col border-2 border-gold">
                <h3 class="text-2xl font-bold text-gold mb-4">Professional</h3>
                <p class="text-3xl font-bold mb-4">From R3,500</p>
                <ul class="text-left space-y-2 mb-6 flex-grow text-gray-400">
                    <li class="flex items-center"><span class="text-gold mr-2">&#10003;</span> Bundled services</li>
                    <li class="flex items-center"><span class="text-gold mr-2">&#10003;</span> Multiple documents</li>
                    <li class="flex items-center"><span class="text-gold mr-2">&#10003;</span> Priority support</li>
                </ul>
                <a href="/assessment" class="btn btn-gold mt-auto">Get Started</a>
            </div>

            <!-- Advisor Tier -->
            <div class="card bg-neutral-900 p-8 rounded-lg flex flex-col">
                <h3 class="text-2xl font-bold text-gold mb-4">Advisor / White-label</h3>
                <p class="text-3xl font-bold mb-4">Custom</p>
                <ul class="text-left space-y-2 mb-6 flex-grow text-gray-400">
                    <li class="flex items-center"><span class="text-gold mr-2">&#10003;</span> Custom token packs</li>
                    <li class="flex items-center"><span class="text-gold mr-2">&#10003;</span> Branded portal</li>
                    <li class="flex items-center"><span class="text-gold mr-2">&#10003;</span> Client management</li>
                </ul>
                <a href="/contact" class="btn btn-outline-gold mt-auto">Contact Us</a>
            </div>
        </div>

        <div class="mt-12 text-sm text-gray-500">
            <p><span class="font-semibold">Surcharges:</span> BVI +15% | St. Kitts +20% | Urgent reviews +10%</p>
        </div>
    </div>
</main>

<?php
get_footer();
?>
