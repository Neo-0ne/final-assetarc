<?php
/*
Template Name: Vault Reset Page
*/
get_header(); ?>

<main class="p-8 text-white max-w-md mx-auto">
  <h1 class="text-3xl font-bold mb-4">Reset Your Vault Access</h1>
  <p class="mb-6">Forgot your token or lost access to your vault? Request a reset below. A temporary link will be emailed to you.</p>

  <form method="post" action="/vault-access/reset-handler.php" class="space-y-4">
    <div>
      <label for="email" class="block text-sm">Email Address</label>
      <input type="email" id="email" name="email" class="w-full p-2 rounded bg-gray-800 text-white border border-gray-600" required>
    </div>

    <div>
      <label for="reason" class="block text-sm">Reason for Reset</label>
      <textarea id="reason" name="reason" rows="3" class="w-full p-2 rounded bg-gray-800 text-white border border-gray-600" required></textarea>
    </div>

    <button type="submit" class="bg-gold text-black px-4 py-2 rounded hover:bg-yellow-400">Request Reset</button>
  </form>
</main>

<?php get_footer(); ?>
