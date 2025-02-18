import pytest
from httpx import AsyncClient
from typing import Dict
import os


@pytest.mark.asyncio
async def test_upload_profile_image_success(
    client: AsyncClient, get_current_user_token: Dict[str, str], get_test_db
):

    token = get_current_user_token["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_filename = "test.jpg"
    image_path = os.path.join(BASE_DIR, image_filename)

    with open(image_path, "rb") as image_file:
        response = await client.post(
            "/api/v1/profile-upload/",
            files={"image": ("test.jpg", image_file, "image/jpeg")},
            headers=headers,
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_upload_profile_image_fail(
    client: AsyncClient, get_current_user_token: Dict[str, str], get_test_db
):

    token = get_current_user_token["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_filename = "test2.svg"
    image_path = os.path.join(BASE_DIR, image_filename)

    with open(image_path, "rb") as image_file:
        response = await client.post(
            "/api/v1/profile-upload/",
            files={"image": ("test2.svg", image_file, "image/jpeg")},
            headers=headers,
        )
    assert response.status_code == 400


@pytest.mark.order(-1)
@pytest.mark.asyncio
async def test_upload_profile_to_s3_image_success(
    client: AsyncClient, get_current_user_token: Dict[str, str], get_test_db
):
    token = get_current_user_token["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_filename = "test.jpg"
    image_path = os.path.join(BASE_DIR, image_filename)

    with open(image_path, "rb") as image_file:
        response = await client.post(
            "/api/v1/profile-upload-s3/",
            files={"file": ("test.jpg", image_file, "image/jpeg")},
            headers=headers,
        )

    assert response.status_code == 200
    assert "filename" in response.json()
    assert response.json()["message"] == "Image uploaded successfully!"


@pytest.mark.asyncio
async def test_upload_profile__to_s3_image_fail(
    client: AsyncClient, get_current_user_token: Dict[str, str], get_test_db
):

    token = get_current_user_token["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_filename = "test2.svg"
    image_path = os.path.join(BASE_DIR, image_filename)

    with open(image_path, "rb") as image_file:
        response = await client.post(
            "/api/v1/profile-upload-s3/",
            files={"file": ("test2.svg", image_file, "image/jpeg")},
            headers=headers,
        )
    assert response.status_code == 500
