import json
import os
import glob
import re

# --- Content Safety Rules (from prompts/P3_document_clauses/P3_REV_02.txt) ---

GUARANTEE_KEYWORDS = [
    'guaranteed', 'you will not owe tax', 'no tax', 'will avoid all tax',
    '100% success', 'zero risk', 'risk-free', 'certain to', 'indisputable'
]
EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
PLACEHOLDER_REGEX = re.compile(r'\b(TODO|FIXME|N/A|PLACEHOLDER)\b', re.IGNORECASE)

def apply_content_safety_flags(record):
    """
    Checks a record for content safety issues and returns a list of flags.
    """
    flags = []
    # Check relevant text fields for issues
    text_to_check = (
        record.get('input', {}).get('scenario', '') + ' ' +
        record.get('output', {}).get('reasoning', {}).get('legal', '') + ' ' +
        record.get('output', {}).get('reasoning', {}).get('practical', '')
    )

    if EMAIL_REGEX.search(text_to_check):
        flags.append({"type": "content_safety", "details": "Found potential PII (email address)"})
    if any(keyword in text_to_check.lower() for keyword in GUARANTEE_KEYWORDS):
        flags.append({"type": "content_safety", "details": "Found potential guarantee of outcome"})
    if PLACEHOLDER_REGEX.search(text_to_check):
        flags.append({"type": "content_safety", "details": "Found placeholder text in output"})

    return flags

def validate_p3_completeness(record):
    """
    Checks for the presence of mandatory clauses based on the document type,
    using the more specific rules from the enhanced P3_REV_01.txt.
    """
    flags = []
    doc_type = record.get('input', {}).get('document_type', '')
    clauses_included = record.get('output', {}).get('clauses_included', [])
    clauses_set = set(clauses_included)

    mandatory_clauses = {}
    if "Shareholders' Agreement" in doc_type:
        mandatory_clauses = {'sa_parties', 'sa_definitions', 'sa_transfer_restrictions'}
    elif "Non-Disclosure Agreement" in doc_type:
        mandatory_clauses = {'nda_parties', 'nda_def_confidential_info', 'nda_term'}
    elif "Board Resolution" in doc_type:
        mandatory_clauses = {'res_company_details', 'res_meeting_details', 'res_resolutions'}
    elif "Trust Deed" in doc_type:
        mandatory_clauses = {'td_settlor', 'td_trustees', 'td_beneficiaries', 'td_trust_property'}

    if mandatory_clauses:
        missing_clauses = mandatory_clauses - clauses_set
        if missing_clauses:
            for clause in missing_clauses:
                flags.append({
                    "type": "completeness",
                    "details": f"Document type '{doc_type}' is missing mandatory clause: {clause}"
                })

    return flags

# --- Business Logic Rules (from prompts/P3_document_clauses/P3_REV_01.txt) ---

def validate_shareholders_agreement_logic(record):
    """Validates the logic of a Shareholders' Agreement record."""
    flags = []
    try:
        scenario = record.get('input', {}).get('scenario', '').lower()
        clauses_included = record.get('output', {}).get('clauses_included', [])

        # Rule: 50/50 founders should not have a drag-along clause
        if '50/50' in scenario or 'fifty/fifty' in scenario:
            if 'sa_drag_along' in clauses_included:
                flags.append({
                    "type": "business_logic",
                    "details": "A 'drag_along' clause was included for a 50/50 founder scenario, which is generally incorrect."
                })

        # Rule: A majority investor scenario should likely have drag-along
        if 'investor' in scenario and 'majority' in scenario:
             if 'sa_drag_along' not in clauses_included:
                flags.append({
                    "type": "business_logic",
                    "details": "A 'drag_along' clause was not included for a majority investor scenario, which is unusual."
                })

    except (TypeError, KeyError):
        flags.append({"type": "business_logic", "details": "Malformed Shareholders' Agreement record structure."})
    return flags

