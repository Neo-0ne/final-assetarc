<?php
/*
Template Name: Advisor Dashboard
*/

// This template is expected to be included by page-white-label.php,
// which already performs the authentication check.

get_header();

// --- Fetch Dashboard Data from eng-identity ---
$access_token = $_COOKIE['access_token'];
$api_url = 'http://eng-identity/api/v1/advisor/dashboard';

$response = wp_remote_get($api_url, [
    'timeout' => 20,
    'cookies' => ['access_token' => $access_token]
]);

$dashboard_data = null;
$error_message = '';

if (is_wp_error($response)) {
    $error_message = 'Could not connect to the advisor service.';
} else {
    $response_code = wp_remote_retrieve_response_code($response);
    if ($response_code === 200) {
        $body = wp_remote_retrieve_body($response);
        $data = json_decode($body, true);
        $dashboard_data = $data['dashboard_data'] ?? null;
    } else {
        $error_message = 'Could not retrieve your dashboard data.';
    }
}
?>

<main class="p-8 text-white max-w-6xl mx-auto">
  <h1 class="text-4xl font-bold mb-4">Advisor Dashboard</h1>
  <p class="mb-8">Manage your clients, review documents, and track your token usage.</p>

  <?php if (!empty($error_message)): ?>
    <div class="bg-red-500 text-white p-4 rounded-lg">
      <?php echo esc_html($error_message); ?>
    </div>
  <?php elseif (!$dashboard_data): ?>
    <div class="bg-neutral-800 p-6 rounded-lg text-center">
      <p>Could not load dashboard data.</p>
    </div>
  <?php else: ?>
    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div class="bg-gray-800 p-6 rounded-lg">
        <h3 class="text-lg text-gold">Active Clients</h3>
        <p class="text-3xl font-bold"><?php echo esc_html($dashboard_data['stats']['active_clients']); ?></p>
      </div>
      <div class="bg-gray-800 p-6 rounded-lg">
        <h3 class="text-lg text-gold">Pending Reviews</h3>
        <p class="text-3xl font-bold"><?php echo esc_html($dashboard_data['stats']['pending_reviews']); ?></p>
      </div>
      <div class="bg-gray-800 p-6 rounded-lg">
        <h3 class="text-lg text-gold">Tokens Remaining</h3>
        <p class="text-3xl font-bold"><?php echo esc_html($dashboard_data['stats']['tokens_remaining']); ?></p>
      </div>
    </div>

    <!-- Client Management Table -->
    <div class="bg-gray-800 p-6 rounded-lg">
      <h2 class="text-2xl font-semibold mb-4">My Clients</h2>
      <table class="w-full text-left">
        <thead>
          <tr>
            <th class="p-2">Client Email</th>
            <th class="p-2">Status</th>
            <th class="p-2">Last Activity</th>
            <th class="p-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          <?php foreach ($dashboard_data['clients'] as $client): ?>
            <tr class="border-t border-gray-700">
              <td class="p-2"><?php echo esc_html($client['email']); ?></td>
              <td class="p-2 text-yellow-400"><?php echo esc_html($client['status']); ?></td>
              <td class="p-2"><?php echo esc_html(date('F j, Y', strtotime($client['last_activity']))); ?></td>
              <td class="p-2"><a href="<?php echo esc_url($client['vault_url']); ?>" class="text-gold">View Vault</a></td>
            </tr>
          <?php endforeach; ?>
        </tbody>
      </table>
    </div>
  <?php endif; ?>
</main>

<?php get_footer(); ?>
