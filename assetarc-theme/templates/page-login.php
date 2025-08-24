<?php
/*
Template Name: Client Login
*/
get_header(); ?>

<main class="p-8 text-white max-w-md mx-auto">
  <h1 class="text-3xl font-bold mb-6">Client Vault Access</h1>
  <form method="post" action="/vault-access.php" class="space-y-4">
    <input type="text" name="token" placeholder="Enter Your Token" class="w-full p-3 rounded bg-gray-800 text-white border border-gray-600">
    <button type="submit" class="bg-gold text-black px-6 py-2 rounded hover:bg-yellow-400">Access Vault</button>
  </form>
</main>

<?php get_footer(); ?>
