<?php
/*
Template Name: Estate Structuring Tools
*/

get_header();

// Feature flags check
$estate_calculator_enabled = getenv('ESTATE_CALCULATOR_ENABLED') === 'true';
$succession_planner_enabled = getenv('SUCCESSION_PLANNER_ENABLED') === 'true';

if (!$estate_calculator_enabled && !$succession_planner_enabled) {
    echo '<main class="p-8 text-white max-w-5xl mx-auto text-center"><h1 class="text-2xl font-bold">Coming Soon</h1><p>This feature is not yet available. Please check back later.</p></main>';
    get_footer();
    exit;
}
?>

<main class="p-8 text-white max-w-5xl mx-auto">
    <h1 class="text-3xl font-bold mb-6 text-gold">Estate & Succession Tools</h1>

    <!-- Tab Navigation -->
    <div class="mb-4 border-b border-gray-700">
        <nav class="flex space-x-4" aria-label="Tabs">
            <?php if ($estate_calculator_enabled): ?>
                <button class="tab-button active" data-target="estate-calculator">Estate Duty Calculator</button>
            <?php endif; ?>
            <?php if ($succession_planner_enabled): ?>
                <button class="tab-button" data-target="succession-planner">Succession Planner</button>
            <?php endif; ?>
        </nav>
    </div>

    <!-- Tab Content -->
    <div>
        <?php if ($estate_calculator_enabled): ?>
            <div id="estate-calculator" class="tab-content active">
                <h2 class="text-2xl font-semibold mb-4">Estate Duty Calculator</h2>
                <p class="mb-6 text-gray-400">Estimate the potential fees and taxes on an estate and see how a trust structure can create significant savings.</p>
                <form id="estate-duty-form" class="bg-gray-900 p-6 rounded-lg space-y-4">
                    <h3 class="text-lg font-semibold">Assets</h3>
                    <div id="assets-container" class="space-y-3">
                        <!-- Asset rows will be added here -->
                    </div>
                    <button type="button" id="add-asset" class="bg-blue-600 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded">Add Asset</button>
                    <hr class="border-gray-700 !my-6">
                    <button type="submit" class="bg-gold hover:bg-yellow-400 text-black font-bold py-2 px-4 rounded w-full">Calculate</button>
                </form>
                <div id="estate-results-container" class="mt-6 hidden"></div>
            </div>
        <?php endif; ?>

        <?php if ($succession_planner_enabled): ?>
            <div id="succession-planner" class="tab-content hidden">
                <h2 class="text-2xl font-semibold mb-4">Succession Planner</h2>
                <p class="mb-6 text-gray-400">Answer a few simple questions to get high-level recommendations for your business continuity plan.</p>
                <form id="succession-form" class="bg-gray-900 p-6 rounded-lg space-y-4">
                    <div class="flex items-center">
                        <input id="has_partners" name="has_partners" type="checkbox" class="h-4 w-4 rounded border-gray-600 bg-gray-700 text-blue-600">
                        <label for="has_partners" class="ml-2 block text-sm">Do you have business partners?</label>
                    </div>
                    <div class="flex items-center">
                        <input id="has_buy_sell" name="has_buy_sell" type="checkbox" class="h-4 w-4 rounded border-gray-600 bg-gray-700 text-blue-600">
                        <label for="has_buy_sell" class="ml-2 block text-sm">Do you have a Buy-Sell Agreement in place?</label>
                    </div>
                     <button type="submit" class="bg-gold hover:bg-yellow-400 text-black font-bold py-2 px-4 rounded w-full">Get Recommendations</button>
                </form>
                <div id="succession-results-container" class="mt-6 hidden"></div>
            </div>
        <?php endif; ?>
    </div>
</main>

