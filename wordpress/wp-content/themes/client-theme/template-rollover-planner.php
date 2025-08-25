<?php
/**
 * Template Name: Section 42-47 Rollover Relief Planner
 *
 * This template provides a tool to check eligibility and calculate the tax
 * benefit of corporate rollover relief transactions.
 */

get_header();
?>

<div id="primary" class="content-area">
    <main id="main" class="site-main">
        <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
            <header class="entry-header">
                <?php the_title('<h1 class="entry-title">', '</h1>'); ?>
            </header>

            <div class="entry-content">
                <p>This tool helps you assess eligibility for corporate rollover relief under Sections 42, 45, 46, and 47 of the Income Tax Act, and quantifies the potential tax deferral benefit.</p>

                <div class="planner-container card">
                    <form id="rollover-planner-form">
                        <!-- Step 1: Section Selection -->
                        <div class="planner-step">
                            <h3>Step 1: Choose the Relevant Transaction</h3>
                            <div class="form-group-grid radio-grid">
                                <label><input type="radio" name="section" value="s42" checked> Sec 42: Asset-for-Share</label>
                                <label><input type="radio" name="section" value="s45"> Sec 45: Intra-Group</label>
                                <label><input type="radio"name="section" value="s46"> Sec 46: Unbundling</label>
                                <label><input type="radio" name="section" value="s47"> Sec 47: Liquidation</label>
                            </div>
                        </div>

                        <!-- Step 2: Eligibility Checklist (Dynamic) -->
                        <div id="eligibility-checklist" class="planner-step">
                            <h3>Step 2: Eligibility Checklist</h3>
                            <!-- Questions will be dynamically inserted here -->
                        </div>

                        <!-- Step 3: Financial Details -->
                        <div class="planner-step">
                            <h3>Step 3: Financial & Taxpayer Details</h3>
                            <div class="form-group-grid">
                                <div class="form-group">
                                    <label for="market_value">Asset Market Value (ZAR)</label>
                                    <input type="number" id="market_value" value="10000000">
                                </div>
                                <div class="form-group">
                                    <label for="base_cost">Asset Base Cost (ZAR)</label>
                                    <input type="number" id="base_cost" value="5000000">
                                </div>
                                <div class="form-group">
                                    <label for="taxpayer_type">Taxpayer Type</label>
                                    <select id="taxpayer_type">
                                        <option value="company" selected>Company</option>
                                        <option value="individual">Individual</option>
                                        <option value="trust">Trust</option>
                                    </select>
                                </div>
                            </div>
                        </div>

                        <div class="form-group">
                            <button type="submit" class="button button-primary">Analyze Transaction</button>
                        </div>
                    </form>

                    <!-- Results -->
                    <div id="results-container" class="calculator-results" style="display: none;">
                        <h3>Analysis Results</h3>
                        <div id="loader" style="display: none;">Calculating...</div>
                        <div id="results-content"></div>
                    </div>
                </div>

                <!-- Hidden master list of all possible questions -->
                <div id="master-questions" style="display: none;">
                    <div class="form-group" data-q="residency">
                        <label>Transferor/Transferee Residency</label>
                        <select class="residency-select" data-id="transferor_residency"><option value="SA">Transferor is SA Resident</option><option value="non-SA">non-SA</option></select>
                        <select class="residency-select" data-id="transferee_residency"><option value="SA">Transferee is SA Resident</option><option value="non-SA">non-SA</option></select>
                    </div>
                    <div class="form-group" data-q="group_relationship">
                        <label>Group Relationship</label>
                        <input type="checkbox" data-id="same_group" checked> Same Group?
                        <input type="number" data-id="percentage" value="70" placeholder="%">
                    </div>
                    <div class="form-group" data-q="consideration">
                        <label>Consideration</label>
                        <input type="checkbox" data-id="shares_issued" checked> Shares Issued?
                        <input type="number" data-id="cash_boot" value="0" placeholder="Cash Boot">
                        <input type="number" data-id="debt_assumed" value="0" placeholder="Debt Assumed">
                    </div>
                    <div class="form-group" data-q="continuity_flags">
                        <label>Continuity</label>
                        <input type="checkbox" data-id="nature_retained" checked> Asset nature retained?
                    </div>
                    <div class="form-group" data-q="timing_flags">
                         <label>Timing Flags</label>
                        <input type="number" data-id="earmarked_disposal_months" placeholder="Disposal in X months">
                    </div>
                    <div class="form-group" data-q="unbundling_details">
                        <label>Unbundling Details</label>
                        <input type="checkbox" data-id="control_threshold_met" checked> Control threshold met?
                    </div>
                     <div class="form-group" data-q="liquidation_details">
                        <label>Liquidation Details</label>
                        <input type="checkbox" data-id="steps_to_deregister_within_36m" checked> Steps to deregister taken?
                    </div>
                </div>
            </div>
        </article>
    </main>
