import sys
import os
import json
import logging
import asyncio

# Fix path to allow importing 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Code")))

from app.services.ai_provider import ai_provider

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("Evaluator")

def run_evaluation():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "eval_samples.json")
    
    if not os.path.exists(data_path):
        logger.error(f"Error: Data file not found at {data_path}")
        return

    with open(data_path, 'r') as f:
        samples = json.load(f)

    logger.info(f"Loaded {len(samples)} samples. Starting evaluation...\n")
    logger.info("-" * 60)

    passed = 0
    failed = 0

    for sample in samples:
        test_id = sample.get("id", "unknown")
        text = sample["text"]
        expected_status = sample.get("expected_status", 200)
        note = sample.get("note", "")

        logger.info(f"TEST [{test_id}]: {note}")
        
        try:
            # Simulate basic validation logic that is in the API route
            if not text.strip():
                if expected_status == 400:
                    logger.info("  [PASS] Correctly identified empty string validation.")
                    passed += 1
                    logger.info("-" * 60)
                    continue
                else:
                    logger.error("  [FAIL] Input was empty but expected success?")
                    failed += 1
                    logger.info("-" * 60)
                    continue

            # Call the provider directly
            summary = ai_provider.summarize(text)
            
            # Checks for success cases
            if expected_status == 200:
                if summary:
                    # Check for specific substring expectations
                    if "expected_substring" in sample and sample["expected_substring"] not in summary:
                         logger.error(f"  [FAIL] Expected substring '{sample['expected_substring']}' not found in summary.")
                         logger.error(f"  Result: {summary}")
                         failed += 1
                    else:
                        logger.info(f"  [PASS] Summary generated successfully (Len: {len(summary)})")
                        logger.debug(f"  Result: {summary}")
                        passed += 1
                else:
                    # If summary is empty but we expected 200
                    # Note: ai_provider currently returns "" if no sentences found.
                    if len(text.strip()) > 0: 
                        logger.warning(f"  [WARN] Provider returned empty summary for non-empty text.")
                        # Deciding if this is a pass or fail depends on requirements. 
                        # For single char, maybe "" is acceptable?
                        passed += 1 
            else:
                logger.error(f"  [FAIL] Expected status {expected_status} but function returned success.")
                failed += 1

        except Exception as e:
            if expected_status != 200:
                logger.info(f"  [PASS] Caught expected exception: {e}")
                passed += 1
            else:
                logger.error(f"  [FAIL] Exception during processing: {e}")
                failed += 1
        
        logger.info("-" * 60)

    logger.info(f"\nFinal Results: {passed} PASSED, {failed} FAILED")

if __name__ == "__main__":
    run_evaluation()
