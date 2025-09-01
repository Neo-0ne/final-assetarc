<?php
/**
 * Template Name: Insurance Wrapper Calculator
 *
 * This template provides a tool to calculate the tax benefit of
 * using an insurance wrapper for investments.
 */

get_header(); // Includes the header.php template file.
?>

<div id="primary" class="content-area">
    <main id="main" class="site-main">
        <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
            <header class="entry-header">
                <?php the_title('<h1 class="entry-title">', '</h1>'); ?>
            </header>

            <div class="entry-content">
                <p>This tool calculates the potential tax savings of using an insurance wrapper (like an endowment or sinking fund) compared to investing directly. The calculation is based on the different tax treatments of income and capital gains for individuals, companies, and trusts.</p>

                <div class="calculator-container card">
                    <div class="calculator-form">
                        <h3>Enter Investment Details</h3>
                        <form id="insurance-calculator-form">
                            <div class="form-group">
                                <label for="investment_amount">Investment Amount (ZAR)</label>
                                <input type="number" id="investment_amount" name="investment_amount" required value="1000000">
                            </div>
                            <div class="form-group">
                                <label for="investment_period_years">Investment Period (Years)</label>
                                <input type="number" id="investment_period_years" name="investment_period_years" required value="10">
                            </div>
                            <div class="form-group">
                                <label for="annual_growth_rate">Expected Annual Growth Rate (%)</label>
                                <input type="number" id="annual_growth_rate" name="annual_growth_rate" step="0.1" required value="8">
                            </div>
                            <div class="form-group">
                                <label for="investor_type">Investor Type</label>
                                <select id="investor_type" name="investor_type" required>
                                    <option value="individual" selected>Individual</option>
                                    <option value="company">Company</option>
                                    <option value="trust">Trust</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <button type="submit" class="button button-primary">Calculate Benefit</button>
                            </div>
                        </form>
                    </div>

                    <div class="calculator-results" id="results-container" style="display: none;">
                        <h3>Calculation Results</h3>
                        <div id="loader" style="display: none;">Calculating...</div>
                        <div id="results-content"></div>
                        <div id="error-message" style="display: none; color: red;"></div>
                    </div>
                </div>

            </div><!-- .entry-content -->
        </article><!-- #post-<?php the_ID(); ?> -->
    </main><!-- #main -->
</div><!-- #primary -->

<script>
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('insurance-calculator-form');
    const resultsContainer = document.getElementById('results-container');
    const loader = document.getElementById('loader');
    const resultsContent = document.getElementById('results-content');
    const errorMessage = document.getElementById('error-message');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        // Show loader and hide previous results/errors
        loader.style.display = 'block';
        resultsContainer.style.display = 'block';
        resultsContent.innerHTML = '';
        errorMessage.style.display = 'none';

        const formData = new FormData(form);
        const inputs = {
            investment_amount: parseFloat(formData.get('investment_amount')),
            investment_period_years: parseInt(formData.get('investment_period_years')),
            // Convert percentage to decimal
            annual_growth_rate: parseFloat(formData.get('annual_growth_rate')) / 100,
            investor_type: formData.get('investor_type')
        };

        // TODO: Replace with the actual API Gateway URL
        const apiUrl = '/api/eng-compliance/compliance/run';

        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                module_id: 'insurance_wrapper_calculator',
                inputs: inputs
            })
        })
        .then(response => response.json())
        .then(data => {
            loader.style.display = 'none';
            if (data.ok && data.result.status === 'completed') {
                displayResults(data.result.details);
            } else {
                let errorDetails = 'An unknown error occurred.';
                if (data.result && data.result.summary) {
                    errorDetails = data.result.summary;
                    if(data.result.details && Array.isArray(data.result.details)) {
                        errorDetails += '<br><ul>';
                        data.result.details.forEach(err => {
                            errorDetails += `<li><strong>${err.loc.join(', ')}:</strong> ${err.msg}</li>`;
                        });
                        errorDetails += '</ul>';
                    }
                }
                displayError(errorDetails);
            }
        })
        .catch(error => {
            loader.style.display = 'none';
            displayError('Failed to connect to the calculation service. Please try again later.');
            console.error('Error:', error);
        });
    });

    function displayError(message) {
        errorMessage.innerHTML = message;
        errorMessage.style.display = 'block';
    }

    function displayResults(details) {
        const { results } = details;
        const { unwrapped_investment, wrapped_investment, summary, total_growth } = results;

        const formatCurrency = (value) => new Intl.NumberFormat('en-ZA', { style: 'currency', currency: 'ZAR' }).format(value);

        resultsContent.innerHTML = `
            <div class="results-summary">
                <h4>Overall Benefit</h4>
                <p>Total Growth Before Tax: <strong>${formatCurrency(total_growth)}</strong></p>
                <p class="highlight">Total Tax Saving with Wrapper: <strong>${formatCurrency(summary.tax_saving_with_wrapper)}</strong></p>
                <p class="highlight">Net Return Benefit: <strong>${formatCurrency(summary.final_net_benefit)}</strong></p>
            </div>
            <hr>
            <div class="results-comparison">
                <div class="result-card">
                    <h5>Direct Investment (Unwrapped)</h5>
                    <p>Total Tax Payable: <strong>${formatCurrency(unwrapped_investment.total_tax)}</strong></p>
                    <p>Net Return After Tax: <strong>${formatCurrency(unwrapped_investment.net_return)}</strong></p>
                    <small>
                        Tax on Interest: ${formatCurrency(unwrapped_investment.tax_details.tax_on_interest)}<br>
                        Tax on Capital Gains: ${formatCurrency(unwrapped_investment.tax_details.tax_on_capital_gains)}<br>
                        Tax on Dividends: ${formatCurrency(unwrapped_investment.tax_details.tax_on_dividends)}
                    </small>
                </div>
                <div class="result-card">
                    <h5>Insurance Wrapper</h5>
                    <p>Total Tax Payable: <strong>${formatCurrency(wrapped_investment.total_tax)}</strong></p>
                    <p>Net Return After Tax: <strong>${formatCurrency(wrapped_investment.net_return)}</strong></p>
                    <small>All growth is taxed as a capital gain upon withdrawal.</small>
                </div>
            </div>
        `;
    }
});
</script>

<style>
.calculator-container.card {
    border: 1px solid #ddd;
    padding: 1.5em;
    border-radius: 8px;
    background-color: #f9f9f9;
    margin-top: 1em;
}
.form-group {
    margin-bottom: 1em;
}
.form-group label {
    display: block;
    margin-bottom: 0.5em;
    font-weight: bold;
}
.form-group input,
.form-group select {
    width: 100%;
    padding: 0.75em;
    border: 1px solid #ccc;
    border-radius: 4px;
}
.button.button-primary {
    background-color: #0073aa;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}
.button.button-primary:hover {
    background-color: #005a87;
}
.calculator-results {
    margin-top: 2em;
    padding-top: 1.5em;
    border-top: 1px solid #ddd;
}
.results-summary p.highlight {
    font-size: 1.2em;
    font-weight: bold;
    color: #2e8540; /* A green color for positive results */
}
.results-comparison {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5em;
    margin-top: 1em;
}
.result-card {
    background-color: #fff;
    border: 1px solid #e5e5e5;
    padding: 1em;
    border-radius: 4px;
}
.result-card h5 {
    margin-top: 0;
    border-bottom: 1px solid #eee;
    padding-bottom: 0.5em;
    margin-bottom: 0.5em;
}
.result-card p {
    margin-bottom: 0.5em;
}
</style>

<?php
get_footer(); // Includes the footer.php template file.
?>
