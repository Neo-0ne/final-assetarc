import os
from flask import Flask, jsonify, request
from pydantic import BaseModel, ValidationError

# Import the compliance modules
from modules import (
    run_s42_47_check, run_bbee_scorecard_check,
    run_estate_duty_check, run_succession_check
)

app = Flask(__name__)

# --- Feature Flags ---
BEE_CALCULATOR_ENABLED = os.getenv('BEE_CALCULATOR_ENABLED', 'false').lower() == 'true'
ESTATE_CALCULATOR_ENABLED = os.getenv('ESTATE_CALCULATOR_ENABLED', 'false').lower() == 'true'
SUCCESSION_PLANNER_ENABLED = os.getenv('SUCCESSION_PLANNER_ENABLED', 'false').lower() == 'true'


# --- Module Router ---
# This dictionary maps a module_id to the function that implements its logic.
# This makes it easy to add new compliance checks in the future.
COMPLIANCE_MODULES = {
    "s42_47": run_s42_47_check,
}

# Add modules behind feature flags
if BEE_CALCULATOR_ENABLED:
    COMPLIANCE_MODULES["bbee_ownership"] = run_bbee_scorecard_check
if ESTATE_CALCULATOR_ENABLED:
    COMPLIANCE_MODULES["estate_duty_calculator"] = run_estate_duty_check
if SUCCESSION_PLANNER_ENABLED:
    COMPLIANCE_MODULES["succession_planner"] = run_succession_check

# --- Models for Request Validation ---
class ComplianceRunBody(BaseModel):
    module_id: str
    inputs: dict

# --- Service Endpoints ---
@app.route('/')
def index():
    return jsonify({"service": "eng-compliance", "status": "running"})

@app.route('/compliance/run', methods=['POST'])
def run_compliance_check():
    try:
        body = ComplianceRunBody(**request.get_json(force=True))
    except ValidationError as e:
        return jsonify({'ok': False, 'error': e.errors()}), 400

    module_id = body.module_id
    inputs = body.inputs

    # Find the requested module in our router
    module_function = COMPLIANCE_MODULES.get(module_id)

    if not module_function:
        return jsonify({"error": f"Module with id '{module_id}' not found or not implemented."}), 404

    try:
        # Execute the module's logic
        result = module_function(inputs)

        # Add some metadata to the response
        response_data = {
            "ok": True,
            "module_id": module_id,
            "result": result
        }
        return jsonify(response_data)

    except Exception as e:
        app.logger.error(f"An error occurred while running module {module_id}: {e}")
        return jsonify({"ok": False, "error": f"An unexpected error occurred in module {module_id}"}), 500


@app.route('/compliance/evidence/<string:case_id>', methods=['GET'])
def get_evidence_pack(case_id):
    # Placeholder
    return jsonify({
        "status": "not_implemented",
        "case_id": case_id,
        "download_url": f"https://vault.example.com/evidence/{case_id}.zip"
    }), 501


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)
