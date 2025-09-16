import json
import os
import glob
import re
import numpy as np
from collections import Counter

# --- Configuration ---
SOURCE_DATA_GLOB = "generated_data/P*/**/*.ndjson" # Use glob to find all P1, P2, P3 files
OUTPUT_DIR = "data/sapient_legal_master"
TRAIN_SPLIT_DIR = os.path.join(OUTPUT_DIR, "train")
MAX_SEQ_LEN = 256 # Increased for potentially longer P3 scenarios
PAD_TOKEN = "<pad>"
UNK_TOKEN = "<unk>"

# --- Helper Functions ---

def build_vocab(file_paths):
    """
    Reads all specified NDJSON files and builds a comprehensive vocabulary.
    """
    words = Counter()
    # Add all possible output structures/clauses to the vocab directly
    # This is more robust than trying to find them all in the generated data
    known_terms = {'za_pty_ltd', 'za_trust', 'mu_ibc', 'bvi_trust', 'jersey_trust', 'Shareholders\' Agreement'}

    for filepath in file_paths:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip(): continue
                record = json.loads(line)

                # Process text from all relevant fields
                text_fields = [
                    record.get('input', {}).get('scenario', ''),
                    record.get('input', {}).get('assumptions', ''),
                    record.get('input', {}).get('constraints', ''),
                    record.get('meta', {}).get('rationale', '')
                ]
                full_text = ' '.join(text_fields).lower()
                tokens = re.findall(r'\b\w+\b', full_text)
                words.update(tokens)

                # Also add output structures/clauses to known_terms set
                structs = record.get('output', {}).get('recommended_structures', [])
                clauses = record.get('output', {}).get('clauses_included', [])
                known_terms.update(structs)
                known_terms.update(clauses)

    # Create word-to-id mapping
    vocab = {PAD_TOKEN: 0, UNK_TOKEN: 1}
    for term in sorted(list(known_terms)):
        if term not in vocab: vocab[term] = len(vocab)
    for word, _ in words.most_common():
        if word not in vocab: vocab[word] = len(vocab)

    return vocab

def tokenize_and_pad(text, vocab, max_len):
    """
    Converts a text string or a list of terms into a padded list of integer tokens.
    """
    if isinstance(text, list):
        tokens = [vocab.get(str(t), vocab[UNK_TOKEN]) for t in text]
    else:
        raw_tokens = re.findall(r'\b\w+\b', str(text).lower())
        tokens = [vocab.get(t, vocab[UNK_TOKEN]) for t in raw_tokens]

    padded_tokens = tokens[:max_len] + [vocab[PAD_TOKEN]] * (max_len - len(tokens))
    return padded_tokens

def get_input_text_from_record(record):
    """
    Creates a single input text string from the most important fields of a record.
    """
    # For P1/P2 style records
    scenario = record.get('input', {}).get('scenario', '')
    if scenario:
        return scenario

    # For P3 style records, combine document type and scenario
    doc_type = record.get('input', {}).get('document_type', '')
    scenario = record.get('input', {}).get('scenario', '')
    if doc_type:
        return f"Document type: {doc_type}. Scenario: {scenario}"

    return "" # Should not happen with our data

def get_output_tokens_from_record(record):
    """
    Gets the correct output tokens, whether from structures or clauses.
    """
    return record.get('output', {}).get('recommended_structures', []) or record.get('output', {}).get('clauses_included', [])


# --- Main Conversion Logic ---

def convert_data():
    """
    Main function to find all data files, build a unified vocab, and convert
    all data to the HRM numpy format.
    """
    file_paths = glob.glob(SOURCE_DATA_GLOB, recursive=True)
    if not file_paths:
        print(f"ERROR: No data files found with glob pattern: {SOURCE_DATA_GLOB}")
        return

    print(f"--- Starting Data Conversion for {len(file_paths)} files ---")

    # 1. Build Unified Vocabulary
    print("Step 1: Building unified vocabulary...")
    vocab = build_vocab(file_paths)
    vocab_size = len(vocab)
    print(f"  Unified vocabulary size: {vocab_size}")

    # 2. Process records and tokenize
    print("Step 2: Processing and tokenizing records from all files...")
    all_inputs = []
    all_labels = []

    for filepath in file_paths:
        print(f"  - Processing {os.path.basename(filepath)}")
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip(): continue
                record = json.loads(line)

                input_text = get_input_text_from_record(record)
                input_tokens = tokenize_and_pad(input_text, vocab, MAX_SEQ_LEN)
                all_inputs.append(input_tokens)

                output_items = get_output_tokens_from_record(record)
                label_tokens = tokenize_and_pad(output_items, vocab, MAX_SEQ_LEN)
                all_labels.append(label_tokens)

    num_examples = len(all_inputs)
    print(f"  Processed {num_examples} total records.")

    # 3. Create NumPy arrays and indices
    print("Step 3: Creating NumPy arrays and index files...")
    results = {
        "inputs": np.array(all_inputs, dtype=np.int32),
        "labels": np.array(all_labels, dtype=np.int32),
        "group_indices": np.arange(num_examples + 1, dtype=np.int32),
        "puzzle_indices": np.arange(num_examples + 1, dtype=np.int32),
        "puzzle_identifiers": np.zeros(num_examples, dtype=np.int32),
    }

    # 4. Create metadata file
    print("Step 4: Creating metadata file...")
    metadata = {
        "seq_len": MAX_SEQ_LEN,
        "vocab_size": vocab_size,
        "pad_id": vocab[PAD_TOKEN],
        "ignore_label_id": vocab[PAD_TOKEN],
        "blank_identifier_id": 0,
        "num_puzzle_identifiers": 1,
        "total_groups": num_examples,
        "mean_puzzle_examples": 1,
        "sets": ["all"]
    }

    # 5. Save all files
    print(f"Step 5: Saving files to {TRAIN_SPLIT_DIR}...")
    os.makedirs(TRAIN_SPLIT_DIR, exist_ok=True)

    with open(os.path.join(TRAIN_SPLIT_DIR, "dataset.json"), "w") as f:
        json.dump(metadata, f, indent=2)

    with open(os.path.join(OUTPUT_DIR, "vocab.json"), "w") as f:
        json.dump(vocab, f, indent=2)

    for key, value in results.items():
        np.save(os.path.join(TRAIN_SPLIT_DIR, f"all__{key}.npy"), value)

    print("\n--- Data Conversion Complete ---")
    print(f"Converted data saved in: {TRAIN_SPLIT_DIR}")
    print(f"Vocabulary saved in: {os.path.join(OUTPUT_DIR, 'vocab.json')}")

if __name__ == "__main__":
    convert_data()
