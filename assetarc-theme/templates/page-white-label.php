<?php
/*
Template Name: White Label Page
*/

$is_advisor = false;
if (isset($_COOKIE['access_token'])) {
    $access_token = $_COOKIE['access_token'];
    $api_url = 'http://eng-identity/auth/user';

    $response = wp_remote_get($api_url, [
        'timeout' => 15,
        'cookies' => ['access_token' => $access_token]
    ]);

    if (!is_wp_error($response) && wp_remote_retrieve_response_code($response) === 200) {
        $user_data = json_decode(wp_remote_retrieve_body($response), true);
        if (isset($user_data['user']['role']) && $user_data['user']['role'] === 'advisor') {
            $is_advisor = true;
        }
    }
}

if ($is_advisor) {
    // If the user is an advisor, show the dashboard
    get_template_part('templates/template-advisor-dashboard');
} else {
    // Otherwise, show the marketing page
    get_header(); ?>
    <main class="p-8 text-white max-w-4xl mx-auto">
      <h1 class="text-4xl font-bold mb-4">White Label AssetArc</h1>
      <p class="mb-6 text-lg">Subscribe as an advisor and offer this platform under your own brand, powered by tokenized access control.</p>

      <section class="grid md:grid-cols-2 gap-6">
        <div class="bg-gray-800 p-6 rounded shadow">
          <h2 class="text-xl font-semibold mb-2">Your Logo. Your Domain.</h2>
          <p>Maintain your brand while we power the backend structuring engine and compliance logic.</p>
        </div>

        <div class="bg-gray-800 p-6 rounded shadow">
          <h2 class="text-xl font-semibold mb-2">Client Token Access</h2>
          <p>Issue structure-specific tokens to your clients so they can complete their setup privately, while you maintain full control.</p>
        </div>
      </section>

      <div class="mt-10 text-center">
        <a href="/consultation" class="bg-gold text-black px-6 py-3 rounded text-lg hover:bg-yellow-400">Become a Partner</a>
      </div>
    </main>
    <?php get_footer();
}
?>
