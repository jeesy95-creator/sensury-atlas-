from sensory_atlas.loaders import load_sensory_objects
from sensory_atlas.schema import CoreAxes, SensoryObject


def test_required_fields_validate() -> None:
    obj = load_sensory_objects()[0]

    assert isinstance(obj, SensoryObject)
    for field in (
        "object_id",
        "label",
        "korean_label",
        "object_type",
        "family",
        "definition",
        "core_axes",
    ):
        assert getattr(obj, field)


def test_core_axes_accepts_string_list_and_null() -> None:
    axes = CoreAxes.model_validate(
        {
            "material": "Textile",
            "texture": ["Soft", "Fine"],
            "time": None,
        }
    )

    assert axes.material == "Textile"
    assert axes.texture == ["Soft", "Fine"]
    assert axes.time is None
