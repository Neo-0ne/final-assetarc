import json
import os
import glob
import re
from decimal import Decimal, InvalidOperation

# --- Content Safety Rules (from prompts/P2_Prompts/P2_REV_02.txt) ---

GUARANTEE_KEYWORDS = [
    'guaranteed', 'you will not owe tax', 'no tax', 'will avoid all tax',
    '100% success', 'zero risk', 'risk-free', 'certain to'
]
EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
PLACEHOLDER_REGEX = re.compile(r'\b(TODO|FIXME|N/A|PLACEHOLDER)\b', re.IGNORECASE)

def apply_content_safety_flags(record):
    """
    Checks a record for content safety issues and returns a list of flags.
    """
    flags = []
    # Check the whole record as a string for simplicity
    text_to_check = json.dumps(record)

    if EMAIL_REGEX.search(text_to_check):
        flags.append({"type": "content_safety", "details": "Found potential PII (email address)"})
    if any(keyword in text_to_check.lower() for keyword in GUARANTEE_KEYWORDS):
        flags.append({"type": "content_safety", "details": "Found potential guarantee of outcome"})
    if PLACEHOLDER_REGEX.search(text_to_check):
        flags.append({"type": "content_safety", "details": "Found placeholder text in output"})

    return flags

# --- Business Logic Rules (from prompts/P2_Prompts/P2_REV_01.txt) ---

def validate_bbee_logic(record):
    """Validates the logic of a B-BBEE scorecard record."""
    flags = []
    try:
        indicators = record.get('output', {}).get('indicators', {})
        total_points = record.get('output', {}).get('total_ownership_points', 0)

        calculated_sum = sum(Decimal(str(v.get('points', 0))) for v in indicators.values())

        # Use a small tolerance for floating point comparisons
        if abs(Decimal(str(total_points)) - calculated_sum) > Decimal('0.01'):
            flags.append({
                "type": "business_logic",
                "details": f"B-BBEE points do not sum correctly. Stated total: {total_points}, calculated sum: {calculated_sum}"
            })
    except (TypeError, KeyError, InvalidOperation):
        flags.append({"type": "business_logic", "details": "Malformed B-BBEE record structure."})
    return flags

def validate_rollover_logic(record):
    """Validates the logic of a Rollover Planner record."""
    flags = []
    try:
        input_data = record.get('input', {})
        output_data = record.get('output', {})
        section = input_data.get('section')
        is_eligible = output_data.get('eligibility', {}).get('eligible')

        # S42 eligibility check
        if section == 's42' and not input_data.get('consideration', {}).get('shares_issued') and is_eligible:
            flags.append({
                "type": "business_logic",
                "details": "s42 transaction incorrectly marked as eligible despite no shares being issued."
            })

        # Deferral benefit check
        net_deferral = Decimal(str(output_data.get('tax_comparison', {}).get('net_deferral_benefit', 0)))
        capital_gain = Decimal(str(input_data.get('asset_profile',{}).get('market_value',0))) - Decimal(str(input_data.get('asset_profile',{}).get('base_cost',0)))

        if is_eligible and capital_gain > 0 and net_deferral <= 0:
             flags.append({
                "type": "business_logic",
                "details": f"Eligible transaction with a capital gain of {capital_gain} has a non-positive deferral benefit of {net_deferral}."
            })

    except (TypeError, KeyError, InvalidOperation):
        flags.append({"type": "business_logic", "details": "Malformed Rollover record structure."})
    return flags

def apply_business_logic_flags(record):
    """
    Routes a record to the correct business logic validator based on its source prompt.
    """
    source_prompt = record.get('meta', {}).get('source_prompt_id', '')
    if 'BBBEE' in source_prompt:
        return validate_bbee_logic(record)
    if 'ROLL' in source_prompt:
        return validate_rollover_logic(record)
    # Add other P2 validators here if needed (e.g., for residency, estate planning)
    return []

# --- Main Processing Logic ---

def process_files():
    """
    Main function to find and process all P2 NDJSON files and generate a detailed report.
    """
    script_dir = os.path.dirname(__file__)
    source_dir = os.path.abspath(os.path.join(script_dir, '..', 'generated_data', 'P2'))
    files_to_process = glob.glob(os.path.join(source_dir, 'P2_*.ndjson'))
    files_to_process = [f for f in files_to_process if '_corrected' not in os.path.basename(f)]

    if not files_to_process:
        print(f"No P2 NDJSON files to process were found in {source_dir}")
        return

    print(f"Found {len(files_to_process)} files to process...")

    report = {
        "files_processed": [],
        "total_records_checked": 0,
        "total_business_logic_flags": 0,
        "total_content_safety_flags": 0,
        "details": {}
    }

    for filepath in files_to_process:
        filename = os.path.basename(filepath)
        corrected_filepath = filepath.replace(".ndjson", "_corrected.ndjson")

        file_stats = {"records_checked": 0, "business_logic_flags": 0, "content_safety_flags": 0}
        print(f"\nProcessing {filename}...")

        with open(filepath, 'r', encoding='utf-8') as infile, \
             open(corrected_filepath, 'w', encoding='utf-8') as outfile:
            for line in infile:
                if not line.strip():
                    continue

                file_stats["records_checked"] += 1
                try:
                    record = json.loads(line)
                    all_flags = []

                    # Unlike P1, for P2 we will only flag, not auto-correct business logic
                    business_flags = apply_business_logic_flags(record)
                    if business_flags:
                        file_stats["business_logic_flags"] += len(business_flags)
                        all_flags.extend(business_flags)

                    safety_flags = apply_content_safety_flags(record)
                    if safety_flags:
                        file_stats["content_safety_flags"] += len(safety_flags)
                        all_flags.extend(safety_flags)

                    if all_flags:
                        if 'qc_flags' not in record:
                            record['qc_flags'] = []
                        # Avoid adding duplicate flags
                        for flag in all_flags:
                            if flag not in record['qc_flags']:
                                record['qc_flags'].append(flag)

                    outfile.write(json.dumps(record) + '\n')

                except json.JSONDecodeError:
                    print(f"  WARNING: Skipping invalid JSON line in {filename}")
                    outfile.write(line) # Write invalid lines as-is

        report["files_processed"].append(filename)
        report["details"][filename] = file_stats
        report["total_records_checked"] += file_stats["records_checked"]
        report["total_business_logic_flags"] += file_stats["business_logic_flags"]
        report["total_content_safety_flags"] += file_stats["content_safety_flags"]
        print(f"  Finished. Flagged file saved to {os.path.basename(corrected_filepath)}")

    # Print final summary report
    print("\n--- QC Run Summary ---")
    print(f"Total files processed: {len(report['files_processed'])}")
    print(f"Total records checked: {report['total_records_checked']}")
    print(f"Total business logic issues flagged: {report['total_business_logic_flags']}")
    print(f"Total content safety issues flagged: {report['total_content_safety_flags']}")
    print("\n--- Detailed Report by File ---")
    for filename, stats in report["details"].items():
        print(f"\nFile: {filename}")
        print(f"  - Records Checked: {stats['records_checked']}")
        print(f"  - Business Logic Flags: {stats['business_logic_flags']}")
        print(f"  - Content Safety Flags: {stats['content_safety_flags']}")
    print("\n--- End of Report ---")

if __name__ == "__main__":
    process_files()