def validate_nda_logic(record):
    """Validates the logic of an NDA record."""
    flags = []
    try:
        scenario = record.get('input', {}).get('scenario', '').lower()
        # This is a placeholder for a more complex check. A real implementation would
        # need to analyze the clause content, which is beyond this script's scope.
        # We can check for simple keywords.
        if 'unilateral' in scenario and 'mutual' in scenario:
             flags.append({
                "type": "business_logic",
                "details": "Scenario mentions both 'unilateral' and 'mutual', which is contradictory for an NDA."
            })
    except (TypeError, KeyError):
        flags.append({"type": "business_logic", "details": "Malformed NDA record structure."})
    return flags


def apply_business_logic_flags(record):
    """
    Routes a record to the correct business logic validator based on its document type.
    """
    doc_type = record.get('input', {}).get('document_type', '')

    if "Shareholders' Agreement" in doc_type:
        return validate_shareholders_agreement_logic(record)
    if "Non-Disclosure Agreement" in doc_type:
        return validate_nda_logic(record)

    return []

# --- Main Processing Logic ---

def process_files():
    """
    Main function to find and process all P3 NDJSON files and generate a detailed report.
    """
    script_dir = os.path.dirname(__file__)
    source_dir = os.path.abspath(os.path.join(script_dir, '..', 'generated_data', 'P3'))
    files_to_process = glob.glob(os.path.join(source_dir, 'P3_*.ndjson'))
    files_to_process = [f for f in files_to_process if '_corrected' not in os.path.basename(f)]

    if not files_to_process:
        print(f"No P3 NDJSON files to process were found in {source_dir}")
        return

    print(f"Found {len(files_to_process)} files to process...")

    report = {
        "files_processed": [],
        "total_records_checked": 0,
        "total_business_logic_flags": 0,
        "total_content_safety_flags": 0,
        "total_completeness_flags": 0,
        "details": {}
    }

    for filepath in files_to_process:
        filename = os.path.basename(filepath)
        corrected_filepath = filepath.replace(".ndjson", "_corrected.ndjson")

        file_stats = {"records_checked": 0, "business_logic_flags": 0, "content_safety_flags": 0, "completeness_flags": 0}
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

                    completeness_flags = validate_p3_completeness(record)
                    if completeness_flags:
                        file_stats["completeness_flags"] += len(completeness_flags)
                        all_flags.extend(completeness_flags)

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
                        for flag in all_flags:
                            if flag not in record['qc_flags']:
                                record['qc_flags'].append(flag)

                    outfile.write(json.dumps(record) + '\n')

                except json.JSONDecodeError:
                    print(f"  WARNING: Skipping invalid JSON line in {filename}")
                    outfile.write(line)

        report["files_processed"].append(filename)
        report["details"][filename] = file_stats
        report["total_records_checked"] += file_stats["records_checked"]
        report["total_business_logic_flags"] += file_stats["business_logic_flags"]
        report["total_content_safety_flags"] += file_stats["content_safety_flags"]
        report["total_completeness_flags"] += file_stats["completeness_flags"]
        print(f"  Finished. Flagged file saved to {os.path.basename(corrected_filepath)}")

    # Print final summary report
    print("\n--- QC Run Summary ---")
    print(f"Total files processed: {len(report['files_processed'])}")
    print(f"Total records checked: {report['total_records_checked']}")
    print(f"Total business logic issues flagged: {report['total_business_logic_flags']}")
    print(f"Total content safety issues flagged: {report['total_content_safety_flags']}")
    print(f"Total completeness issues flagged: {report['total_completeness_flags']}")
    print("\n--- Detailed Report by File ---")
    for filename, stats in report["details"].items():
        print(f"\nFile: {filename}")
        print(f"  - Records Checked: {stats['records_checked']}")
        print(f"  - Business Logic Flags: {stats['business_logic_flags']}")
        print(f"  - Content Safety Flags: {stats['content_safety_flags']}")
        print(f"  - Completeness Flags: {stats['completeness_flags']}")
    print("\n--- End of Report ---")

if __name__ == "__main__":
    process_files()
