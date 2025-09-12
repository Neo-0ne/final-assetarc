import os
import json
import glob
import re

def correct_business_logic(record):
    """
    Validates and corrects the business logic of a single P1 flashcard record.
    Returns the (potentially corrected) record and a boolean indicating if a correction was made.
    """
    try:
        goals = record.get("input", {}).get("goals", [])
        jurisdiction = record.get("input", {}).get("jurisdiction")
        current_structures = record.get("output", {}).get("recommended_structures", [])
        
        correct_structures = None
        
        # Rule 1 & 2: Simple ZA cases
        if jurisdiction == 'za':
            if sorted(goals) == ['asset_protection']:
                correct_structures = ['za_trust']
            elif sorted(goals) == ['liability_protection']:
                correct_structures = ['za_pty_ltd']
            # Rule 3: Hybrid ZA case
            elif 'asset_protection' in goals and 'liability_protection' in goals:
                correct_structures = sorted(list(set(current_structures) | {'za_pty_ltd', 'za_trust'}))

        # Rule 4: International cases
        if 'international_trade' in goals or 'tax_efficiency' in goals:
            if jurisdiction != 'za':
                 correct_structures = sorted(list(set(current_structures) | {'mu_ibc'}))

        if correct_structures and sorted(current_structures) != sorted(correct_structures):
            record["output"]["recommended_structures"] = correct_structures
            return record, True

    except Exception:
        return record, False

    return record, False

def flag_content_safety_issues(record):
    """
    Analyzes a record for content safety issues like PII or guarantees.
    Returns the record with a `qc_flags` key added if issues are found,
    and a boolean indicating if a flag was added.
    """
    flags = []
    text_to_check = json.dumps(record)

    if re.search(r'[\w\.-]+@[\w\.-]+', text_to_check):
        flags.append({"type": "content_safety", "details": "Found potential email address"})
    
    guarantee_keywords = ["guarantee", "guaranteed", "no risk", "will not owe", "certain to"]
    if any(keyword in text_to_check.lower() for keyword in guarantee_keywords):
        flags.append({"type": "content_safety", "details": "Found potential guarantee of outcome"})

    if flags:
        if "qc_flags" in record:
            record["qc_flags"].extend(flags)
        else:
            record["qc_flags"] = flags
        return record, True

    return record, False

def process_files():
    """
    Main function to find P1 data files, process them, and generate a report.
    """
    p1_files = glob.glob("generated_data/P1_*.ndjson")
    report = {
        "files_processed": [],
        "total_records_checked": 0,
        "total_errors_corrected": 0,
        "total_flags_added": 0,
        "details": {}
    }

    if not p1_files:
        print("No P1 NDJSON files found in generated_data/. Exiting.")
        return

    for filepath in p1_files:
        filename = os.path.basename(filepath)
        corrected_filepath = filepath.replace(".ndjson", "_corrected.ndjson")
        
        file_stats = {
            "records_checked": 0,
            "errors_corrected": 0,
            "flags_added": 0
        }

        print(f"Processing {filename}...")

        with open(filepath, 'r') as infile, open(corrected_filepath, 'w') as outfile:
            for line in infile:
                if not line.strip():
                    continue
                
                try:
                    record = json.loads(line)
                    file_stats["records_checked"] += 1

                    corrected_record, was_corrected = correct_business_logic(record)
                    if was_corrected:
                        file_stats["errors_corrected"] += 1

                    flagged_record, was_flagged = flag_content_safety_issues(corrected_record)
                    if was_flagged:
                        file_stats["flags_added"] += 1
                    
                    outfile.write(json.dumps(flagged_record) + '\n')

                except json.JSONDecodeError:
                    print(f"  WARNING: Skipping invalid JSON line in {filename}")

        report["files_processed"].append(filename)
        report["details"][filename] = file_stats
        report["total_records_checked"] += file_stats["records_checked"]
        report["total_errors_corrected"] += file_stats["errors_corrected"]
        report["total_flags_added"] += file_stats["flags_added"]

        print(f"  Finished processing. Corrected file saved to {corrected_filepath}")

    # Print final report
    print("\n--- QC Run Summary ---")
    print(f"Total files processed: {len(report['files_processed'])}")
    print(f"Total records checked: {report['total_records_checked']}")
    print(f"Total business logic errors corrected: {report['total_errors_corrected']}")
    print(f"Total content safety issues flagged: {report['total_flags_added']}")
    print("\n--- Detailed Report by File ---")
    for filename, stats in report["details"].items():
        print(f"\nFile: {filename}")
        print(f"  - Records Checked: {stats['records_checked']}")
        print(f"  - Errors Corrected: {stats['errors_corrected']}")
        print(f"  - Issues Flagged: {stats['flags_added']}")
    print("\n--- End of Report ---")

if __name__ == "__main__":
    process_files()
