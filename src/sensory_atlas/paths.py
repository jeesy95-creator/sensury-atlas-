"""Canonical data path registry for Sensory Atlas.

All data file paths must be imported from here.
Do not scatter path strings across the codebase.
"""

from __future__ import annotations

from pathlib import Path


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


PROJECT_ROOT = _project_root()

DATA_DIR = PROJECT_ROOT / "data"
CORE_DATA_DIR = DATA_DIR / "core"
EVALUATION_DATA_DIR = DATA_DIR / "evaluation"
VOCABULARY_DATA_DIR = DATA_DIR / "vocabulary"
WORKFLOW_DATA_DIR = DATA_DIR / "workflow"
REGRESSION_DATA_DIR = DATA_DIR / "regression"

# core — parser runtime
SENSORY_OBJECTS_PATH = CORE_DATA_DIR / "sensory_objects.jsonl"
PHRASE_CUES_PATH = CORE_DATA_DIR / "phrase_cues.json"
CUE_HIERARCHY_PATH = CORE_DATA_DIR / "cue_hierarchy.json"

# evaluation
TEST_SENTENCES_DEFAULT_PATH = EVALUATION_DATA_DIR / "test_sentences_20.jsonl"
TEST_SENTENCES_BLIND_PATH = EVALUATION_DATA_DIR / "blind_test_sentences_30.jsonl"
TEST_SENTENCES_HOLDOUT_PATH = EVALUATION_DATA_DIR / "holdout_test_sentences_50.jsonl"

# vocabulary
AXIS_DESCRIPTORS_PATH = VOCABULARY_DATA_DIR / "sensory_axis_descriptors.json"
AXIS_MAPPING_PATH = VOCABULARY_DATA_DIR / "axis_mapping.json"
MODIFIER_GROUPS_PATH = VOCABULARY_DATA_DIR / "sensory_modifier_groups.json"
EXPRESSION_PATTERNS_PATH = VOCABULARY_DATA_DIR / "sensory_expression_patterns.jsonl"
GENERAL_VOCABULARY_PATH = VOCABULARY_DATA_DIR / "general_sensory_vocabulary.csv"
DOMAIN_VOCABULARY_SEED_PATH = VOCABULARY_DATA_DIR / "domain_vocabulary_seed.csv"
DOMAIN_MAPPING_PATH = VOCABULARY_DATA_DIR / "domain_mapping.json"

# workflow
CANDIDATE_OBJECTS_PATH = WORKFLOW_DATA_DIR / "sensory_object_candidates.jsonl"
CANDIDATE_REVIEW_STATUS_PATH = WORKFLOW_DATA_DIR / "candidate_review_status.jsonl"
CURATED_SHORTLIST_PATH = WORKFLOW_DATA_DIR / "curated_candidate_shortlist_v1_5.jsonl"

# regression
DEV_FAILURE_CASES_PATH = REGRESSION_DATA_DIR / "dev_failure_cases.jsonl"
ONTOLOGY_EXPANSION_CASES_PATH = REGRESSION_DATA_DIR / "ontology_expansion_v1_5_cases.jsonl"

EVALUATION_DATASET_PATHS = {
    "default": TEST_SENTENCES_DEFAULT_PATH,
    "blind": TEST_SENTENCES_BLIND_PATH,
    "holdout": TEST_SENTENCES_HOLDOUT_PATH,
}
