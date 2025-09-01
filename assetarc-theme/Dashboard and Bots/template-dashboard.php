<?php
/**
 * Template Name: Dashboard Template
 * Description: Custom dashboard layout for AssetArc clients and advisors.
 */

get_header();
?>

<div class="dashboard-container">
  <section class="dashboard-header">
    <h1>Welcome to Your AssetArc Dashboard</h1>
    <p>Access your documents, bots, and resources below.</p>
  </section>

  <section class="dashboard-grid">
    <div class="dashboard-card">
      <h2>Vault Access</h2>
      <p>View your stored legal structuring documents and submissions.</p>
      <a class="button" href="/vault-access.php">Open Vault</a>
    </div>

    <div class="dashboard-card">
      <h2>Available Bots</h2>
      <p>Generate and manage your structuring documents using our AI bots.</p>
      <a class="button" href="/bot-launchpad">Go to Bots</a>
    </div>

    <div class="dashboard-card">
      <h2>Token Usage</h2>
      <p>Check your token balance and view usage history.</p>
      <a class="button" href="/token-utils.php">View Tokens</a>
    </div>

    <div class="dashboard-card">
      <h2>Newsletter Settings</h2>
      <p>Update your newsletter preferences and content schedule.</p>
      <a class="button" href="/newsletter-handler.php">Manage Preferences</a>
    </div>
  </section>
</div>

<style>
.dashboard-container {
  padding: 2rem;
  color: #fff;
  background-color: #000;
}

.dashboard-header h1 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  color: #FFD700;
}

.dashboard-header p {
  color: #ccc;
}

.dashboard-grid {
  display: grid;
  gap: 2rem;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  margin-top: 2rem;
}

.dashboard-card {
  background: #111;
  padding: 1.5rem;
  border-radius: 1rem;
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.1);
}

.dashboard-card h2 {
  font-size: 1.25rem;
  margin-bottom: 1rem;
  color: #FFD700;
}

.dashboard-card p {
  color: #ccc;
  font-size: 0.95rem;
}

.dashboard-card .button {
  margin-top: 1rem;
  display: inline-block;
  padding: 0.75rem 1.25rem;
  background: linear-gradient(to right, #8C6239, #FFD700);
  color: #000;
  border-radius: 1rem;
  text-decoration: none;
  font-weight: bold;
}
</style>

<?php get_footer(); ?>
