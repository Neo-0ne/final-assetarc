import json
import os
import glob
import re
import math
from decimal import Decimal, InvalidOperation

# --- Validation Functions ---

def apply_content_safety_flags(record):
    """Checks for content safety issues."""
    flags = []
    text_to_check = json.dumps(record)
    GUARANTEE_KEYWORDS = ['guaranteed', 'risk-free', 'certain to']
    EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    if EMAIL_REGEX.search(text_to_check):
        flags.append({"type": "content_safety", "details": "Found potential PII (email address)"})
    if any(keyword in text_to_check.lower() for keyword in GUARANTEE_KEYWORDS):
        flags.append({"type": "content_safety", "details": "Found potential guarantee of outcome"})
    return flags

def validate_p2_completeness(record):
    """Checks for presence of required fields."""
    flags = []
    source_prompt = record.get('meta', {}).get('source_prompt_id', '')
    input_data = record.get('input', {})
    if 'ROLL' in source_prompt and not all(k in input_data for k in ['section', 'consideration', 'asset_profile']):
        flags.append({"type": "completeness", "details": "Missing required fields for Rollover."})
    elif 'BBBEE' in source_prompt and 'shareholders' not in input_data:
        flags.append({"type": "completeness", "details": "Missing required field for B-BBEE: shareholders"})
    return flags

def validate_bbee_logic(record):
    """Validates B-BBEE scorecard logic."""
    flags = []
    try:
        indicators = record.get('output', {}).get('indicators', {})
        total_points = Decimal(str(record.get('output', {}).get('total_ownership_points', 0)))
        calculated_sum = sum(Decimal(str(v.get('points', 0))) for v in indicators.values())
        if abs(total_points - calculated_sum) > Decimal('0.01'):
            flags.append({"type": "business_logic", "details": "B-BBEE points do not sum correctly."})
    except (TypeError, KeyError, InvalidOperation):
        flags.append({"type": "business_logic", "details": "Malformed B-BBEE record."})
    return flags

def validate_rollover_logic(record):
    """Validates Rollover Planner logic."""
    flags = []
    try:
        input_data = record.get('input', {})
        is_eligible = record.get('output', {}).get('eligibility', {}).get('eligible')
        if input_data.get('section') == 's42' and not input_data.get('consideration', {}).get('shares_issued') and is_eligible:
            flags.append({"type": "business_logic", "details": "s42 transaction incorrectly marked eligible."})
    except (TypeError, KeyError):
        flags.append({"type": "business_logic", "details": "Malformed Rollover record."})
    return flags

def apply_business_logic_flags(record):
    """Routes record to correct business logic validator."""
    source_prompt = record.get('meta', {}).get('source_prompt_id', '')
    if 'BBBEE' in source_prompt:
        return validate_bbee_logic(record)
    if 'ROLL' in source_prompt:
        return validate_rollover_logic(record)
    return []

def validate_statistical_anomalies(record, stats):
    """Checks for statistical outliers in numerical fields."""
    flags = []
    fields_to_check = ['market_value', 'base_cost']
    try:
        asset_profile = record.get('input', {}).get('asset_profile', {})
        if not asset_profile: return flags
        for field in fields_to_check:
            if field in asset_profile:
                value = Decimal(str(asset_profile[field]))
                stat = stats.get(field)
                if not stat or stat['std_dev'] == 0: continue
                z_score = abs((value - stat['mean']) / stat['std_dev'])
                if z_score > 5:
                    flags.append({"type": "statistical_anomaly", "details": f"Field '{field}' value {value} is a statistical outlier (Z-score: {z_score:.2f})"})
    except (TypeError, KeyError, InvalidOperation):
        flags.append({"type": "business_logic", "details": "Malformed asset_profile for stats check."})
    return flags

# --- Main Processing Logic (Two Passes) ---

