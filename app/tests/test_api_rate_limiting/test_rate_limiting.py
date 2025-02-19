# import pytest
# from httpx import AsyncClient
# from typing import Dict
# import os


# @pytest.mark.asyncio
# async def test_rate_limiting(
#     client: AsyncClient
# ):
#     for number_of_resquest in range(0, 10):
#         response = await client.get("/health")
#         if number_of_resquest < 2:
#             assert response.status_code == 200
#         assert response.status_code == 429
