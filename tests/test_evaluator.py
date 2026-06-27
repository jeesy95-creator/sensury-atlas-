from sensory_atlas.evaluator import evaluate_parser
from sensory_atlas.loaders import load_sensory_objects, load_test_sentences


def test_evaluator_runs() -> None:
    objects = load_sensory_objects()
    sentences = load_test_sentences()

    report = evaluate_parser(sentences, objects)

    assert report.total == 20
    assert 0 <= report.top1_hit_rate <= 1
    assert 0 <= report.top3_hit_rate <= 1
    assert report.rows
