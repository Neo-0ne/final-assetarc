<?php
/*
Template Name: B-BBEE Scorecard Calculator
*/

get_header();

// Simple feature flag check
$bee_calculator_enabled = getenv('BEE_CALCULATOR_ENABLED') === 'true';

if (!$bee_calculator_enabled) {
    echo '<main class="p-8 text-white max-w-5xl mx-auto text-center"><h1 class="text-2xl font-bold">Coming Soon</h1><p>This feature is not yet available. Please check back later.</p></main>';
    get_footer();
    exit;
}
?>

<main class="p-8 text-white max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-4 text-gold">B-BBEE Ownership Scorecard Calculator</h1>
    <p class="mb-8 text-gray-300">Enter your company's ownership details to get a high-level estimate of your Ownership scorecard points.</p>

    <form id="bbee-form" class="bg-gray-900 p-6 rounded-lg shadow-lg space-y-6">

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
                <label for="total_entity_value" class="block text-sm font-medium">Total Entity Value (R)</label>
                <input type="number" id="total_entity_value" name="total_entity_value" class="mt-1 block w-full bg-gray-800 border-gray-700 rounded-md shadow-sm p-2" required>
            </div>
            <div>
                <label for="total_acquisition_debt" class="block text-sm font-medium">Black Participant Acquisition Debt (R)</label>
                <input type="number" id="total_acquisition_debt" name="total_acquisition_debt" class="mt-1 block w-full bg-gray-800 border-gray-700 rounded-md shadow-sm p-2" required>
            </div>
            <div>
                <label for="years_since_equity_deal" class="block text-sm font-medium">Years Since Deal</label>
                <input type="number" id="years_since_equity_deal" name="years_since_equity_deal" class="mt-1 block w-full bg-gray-800 border-gray-700 rounded-md shadow-sm p-2" required>
            </div>
        </div>

        <hr class="border-gray-700">

        <h2 class="text-xl font-semibold">Shareholders</h2>
        <div id="shareholders-container" class="space-y-4">
            <!-- Shareholder rows will be added here by JavaScript -->
        </div>

        <div class="flex justify-between items-center">
            <button type="button" id="add-shareholder" class="bg-blue-600 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded">
                Add Shareholder
            </button>
            <button type="submit" class="bg-gold hover:bg-yellow-400 text-black font-bold py-2 px-4 rounded">
                Calculate Score
            </button>
        </div>
    </form>

    <div id="results-container" class="mt-8 bg-gray-900 p-6 rounded-lg shadow-lg hidden">
        <h2 class="text-2xl font-bold mb-4">Scorecard Results</h2>
        <div id="results-content"></div>
    </div>

</main>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const shareholdersContainer = document.getElementById('shareholders-container');
    const addShareholderBtn = document.getElementById('add-shareholder');
    const bbeeForm = document.getElementById('bbee-form');
    const resultsContainer = document.getElementById('results-container');
    const resultsContent = document.getElementById('results-content');
    let shareholderId = 0;

    function createShareholderRow() {
        shareholderId++;
        const row = document.createElement('div');
        row.className = 'grid grid-cols-1 md:grid-cols-4 gap-3 p-3 bg-gray-800 rounded';
        row.setAttribute('data-id', shareholderId);

        row.innerHTML = `
            <div class="flex items-center">
                <input id="is_black_${shareholderId}" name="is_black_${shareholderId}" type="checkbox" class="h-4 w-4 rounded border-gray-600 bg-gray-700 text-blue-600 focus:ring-blue-500">
                <label for="is_black_${shareholderId}" class="ml-2 block text-sm">Is Black?</label>
            </div>
            <div class="flex items-center">
                <input id="is_black_woman_${shareholderId}" name="is_black_woman_${shareholderId}" type="checkbox" class="h-4 w-4 rounded border-gray-600 bg-gray-700 text-blue-600 focus:ring-blue-500">
                <label for="is_black_woman_${shareholderId}" class="ml-2 block text-sm">Is Black Woman?</label>
            </div>
            <div>
                <input type="number" name="voting_percentage_${shareholderId}" placeholder="Voting %" class="w-full bg-gray-700 border-gray-600 rounded-md p-2 text-sm" required>
            </div>
            <div>
                <input type="number" name="economic_interest_percentage_${shareholderId}" placeholder="Economic Interest %" class="w-full bg-gray-700 border-gray-600 rounded-md p-2 text-sm" required>
            </div>
        `;
        shareholdersContainer.appendChild(row);
    }

    addShareholderBtn.addEventListener('click', createShareholderRow);

    bbeeForm.addEventListener('submit', function(e) {
        e.preventDefault();
        resultsContainer.classList.add('hidden');
        resultsContent.innerHTML = '<p>Calculating...</p>';

        const formData = new FormData(bbeeForm);
        const shareholders = [];
        for (let i = 1; i <= shareholderId; i++) {
            shareholders.push({
                is_black: formData.has(`is_black_${i}`),
                is_black_woman: formData.has(`is_black_woman_${i}`),
                voting_percentage: parseFloat(formData.get(`voting_percentage_${i}`)),
                economic_interest_percentage: parseFloat(formData.get(`economic_interest_percentage_${i}`))
            });
        }

        const payload = {
            module_id: "bbee_ownership",
            inputs: {
                total_entity_value: parseFloat(formData.get('total_entity_value')),
                total_acquisition_debt: parseFloat(formData.get('total_acquisition_debt')),
                years_since_equity_deal: parseInt(formData.get('years_since_equity_deal')),
                shareholders: shareholders
            }
        };

        fetch('/compliance/run', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
        .then(response => response.json())
        .then(data => {
            resultsContainer.classList.remove('hidden');
            if (data.ok && data.result.status === 'completed') {
                const details = data.result.details;
                resultsContent.innerHTML = `
                    <h3 class="text-xl font-bold ${details.discounting_principle_applied ? 'text-red-500' : 'text-green-500'}">
                        Total Ownership Points: ${details.total_ownership_points} / 25
                    </h3>
                    ${details.discounting_principle_applied ? '<p class="text-red-500 font-semibold">Warning: Sub-minimum for Net Value not met. Your overall B-BBEE level will be discounted by one level.</p>' : ''}
                    <div class="mt-4 grid grid-cols-2 gap-4 text-sm">
                        ${Object.entries(details.indicators).map(([key, value]) => `
                            <div class="bg-gray-800 p-3 rounded">
                                <p class="font-semibold capitalize">${key.replace(/_/g, ' ')}</p>
                                <p>Points: <span class="font-bold text-gold">${value.points}</span></p>
                                <p>Actual: ${value.actual || 'N/A'}</p>
                                ${value.sub_minimum_met === false ? '<p class="text-red-500">Sub-minimum not met</p>' : ''}
                            </div>
                        `).join('')}
                    </div>
                `;
            } else {
                resultsContent.innerHTML = `<p class="text-red-500">An error occurred: ${data.error || data.result.summary}</p><pre class="text-xs text-left whitespace-pre-wrap">${JSON.stringify(data.result.details, null, 2)}</pre>`;
            }
        })
        .catch(error => {
            resultsContainer.classList.remove('hidden');
            resultsContent.innerHTML = `<p class="text-red-500">A network error occurred. Please try again.</p>`;
            console.error('Error:', error);
        });
    });

    // Add one shareholder row to start with
    createShareholderRow();
});
</script>

<?php get_footer(); ?>
