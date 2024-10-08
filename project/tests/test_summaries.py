import json


def test_create_summary(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", content=json.dumps({"url": "https://foo.bar"})
    )

    assert response.status_code == 201
    assert response.json()["url"] == "https://foo.bar"


def test_read_summary(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", content=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.get(f"/summaries/{summary_id}/")
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == "https://foo.bar"
    assert response_dict["summary"]
    assert response_dict["created_at"]


# def test_create_summaries_invalid_json(test_app):
#     response = test_app.post("/summaries/", data=json.dumps({}))
#     assert response.status_code == 422
#     assert response.json() == {
#         "detail": [
#             {
#                 "input": {},
#                 "loc": ["body", "url"],
#                 "msg": "Field required",
#                 "type": "missing",
#                 "url": "https://errors.pydantic.dev/2.5/v/missing",
#             }
#         ]
#     }


def test_read_all_summaries(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", content=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.get("/summaries/")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == summary_id, response_list))) == 1


def test_remove_summary(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", content=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.delete(f"/summaries/{summary_id}/")
    assert response.status_code == 200
    assert response.json() == {"id": summary_id, "url": "https://foo.bar"}


def test_remove_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.delete("/summaries/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_update_summary(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", content=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.put(
        f"/summaries/{summary_id}/",
        content=json.dumps({"url": "https://foo.bar", "summary": "updated!"}),
    )
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == "https://foo.bar"
    assert response_dict["summary"] == "updated!"
    assert response_dict["created_at"]


def test_update_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.put(
        "/summaries/999/",
        content=json.dumps({"url": "https://foo.bar", "summary": "updated!"}),
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_update_summary_invalid_json(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", content=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.put(f"/summaries/{summary_id}/", content=json.dumps({}))
    assert response.status_code == 422

    errors = response.json()["detail"]
    assert len(errors) == 2
    assert any(error["loc"] == ["body", "url"] for error in errors)
    assert any(error["loc"] == ["body", "summary"] for error in errors)
    assert all(error["type"] == "missing" for error in errors)


def test_update_summary_invalid_keys(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", content=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.put(
        f"/summaries/{summary_id}/", content=json.dumps({"url": "https://foo.bar"})
    )
    assert response.status_code == 422

    errors = response.json()["detail"]
    assert len(errors) == 1
    assert errors[0]["loc"] == ["body", "summary"]
    assert errors[0]["type"] == "missing"


# def test_read_summary_incorrect_id(test_app_with_db):
#     response = test_app_with_db.get("/summaries/999/")
#     assert response.status_code == 404
#     assert response.json()["detail"] == "Summary not found"

#     response = test_app_with_db.get("/summaries/0/")
#     assert response.status_code == 422
#     assert response.json() == {
#         "detail": [
#             {
#                 "ctx": {"gt": 0},
#                 "input": "0",
#                 "loc": ["path", "id"],
#                 "msg": "Input should be greater than 0",
#                 "type": "greater_than",
#                 "url": "https://errors.pydantic.dev/2.5/v/greater_than",
#             }
#         ]
#     }


# @pytest.mark.asyncio
# async def test_create_summaries_invalid_json(test_app):
#     async with AsyncClient(app=test_app.app, base_url="http://test") as ac:
#         response = await ac.post("/summaries/", json={})
#         assert response.status_code == 422

#         errors = response.json()["detail"]
#         assert len(errors) == 1
#         error = errors[0]

#         assert error["loc"] == ["body", "url"]
#         assert error["type"] == "missing"
#         assert error["msg"] == "Field required"

#         response = await ac.post("/summaries/", json={"url": "invalid://url"})
#         assert response.status_code == 422

#         errors = response.json()["detail"]
#         assert len(errors) == 1
#         error = errors[0]

#         assert error["loc"] == ["body", "url"]
#         assert "URL scheme should be 'http' or 'https'" in error["msg"]


# def test_create_summaries_invalid_json(test_app):
#     # Test with empty JSON
#     response = test_app.post("/summaries/", content=json.dumps({}))
#     assert response.status_code == 422
#     error_detail = response.json()["detail"][0]
#     assert error_detail["loc"] == ["body", "url"]
#     assert error_detail["msg"] == "Field required"
#     assert error_detail["type"] == "missing"

#     # Test with invalid URL
#     response = test_app.post("/summaries/", content=json.dumps({"url": "invalid://url"}))
#     assert response.status_code == 422
#     error_detail = response.json()["detail"][0]
#     assert error_detail["loc"] == ["body", "url"]
#     assert "URL scheme" in error_detail["msg"]
#     assert error_detail["type"] == "url_parsing"
