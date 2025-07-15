import pytest
from xdl.client import XClient

@pytest.mark.asyncio
async def test_get_user_id():
    async with XClient() as cli:
        uid = await cli.get_user_id("jack")
    assert uid.isdigit()