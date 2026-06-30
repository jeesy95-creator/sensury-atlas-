import csv
import json
from pathlib import Path

from sensory_atlas.loaders import read_jsonl


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_DOMAINS = {"fragrance", "whisky", "wine", "coffee", "cross_domain"}
ALLOWED_INTEGRATION_STATUSES = {
    "existing_object",
    "candidate_object",
    "axis_descriptor",
    "do_not_integrate_yet",
}
REQUIRED_CSV_COLUMNS = {
    "domain",
    "vocabulary_type",
    "term",
    "korean_label",
    "sensory_family",
    "mapped_existing_objects",
    "candidate_object_id",
    "core_axes",
    "suggested_phrase_cues",
    "negative_cues",
    "integration_status",
    "notes",
}
REQUIRED_CROSS_DOMAIN_MAPPINGS = {
    "smoky",
    "clean",
    "powdery",
    "aquatic",
    "mineral",
    "woody",
    "green",
    "gourmand",
}


def test_domain_vocabulary_seed_csv_shape() -> None:
    path = PROJECT_ROOT / "data" / "domain_vocabulary_seed.csv"

    assert path.exists()
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) >= 120
    assert set(rows[0]) == REQUIRED_CSV_COLUMNS
    assert REQUIRED_DOMAINS <= {row["domain"] for row in rows}
    assert {row["integration_status"] for row in rows} <= ALLOWED_INTEGRATION_STATUSES


def test_sensory_object_candidates_jsonl_shape() -> None:
    path = PROJECT_ROOT / "data" / "sensory_object_candidates.jsonl"
    records = read_jsonl(path)

    assert path.exists()
    assert len(records) >= 40
    for record in records:
        assert record["candidate_object_id"]
        assert record["korean_label"]
        assert record["source_domains"]
        assert record["family"]
        assert record["definition"]
        assert record["core_axes"]
        assert len(record["example_expressions"]) >= 3
        assert record["suggested_phrase_cues"]
        assert record["integration_recommendation"]


def test_domain_mapping_json_shape() -> None:
    path = PROJECT_ROOT / "data" / "domain_mapping.json"

    assert path.exists()
    mapping = json.loads(path.read_text(encoding="utf-8"))

    assert mapping["version"] == "v1.1"
    assert REQUIRED_DOMAINS <= set(mapping["domains"])
    assert REQUIRED_CROSS_DOMAIN_MAPPINGS <= set(mapping["cross_domain_mappings"])