def process_files():
    """Main function to find and process all P2 NDJSON files."""
    script_dir = os.path.dirname(__file__)
    source_dir = os.path.abspath(os.path.join(script_dir, '..', 'generated_data', 'P2'))
    files_to_process = glob.glob(os.path.join(source_dir, 'P2_*.ndjson'))
    files_to_process = [f for f in files_to_process if '_corrected' not in os.path.basename(f)]

    if not files_to_process:
        print(f"No P2 NDJSON files to process were found in {source_dir}"); return

    print(f"Found {len(files_to_process)} files to process...")

    # --- Pass 1: Calculate Statistics ---
    print("\n--- Pass 1: Calculating statistics for anomaly detection ---")
    values = {'market_value': [], 'base_cost': []}
    for filepath in files_to_process:
        with open(filepath, 'r', encoding='utf-8') as infile:
            for line in infile:
                try:
                    record = json.loads(line)
                    asset_profile = record.get('input', {}).get('asset_profile', {})
                    if 'market_value' in asset_profile: values['market_value'].append(Decimal(str(asset_profile['market_value'])))
                    if 'base_cost' in asset_profile: values['base_cost'].append(Decimal(str(asset_profile['base_cost'])))
                except (json.JSONDecodeError, InvalidOperation): continue

    stats = {}
    for field, data in values.items():
        if len(data) > 1:
            mean = sum(data) / len(data)
            variance = sum([(x - mean) ** 2 for x in data]) / len(data)
            stats[field] = {'mean': mean, 'std_dev': Decimal(math.sqrt(variance))}
            print(f"  - {field}: Mean={stats[field]['mean']:.2f}, StdDev={stats[field]['std_dev']:.2f}")

    # --- Pass 2: Process Files and Apply Validations ---
    print("\n--- Pass 2: Processing files and applying validations ---")
    report = {"files_processed": [], "total_records_checked": 0, "total_business_logic_flags": 0, "total_content_safety_flags": 0, "total_completeness_flags": 0, "total_anomaly_flags": 0, "details": {}}

    for filepath in files_to_process:
        filename = os.path.basename(filepath)
        corrected_filepath = filepath.replace(".ndjson", "_corrected.ndjson")
        file_stats = {"records_checked": 0, "business_logic_flags": 0, "content_safety_flags": 0, "completeness_flags": 0, "anomaly_flags": 0}
        print(f"\nProcessing {filename}...")
        with open(filepath, 'r', encoding='utf-8') as infile, open(corrected_filepath, 'w', encoding='utf-8') as outfile:
            for line in infile:
                file_stats["records_checked"] += 1
                try:
                    record = json.loads(line)
                    all_flags = [
                        *validate_p2_completeness(record),
                        *apply_business_logic_flags(record),
                        *apply_content_safety_flags(record),
                        *validate_statistical_anomalies(record, stats)
                    ]
                    if all_flags:
                        file_stats["completeness_flags"] += sum(1 for f in all_flags if f['type'] == 'completeness')
                        file_stats["business_logic_flags"] += sum(1 for f in all_flags if f['type'] == 'business_logic')
                        file_stats["content_safety_flags"] += sum(1 for f in all_flags if f['type'] == 'content_safety')
                        file_stats["anomaly_flags"] += sum(1 for f in all_flags if f['type'] == 'statistical_anomaly')
                        record['qc_flags'] = all_flags
                    outfile.write(json.dumps(record) + '\n')
                except json.JSONDecodeError:
                    outfile.write(line)

        report["files_processed"].append(filename)
        report["details"][filename] = file_stats
        for key in file_stats: report[f"total_{key}"] = report.get(f"total_{key}", 0) + file_stats[key]
        print(f"  Finished. Flagged file saved to {os.path.basename(corrected_filepath)}")

    # Print final summary report
    print("\n--- QC Run Summary ---")
    print(f"Total files processed: {len(report['files_processed'])}")
    print(f"Total records checked: {report['total_records_checked']}")
    print(f"Total business logic issues flagged: {report['total_business_logic_flags']}")
    print(f"Total content safety issues flagged: {report['total_content_safety_flags']}")
    print(f"Total completeness issues flagged: {report['total_completeness_flags']}")
    print(f"Total anomaly issues flagged: {report['total_anomaly_flags']}")
    print("\n--- Detailed Report by File ---")
    for filename, stats in report["details"].items():
        print(f"\nFile: {filename}")
        for key, value in stats.items():
            print(f"  - {key.replace('_', ' ').title()}: {value}")
    print("\n--- End of Report ---")

if __name__ == "__main__":
    process_files()
