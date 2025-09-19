from server.models import SubmissionMeta, GPS, Device


def test_submission_meta_roundtrip():
    meta = SubmissionMeta(
        id="test123",
        timestamp="2025-09-17T00:00:00Z",
        user_id="u1",
        consent=True,
        tags=["synchronicity", "ritual"],
        gps=GPS(lat=1.23, lon=4.56, accuracy=7.0),
        device=Device(user_agent="pytest", make="x", model="y", os="z"),
        context={"k": "v"},
        sha256_map={"note.txt": "abc123"},
    )
    js = meta.model_dump_json()
    meta2 = SubmissionMeta.model_validate_json(js)
    assert meta2.id == meta.id
    assert meta2.gps and meta2.gps.lat == 1.23
