from unittest.mock import AsyncMock

import pytest

import config
from media_platform.xhs.client import XiaoHongShuClient


@pytest.mark.asyncio
async def test_creator_start_page_skips_completed_pages(monkeypatch):
    monkeypatch.setattr(config, "START_PAGE", 2)
    monkeypatch.setattr(config, "CRAWLER_MAX_NOTES_COUNT", 100)
    client = XiaoHongShuClient(headers={}, playwright_page=None, cookie_dict={})
    client.get_notes_by_creator = AsyncMock(side_effect=[
        {"has_more": True, "cursor": "n1", "notes": [{"note_id": "n1"}]},
        {"has_more": False, "cursor": "n2", "notes": [{"note_id": "n2"}]},
    ])
    callback = AsyncMock()

    result = await client.get_all_notes_by_creator("u1", crawl_interval=0, callback=callback)

    callback.assert_awaited_once_with([{"note_id": "n2"}])
    assert [note["note_id"] for note in result] == ["n1", "n2"]
    assert client.get_notes_by_creator.await_args_list[1].args == ("u1", "n1")
