# -*- coding: utf-8 -*-
# Copyright (c) 2025 relakkes@gmail.com
#
# This file is part of MediaCrawler project.
# Repository: https://github.com/NanmiCoder/MediaCrawler/blob/main/media_platform/xhs/extractor.py
# GitHub: https://github.com/NanmiCoder
# Licensed under NON-COMMERCIAL LEARNING LICENSE 1.1
#

# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：
# 1. 不得用于任何商业用途。
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。
# 3. 不得进行大规模爬取或对平台造成运营干扰。
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。
# 5. 不得用于任何非法或不当的用途。
#
# 详细许可条款请参阅项目根目录下的LICENSE文件。
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。

import json
import re
from typing import Dict, Optional

import humps


def _extract_initial_state(html: str) -> Dict:
    match = re.search(r"window\.__INITIAL_STATE__=({.*})</script>", html)
    if match is None:
        return {}
    # 网页状态包含 undefined 和空 Map；仅转换字符串外的 JavaScript 值。
    state = re.sub(
        r'"(?:\\.|[^"\\])*"|\bundefined\b|new Map\(\[\]\)',
        lambda token: {"undefined": "null", "new Map([])": "{}"}.get(token[0], token[0]),
        match.group(1),
    )
    return json.loads(state, strict=False)


class XiaoHongShuExtractor:
    def __init__(self):
        pass

    def extract_note_detail_from_html(self, note_id: str, html: str) -> Optional[Dict]:
        """Extract note details from HTML

        Args:
            html (str): HTML string

        Returns:
            Dict: Note details dictionary
        """
        if "noteDetailMap" not in html:
            # Either a CAPTCHA appeared or the note doesn't exist
            return None

        state = _extract_initial_state(html)
        if state:
            note_dict = humps.decamelize(state)
            return note_dict["note"]["note_detail_map"][note_id]["note"]
        return None

    def extract_creator_info_from_html(self, html: str) -> Optional[Dict]:
        """Extract user information from HTML

        Args:
            html (str): HTML string

        Returns:
            Dict: User information dictionary
        """
        info = _extract_initial_state(html)
        if not info:
            return None
        return info.get("user").get("userPageData")
