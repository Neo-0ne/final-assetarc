<?php
/*
Template Name: Vault Page
*/

// --- Authentication Check ---
if (!is_user_logged_in() || !isset($_COOKIE['access_token'])) {
    wp_redirect(wp_login_url(get_permalink()));
    exit;
}

get_header();

// --- Fetch Files from eng-vault ---
$access_token = $_COOKIE['access_token'];
$api_url = 'http://eng-vault/vault/files'; // Internal service name

$response = wp_remote_get($api_url, [
    'timeout' => 20,
    'cookies' => ['access_token' => $access_token]
]);

$files = [];
$error_message = '';

if (is_wp_error($response)) {
    $error_message = 'Could not connect to the vault service.';
} else {
    $response_code = wp_remote_retrieve_response_code($response);
    if ($response_code === 200) {
        $body = wp_remote_retrieve_body($response);
        $data = json_decode($body, true);
        $files = $data['files'] ?? [];
    } else {
        $error_message = 'Could not retrieve your files. Please try again later.';
    }
}
?>

<main class="p-8 text-white max-w-4xl mx-auto">
  <h1 class="text-4xl font-bold mb-4">Client Vault</h1>
  <p class="mb-6">Securely access your documents and packages.</p>

  <?php if (!empty($error_message)): ?>
    <div class="bg-red-500 text-white p-4 rounded-lg">
      <?php echo esc_html($error_message); ?>
    </div>
  <?php elseif (empty($files)): ?>
    <div class="bg-neutral-800 p-6 rounded-lg text-center">
      <p>You have no documents in your vault yet.</p>
    </div>
  <?php else: ?>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <?php foreach ($files as $file): ?>
        <div class="bg-gray-800 p-6 rounded">
          <h2 class="text-2xl text-gold mb-2"><?php echo esc_html($file['filename']); ?></h2>
          <p class="text-sm text-gray-400 mb-4">Uploaded on: <?php echo esc_html(date('F j, Y', strtotime($file['created_at']))); ?></p>
          <!-- The download link will need a dedicated handler -->
          <a href="/vault/download/<?php echo esc_attr($file['file_id']); ?>" class="underline text-gold">Download</a>
        </div>
      <?php endforeach; ?>
    </div>
  <?php endif; ?>
</main>

<?php get_footer(); ?>
