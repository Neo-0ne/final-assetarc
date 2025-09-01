<?php
/* Template Name: Vault Access */

get_header();
?>

<main class="vault-access">
  <section class="container mx-auto px-6 py-10 text-white">
    <h1 class="text-3xl font-bold mb-4">🔐 Vault Access</h1>

    <form id="vault-login" class="bg-gray-900 p-6 rounded-xl shadow-lg max-w-md mx-auto" method="post" action="/wp-content/themes/assetarc-theme/Vault_API/vault-access.php">
      <label for="token" class="block mb-2 font-medium">Enter Access Token:</label>
      <input type="text" id="token" name="access_token" required class="w-full p-2 mb-4 text-black rounded">
      <button type="submit" class="bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded">Unlock</button>
    </form>

    <div id="vault-documents" class="mt-8 hidden">
      <h2 class="text-2xl mb-4">Your Vault Documents</h2>
      <div id="vault-content" class="grid gap-4 md:grid-cols-2">
        <!-- Populated by script.js -->
      </div>
    </div>
  </section>
</main>

<?php get_footer(); ?>
