import json

from media_platform.xhs.extractor import XiaoHongShuExtractor


def test_note_state_preserves_quoted_undefined():
    note = {"noteId": "n1", "desc": 'undefined, :undefined, and "undefined"'}
    state = json.dumps({"note": {"noteDetailMap": {"n1": {"note": note}}}})
    state = state[:-1] + ',"optional":undefined,"aiNotes":new Map([])}'
    html = f"<script>window.__INITIAL_STATE__={state}</script>"

    result = XiaoHongShuExtractor().extract_note_detail_from_html("n1", html)

    assert result == {"note_id": "n1", "desc": note["desc"]}


def test_creator_state_preserves_body_text():
    html = '<script>window.__INITIAL_STATE__={"user":{"userPageData":{"desc":":undefined"}},"optional":undefined}</script>'

    result = XiaoHongShuExtractor().extract_creator_info_from_html(html)

    assert result == {"desc": ":undefined"}


def test_missing_state_returns_none():
    extractor = XiaoHongShuExtractor()
    assert extractor.extract_note_detail_from_html("n1", "<html></html>") is None
    assert extractor.extract_creator_info_from_html("<html></html>") is None