<style>
.tab-button {
    padding: 8px 16px;
    cursor: pointer;
    border: none;
    background-color: transparent;
    color: #9ca3af; /* gray-400 */
    border-bottom: 2px solid transparent;
}
.tab-button.active {
    color: #FFD700; /* gold */
    border-bottom-color: #FFD700;
}
.tab-content {
    display: none;
}
.tab-content.active {
    display: block;
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    // --- Tab Logic ---
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    const firstActiveButton = document.querySelector('.tab-button.active');
    if(firstActiveButton){
        document.getElementById(firstActiveButton.dataset.target).classList.add('active');
    }

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            tabContents.forEach(content => {
                content.classList.remove('active');
                if (content.id === button.dataset.target) {
                    content.classList.add('active');
                }
            });
        });
    });

    // --- Estate Duty Calculator Logic ---
    const estateForm = document.getElementById('estate-duty-form');
    if (estateForm) {
        const assetsContainer = document.getElementById('assets-container');
        const addAssetBtn = document.getElementById('add-asset');
        const estateResultsContainer = document.getElementById('estate-results-container');
        let assetId = 0;

        function createAssetRow() {
            assetId++;
            const row = document.createElement('div');
            row.className = 'grid grid-cols-1 md:grid-cols-3 gap-2 p-2 bg-gray-800 rounded items-center';
            row.innerHTML = `
                <input type="text" name="asset_name_${assetId}" placeholder="Asset Name (e.g., House)" class="w-full bg-gray-700 p-2 text-sm rounded" required>
                <input type="number" name="asset_value_${assetId}" placeholder="Value (R)" class="w-full bg-gray-700 p-2 text-sm rounded" required>
                <div class="flex items-center">
                    <input id="in_trust_${assetId}" name="in_trust_${assetId}" type="checkbox" class="h-4 w-4 rounded bg-gray-700">
                    <label for="in_trust_${assetId}" class="ml-2 text-sm">Held in Trust?</label>
                </div>
            `;
            assetsContainer.appendChild(row);
        }
        addAssetBtn.addEventListener('click', createAssetRow);
        createAssetRow(); // Start with one asset row

        estateForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(estateForm);
            const assets = [];
            for (let i = 1; i <= assetId; i++) {
                if (formData.get(`asset_name_${i}`)) {
                    assets.push({
                        name: formData.get(`asset_name_${i}`),
                        value: parseFloat(formData.get(`asset_value_${i}`)),
                        in_trust: formData.has(`in_trust_${i}`)
                    });
                }
            }
            const payload = { module_id: "estate_duty_calculator", inputs: { assets: assets } };

            estateResultsContainer.classList.remove('hidden');
            estateResultsContainer.innerHTML = '<p>Calculating...</p>';

            fetch('/compliance/run', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload) })
            .then(res => res.json())
            .then(data => {
                if (data.ok && data.result.status === 'completed') {
                    const details = data.result.details;
                    const formatCurrency = (num) => `R ${num.toLocaleString('en-ZA', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
                    estateResultsContainer.innerHTML = `
                        <h3 class="text-xl font-semibold mb-4">Calculation Summary</h3>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div class="bg-gray-800 p-4 rounded">
                                <h4 class="font-bold text-lg">Before Structuring</h4>
                                <p>Gross Estate: ${formatCurrency(details.before_scenario.gross_estate_value)}</p>
                                <p>Executor Fees: ${formatCurrency(details.before_scenario.executor_fees)}</p>
                                <p>Estate Duty: ${formatCurrency(details.before_scenario.estate_duty)}</p>
                                <p class="font-bold text-red-500 mt-2">Total Costs: ${formatCurrency(details.before_scenario.total_costs)}</p>
                            </div>
                            <div class="bg-gray-800 p-4 rounded">
                                <h4 class="font-bold text-lg">After Structuring</h4>
                                <p>Gross Estate: ${formatCurrency(details.after_scenario.gross_estate_value)}</p>
                                <p>Executor Fees: ${formatCurrency(details.after_scenario.executor_fees)}</p>
                                <p>Estate Duty: ${formatCurrency(details.after_scenario.estate_duty)}</p>
                                <p class="font-bold text-green-500 mt-2">Total Costs: ${formatCurrency(details.after_scenario.total_costs)}</p>
                            </div>
                        </div>
                        <div class="text-center bg-green-900/50 p-4 rounded mt-4">
                            <p class="text-lg font-bold text-green-400">Total Potential Savings: ${formatCurrency(details.summary.total_savings)}</p>
                        </div>
                    `;
                } else {
                     estateResultsContainer.innerHTML = '<p class="text-red-500">An error occurred. Please check your inputs.</p>';
                }
            }).catch(err => {
                estateResultsContainer.innerHTML = '<p class="text-red-500">A network error occurred.</p>';
            });
        });
    }

    // --- Succession Planner Logic ---
    const successionForm = document.getElementById('succession-form');
    if(successionForm) {
        const successionResultsContainer = document.getElementById('succession-results-container');
        successionForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const hasPartners = document.getElementById('has_partners').checked;
            const hasBuySell = document.getElementById('has_buy_sell').checked;
            const payload = { module_id: "succession_planner", inputs: { has_partners: hasPartners, has_buy_sell: hasBuySell } };

            successionResultsContainer.classList.remove('hidden');
            successionResultsContainer.innerHTML = '<p>Analyzing...</p>';

            fetch('/compliance/run', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload) })
            .then(res => res.json())
            .then(data => {
                if(data.ok && data.result.status === 'completed') {
                    const recommendations = data.result.details.recommendations;
                    successionResultsContainer.innerHTML = `
                        <h3 class="text-xl font-semibold mb-2">Your Recommendations</h3>
                        <ul class="space-y-3 list-disc list-inside">
                            ${recommendations.map(rec => `<li><span class="font-semibold">${rec.title}:</span> ${rec.text}</li>`).join('')}
                        </ul>
                    `;
                } else {
                    successionResultsContainer.innerHTML = '<p class="text-red-500">Could not retrieve recommendations.</p>';
                }
            }).catch(err => {
                successionResultsContainer.innerHTML = '<p class="text-red-500">A network error occurred.</p>';
            });
        });
    }
});
</script>

<?php get_footer(); ?>
