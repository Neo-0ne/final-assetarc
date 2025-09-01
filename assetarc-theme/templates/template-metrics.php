<?php
/* Template Name: Metrics Dashboard */

get_header();
?>

<main class="metrics-dashboard">
  <section class="container mx-auto px-6 py-10 text-white">
    <h1 class="text-3xl font-bold mb-6">📊 Platform Metrics Dashboard (MVP)</h1>
    <div id="metrics-content" class="grid gap-6 md:grid-cols-2">

      <!-- Total Revenue Card -->
      <div class="p-4 bg-gray-900 rounded-xl shadow-lg">
        <h2 class="text-xl font-semibold mb-2">Total Revenue</h2>
        <p id="total-revenue" class="text-2xl font-bold">Loading...</p>
      </div>

      <!-- Total Transactions Card -->
      <div class="p-4 bg-gray-900 rounded-xl shadow-lg">
        <h2 class="text-xl font-semibold mb-2">Total Transactions</h2>
        <p id="total-transactions" class="text-2xl font-bold">Loading...</p>
      </div>

    </div>
  </section>
</main>

<script>
document.addEventListener('DOMContentLoaded', function() {
    // In a real WordPress theme, you would use wp_localize_script to pass
    // data from PHP to JavaScript securely. For this MVP, we will use the
    // hardcoded mock API key to demonstrate functionality.
    const apiKey = "mock-internal-api-key";
    const metricsUrl = 'http://localhost:5003/api/v1/metrics';

    const totalRevenueEl = document.getElementById('total-revenue');
    const totalTransactionsEl = document.getElementById('total-transactions');

    fetch(metricsUrl, {
        headers: { 'x-api-key': apiKey }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.ok && data.metrics) {
            const metrics = data.metrics;
            // Format the revenue as currency.
            const formattedRevenue = new Intl.NumberFormat('en-ZA', {
                style: 'currency',
                currency: metrics.currency || 'ZAR'
            }).format(metrics.total_revenue);

            totalRevenueEl.textContent = formattedRevenue;
            totalTransactionsEl.textContent = String(metrics.total_transactions);
        } else {
            const errorMsg = data.error || 'API response was not ok.';
            throw new Error(errorMsg);
        }
    })
    .catch(error => {
        console.error('Error fetching metrics:', error);
        totalRevenueEl.textContent = 'Error';
        totalTransactionsEl.textContent = 'Error';
    });
});
</script>

<?php get_footer(); ?>