</div>

<style>
/* Basic styles from previous calculators */
.planner-container.card { border: 1px solid #ddd; padding: 1.5em; border-radius: 8px; background-color: #f9f9f9; margin-top: 1em; }
.planner-step { border-bottom: 1px solid #e0e0e0; padding-bottom: 1.5em; margin-bottom: 1.5em; }
.form-group { margin-bottom: 1em; }
.form-group label { display: block; margin-bottom: 0.5em; font-weight: bold; }
.form-group input[type="number"], .form-group select { width: 100%; padding: 0.75em; border: 1px solid #ccc; border-radius: 4px; }
.form-group-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1em; }
.radio-grid { display: flex; flex-wrap: wrap; gap: 1.5em; }
.radio-grid label { font-weight: normal; }
.button-primary { background-color: #0073aa; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
.calculator-results { margin-top: 1em; padding-top: 1.5em; border-top: 2px solid #0073aa; }
/* Custom styles */
#eligibility-checklist .form-group { background-color: #fff; padding: 1em; border: 1px solid #e5e5e5; border-radius: 4px; }
#eligibility-checklist .form-group label { font-size: 0.9em; }
#eligibility-checklist .form-group input { margin-right: 5px; }
.results-grid { display: grid; grid-template-columns: 1fr 2fr; gap: 2em; }
.eligibility-result { padding: 1em; border-radius: 5px; }
.eligibility-result.eligible { background-color: #f0fff4; border: 1px solid #38a169; }
.eligibility-result.ineligible { background-color: #fff5f5; border: 1px solid #e53e3e; }
.eligibility-result ul { margin-top: 0.5em; padding-left: 20px; }
.tax-comparison-table { width: 100%; border-collapse: collapse; }
.tax-comparison-table th, .tax-comparison-table td { border: 1px solid #ddd; padding: 0.8em; text-align: left; }
.tax-comparison-table th { background-color: #f7f7f7; }
.tax-comparison-table .net-benefit { font-weight: bold; color: #2e8540; }
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('rollover-planner-form');
    const sectionRadios = form.elements['section'];
    const checklistContainer = document.getElementById('eligibility-checklist');
    const masterQuestions = document.getElementById('master-questions');

    const resultsContainer = document.getElementById('results-container');
    const loader = document.getElementById('loader');
    const resultsContent = document.getElementById('results-content');

    const questionMap = {
        s42: ['residency', 'consideration', 'continuity_flags', 'timing_flags'],
        s45: ['residency', 'group_relationship'],
        s46: ['residency', 'unbundling_details'],
        s47: ['residency', 'group_relationship', 'liquidation_details']
    };

    function updateChecklist() {
        const selectedSection = form.elements['section'].value;
        checklistContainer.innerHTML = '<h3>Step 2: Eligibility Checklist</h3>'; // Clear previous
        const questionsToShow = questionMap[selectedSection];
        questionsToShow.forEach(q_id => {
            const questionNode = masterQuestions.querySelector(`[data-q="${q_id}"]`);
            if (questionNode) {
                checklistContainer.appendChild(questionNode.cloneNode(true));
            }
        });
    }

    for (const radio of sectionRadios) {
        radio.addEventListener('change', updateChecklist);
    }

    // Initial setup
    updateChecklist();

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        loader.style.display = 'block';
        resultsContainer.style.display = 'block';
        resultsContent.innerHTML = '';

        const checklistData = new FormData(checklistContainer);
        const inputs = {
            section: form.elements['section'].value,
            taxpayer_type: document.getElementById('taxpayer_type').value,
            transferor_residency: checklistContainer.querySelector('[data-id="transferor_residency"]')?.value || 'SA',
            transferee_residency: checklistContainer.querySelector('[data-id="transferee_residency"]')?.value || 'SA',
            group_relationship: {
                same_group: checklistContainer.querySelector('[data-id="same_group"]')?.checked || false,
                percentage: parseFloat(checklistContainer.querySelector('[data-id="percentage"]')?.value) || 0
            },
            consideration: {
                shares_issued: checklistContainer.querySelector('[data-id="shares_issued"]')?.checked || false,
                cash_boot: parseFloat(checklistContainer.querySelector('[data-id="cash_boot"]')?.value) || 0,
                debt_assumed: parseFloat(checklistContainer.querySelector('[data-id="debt_assumed"]')?.value) || 0
            },
            asset_profile: {
                type: 'capital', // Simplified for now
                market_value: parseFloat(document.getElementById('market_value').value),
                base_cost: parseFloat(document.getElementById('base_cost').value)
            },
            continuity_flags: {
                nature_retained: checklistContainer.querySelector('[data-id="nature_retained"]')?.checked || false,
                anti_avoidance_risk: false // Not a user input
            },
            timing_flags: {
                earmarked_disposal_months: checklistContainer.querySelector('[data-id="earmarked_disposal_months"]')?.value ? parseInt(checklistContainer.querySelector('[data-id="earmarked_disposal_months"]').value) : null
            },
            unbundling_details: {
                listed: true, // Simplified
                control_threshold_met: checklistContainer.querySelector('[data-id="control_threshold_met"]')?.checked || false
            },
            liquidation_details: {
                steps_to_deregister_within_36m: checklistContainer.querySelector('[data-id="steps_to_deregister_within_36m"]')?.checked || false,
                retain_assets_for_debt: true // Simplified
            },
            recoupments: 0,
            allowances_claimed: 0
        };

        const apiUrl = '/api/eng-compliance/compliance/run';
        fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ module_id: 'rollover_planner', inputs: inputs })
        })
        .then(res => res.json())
        .then(data => {
            loader.style.display = 'none';
            if(data.ok) {
                renderResults(data.result.details);
            } else {
                renderError(data.result?.summary || 'An unexpected error occurred.');
            }
        })
        .catch(err => {
            loader.style.display = 'none';
            renderError('Failed to connect to the analysis service.');
        });
    });

    function renderError(message) {
         resultsContent.innerHTML = `<div class="eligibility-result ineligible"><strong>Error:</strong> ${message}</div>`;
    }

    function renderResults(details) {
        const { eligibility, tax_comparison } = details;
        const formatCurrency = (val) => new Intl.NumberFormat('en-ZA', { style: 'currency', currency: 'ZAR' }).format(val);

        let eligibilityHtml = '';
        if (eligibility.eligible) {
            eligibilityHtml = `<div class="eligibility-result eligible">
                <h4>Eligible for ${eligibility.decision_trace.length > 0 ? eligibility.decision_trace[0].rule.split('_')[0].toUpperCase() : ''} Relief</h4>
                ${eligibility.warnings.length > 0 ? `<strong>Warnings:</strong><ul>${eligibility.warnings.map(w => `<li>${w}</li>`).join('')}</ul>` : ''}
            </div>`;
        } else {
            eligibilityHtml = `<div class="eligibility-result ineligible">
                <h4>Not Eligible for Relief</h4>
                <strong>Reasons:</strong>
                <ul>${eligibility.failed_reasons.map(r => `<li>${r}</li>`).join('')}</ul>
            </div>`;
        }

        const taxHtml = `
            <div class="tax-comparison">
                <h4>Tax Impact Analysis</h4>
                <table class="tax-comparison-table">
                    <thead>
                        <tr><th>Scenario</th><th>Value</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>CGT without Relief</td><td>${formatCurrency(tax_comparison.cgt_no_relief)}</td></tr>
                        <tr><td>CGT with Relief (incl. boot)</td><td>${formatCurrency(tax_comparison.cgt_with_relief)}</td></tr>
                        <tr><td>Rolled-over Base Cost</td><td>${formatCurrency(tax_comparison.rolled_base_cost_to_acquirer)}</td></tr>
                        <tr class="net-benefit"><td>Net Tax Deferral Benefit</td><td>${formatCurrency(tax_comparison.net_deferral_benefit)}</td></tr>
                    </tbody>
                </table>
                <small>${tax_comparison.notes[0]}</small>
            </div>`;

        resultsContent.innerHTML = `<div class="results-grid">${eligibilityHtml}${taxHtml}</div>`;
    }
});
</script>

<?php
get_footer();
?>
