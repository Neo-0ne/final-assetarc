<?php
/**
 * Template Name: International Tax Residency Planner
 *
 * This template provides a tool to help users determine their
 * South African tax residency status.
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
                <p>This tool helps you determine your South African tax residency status by guiding you through the official tests. Your tax residency status determines whether you are taxed on your worldwide income or only on income from a South African source.</p>

                <div class="planner-container card">
                    <!-- Step 1: Ordinary Residence -->
                    <div id="step-1" class="planner-step">
                        <h3>Step 1: Ordinary Residence Test</h3>
                        <p>This test is about where your "real home" is. Answer the following questions about your personal and economic ties to South Africa.</p>
                        <form id="ordinary-residence-form">
                            <div class="form-group-checkbox">
                                <input type="checkbox" id="has_permanent_home" name="has_permanent_home">
                                <label for="has_permanent_home">Do you have a permanent home available in South Africa?</label>
                            </div>
                            <div class="form-group-checkbox">
                                <input type="checkbox" id="has_family_ties" name="has_family_ties">
                                <label for="has_family_ties">Are your immediate family members (e.g., spouse, children) primarily based in South Africa?</label>
                            </div>
                             <div class="form-group-checkbox">
                                <input type="checkbox" id="has_economic_ties" name="has_economic_ties">
                                <label for="has_economic_ties">Are your main economic interests (e.g., businesses, assets) located in South Africa?</label>
                            </div>
                            <div class="form-group-checkbox">
                                <input type="checkbox" id="intends_to_return" name="intends_to_return">
                                <label for="intends_to_return">Do you intend to return to South Africa as your permanent home?</label>
                            </div>
                            <div class="form-group">
                                <button type="button" id="check-ordinary-residence" class="button">Check Ordinary Residence</button>
                            </div>
                        </form>
                    </div>

                    <!-- Step 2: Physical Presence -->
                    <div id="step-2" class="planner-step" style="display: none;">
                        <h3>Step 2: Physical Presence Test</h3>
                        <p>Since you may not be ordinarily resident, we need to check the number of days you have been physically present in South Africa.</p>
                        <form id="physical-presence-form">
                            <div class="form-group">
                                <label for="days_in_current_year">Days in SA (Current Tax Year)</label>
                                <input type="number" id="days_in_current_year" required value="100">
                            </div>
                            <p>Days in SA for each of the <strong>5 preceding</strong> tax years:</p>
                            <div class="form-group-grid">
                                <input type="number" id="prev_year_1" placeholder="Year -1" required value="100">
                                <input type="number" id="prev_year_2" placeholder="Year -2" required value="100">
                                <input type="number" id="prev_year_3" placeholder="Year -3" required value="100">
                                <input type="number" id="prev_year_4" placeholder="Year -4" required value="100">
                                <input type="number" id="prev_year_5" placeholder="Year -5" required value="100">
                            </div>
                             <div class="form-group">
                                <button type="submit" class="button button-primary">Determine My Residency</button>
                            </div>
                        </form>
                    </div>

                    <!-- Step 3: Exit Rule (Optional) -->
                    <div id="step-3" class="planner-step" style="display: none;">
                        <h4>Already a resident and think you've left? (Exit Rule)</h4>
                         <div class="form-group">
                            <label for="days_continuously_absent">Days continuously outside SA (optional)</label>
                            <input type="number" id="days_continuously_absent" placeholder="e.g., 331">
                            <small>If you were resident via the Physical Presence Test, spending over 330 continuous days abroad may cease your residency.</small>
                        </div>
                    </div>

                    <!-- Results -->
                    <div class="calculator-results" id="results-container" style="display: none;">
                        <h3>Your Tax Residency Status</h3>
                        <div id="loader" style="display: none;">Calculating...</div>
                        <div id="results-content"></div>
                    </div>
                </div>

            </div><!-- .entry-content -->
        </article><!-- #post-<?php the_ID(); ?> -->
    </main><!-- #main -->
</div><!-- #primary -->

<style>
.planner-container.card { border: 1px solid #ddd; padding: 1.5em; border-radius: 8px; background-color: #f9f9f9; margin-top: 1em; }
.planner-step { border-bottom: 1px solid #e0e0e0; padding-bottom: 1.5em; margin-bottom: 1.5em; }
.planner-step:last-child { border-bottom: none; }
.form-group { margin-bottom: 1em; }
.form-group-checkbox { display: flex; align-items: center; margin-bottom: 0.8em; }
.form-group-checkbox input { margin-right: 10px; width: auto; }
.form-group-checkbox label { margin-bottom: 0; font-weight: normal; }
.form-group-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(80px, 1fr)); gap: 10px; }
.form-group label, .form-group p { display: block; margin-bottom: 0.5em; font-weight: bold; }
.form-group input, .form-group select { width: 100%; padding: 0.75em; border: 1px solid #ccc; border-radius: 4px; }
.button { padding: 10px 15px; border: 1px solid #ccc; background-color: #f0f0f0; border-radius: 4px; cursor: pointer; }
.button-primary { background-color: #0073aa; color: white; border-color: #0073aa; }
.calculator-results { margin-top: 1em; padding-top: 1.5em; border-top: 2px solid #0073aa; }
.result-box { padding: 1em; border-radius: 5px; }
.result-box.resident { background-color: #fff5f5; border: 1px solid #e53e3e; }
.result-box.non-resident { background-color: #f0fff4; border: 1px solid #38a169; }
.result-box h4 { margin-top: 0; }
.result-box .reasoning { font-style: italic; color: #555; margin: 0.5em 0; }
.result-box .advice { margin-top: 1em; padding-top: 1em; border-top: 1px solid #ddd; font-weight: bold; }
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const step1 = document.getElementById('step-1');
    const step2 = document.getElementById('step-2');
    const step3 = document.getElementById('step-3'); // Optional exit rule inputs
    const checkOrdResidenceBtn = document.getElementById('check-ordinary-residence');
    const presenceForm = document.getElementById('physical-presence-form');

    const resultsContainer = document.getElementById('results-container');
    const loader = document.getElementById('loader');
    const resultsContent = document.getElementById('results-content');

    let ordinaryResidenceFlags = {};

    checkOrdResidenceBtn.addEventListener('click', function() {
        const ordForm = new FormData(document.getElementById('ordinary-residence-form'));
        ordinaryResidenceFlags = {
            has_permanent_home: ordForm.has('has_permanent_home'),
            has_family_ties: ordForm.has('has_family_ties'),
            has_economic_ties: ordForm.has('has_economic_ties'),
            intends_to_return: ordForm.has('intends_to_return')
        };

        // Simple heuristic: if 3 or more are true, they are likely resident. Let's send to API anyway.
        const trueCount = Object.values(ordinaryResidenceFlags).filter(Boolean).length;
        if (trueCount >= 3) {
            // We can pre-emptively run the calculation
             runFullCalculation();
        } else {
            // Otherwise, move to next step
            step1.style.display = 'none';
            step2.style.display = 'block';
            step3.style.display = 'block';
        }
    });

    presenceForm.addEventListener('submit', function(event) {
        event.preventDefault();
        runFullCalculation();
    });

    function runFullCalculation() {
        loader.style.display = 'block';
        resultsContainer.style.display = 'block';
        resultsContent.innerHTML = '';

        const presenceData = new FormData(presenceForm);
        const exitDays = document.getElementById('days_continuously_absent').value;

        const inputs = {
            ordinary_residence_flags: ordinaryResidenceFlags,
            days_in_current_year: parseInt(document.getElementById('days_in_current_year').value) || 0,
            days_each_of_prev_5_years: [
                parseInt(document.getElementById('prev_year_1').value) || 0,
                parseInt(document.getElementById('prev_year_2').value) || 0,
                parseInt(document.getElementById('prev_year_3').value) || 0,
                parseInt(document.getElementById('prev_year_4').value) || 0,
                parseInt(document.getElementById('prev_year_5').value) || 0,
            ],
            days_continuously_absent: exitDays ? parseInt(exitDays) : null,
        };

        const apiUrl = '/api/eng-compliance/compliance/run';

        fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                module_id: 'residency_planner',
                inputs: inputs
            })
        })
        .then(response => response.json())
        .then(data => {
            loader.style.display = 'none';
            if (data.ok && data.result.status === 'completed') {
                displayResults(data.result.details);
            } else {
                let errorSummary = (data.result && data.result.summary) ? data.result.summary : 'An unknown error occurred.';
                displayError(errorSummary);
            }
        })
        .catch(error => {
            loader.style.display = 'none';
            displayError('Failed to connect to the calculation service.');
            console.error('Error:', error);
        });
    }

    function displayError(message) {
        resultsContent.innerHTML = `<div class="result-box resident"><h4>Error</h4><p>${message}</p></div>`;
    }

    function displayResults(details) {
        const { status, reasoning, advice } = details;
        const statusClass = status.toLowerCase().replace(' ', '-');
        resultsContent.innerHTML = `
            <div class="result-box ${statusClass}">
                <h4>Status: ${status}</h4>
                <p class="reasoning">${reasoning}</p>
                <div class="advice">${advice}</div>
            </div>
        `;
    }
});
</script>

<?php
get_footer();
?>
