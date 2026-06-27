from sensory_atlas.loaders import load_sensory_objects, load_test_sentences


def test_load_sensory_objects() -> None:
    objects = load_sensory_objects()

    assert len(objects) >= 1
    assert objects[0].object_id
    assert objects[0].core_axes is not None


def test_load_test_sentences() -> None:
    sentences = load_test_sentences()

    assert len(sentences) == 20
    assert all("raw_text" in sentence for sentence in sentences)
