<?php
/**
 * Template Name: Consultation
 */

get_header();
?>

<main class="consultation-page bg-black text-white py-16 px-6 lg:px-24">
    <div class="max-w-screen-xl mx-auto">

        <h1 class="text-4xl lg:text-5xl font-semibold text-gold mb-10">Book a Consultation</h1>

        <section class="mb-10">
            <p class="text-lg text-gray-300 max-w-2xl">
                Whether you're ready to structure globally, optimize your tax position, or just want clarity on your next step — you're in the right place.
            </p>
        </section>

        <div class="bg-gray-900 p-6 rounded-xl shadow mb-16">
            <h2 class="text-2xl text-gold font-semibold mb-4">Choose Your Path</h2>

            <ul class="space-y-6 text-gray-300">
                <li>✔ 15-min Initial Discovery Call (Free)</li>
                <li>✔ 60-min Structuring Consultation (Paid)</li>
                <li>✔ Invite-only Deep Dive with Advisor (via Token Access)</li>
            </ul>
        </div>

        <section class="bg-gray-950 p-6 rounded-xl shadow-xl mb-16">
            <h2 class="text-xl text-white font-semibold mb-4">📅 Schedule Your Session</h2>
            <div class="calendly-inline-widget" data-url="https://calendly.com/YOUR-CALENDLY-URL" style="min-width:320px;height:700px;"></div>
            <script type="text/javascript" src="https://assets.calendly.com/assets/external/widget.js" async></script>
        </section>

        <section class="text-center mt-20">
            <h2 class="text-2xl lg:text-3xl font-bold text-white mb-4">Already Have a Token?</h2>
            <p class="text-gray-400 mb-6 max-w-2xl mx-auto">Enter your token to unlock access to private sessions, downloadable packs, or white-label structuring flows.</p>
            <a href="/vault" class="inline-block bg-gold text-black font-semibold px-6 py-3 rounded-full hover:bg-yellow-400 transition">
                Access the Vault
            </a>
        </section>

    </div>
</main>

<?php
get_footer();
?>
