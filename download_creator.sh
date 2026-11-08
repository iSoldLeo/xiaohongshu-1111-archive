#!/bin/zsh
set -euo pipefail

ROOT="${0:A:h}"
CREATOR_URL='https://www.xiaohongshu.com/user/profile/63efba5a000000001001c0e3?xsec_token=ABcQ0e84TMCCQ4rELgE-fc2NApa7LjHlxKoS_mbqkQzv4=&xsec_source=pc_followed'
mkdir -p "$ROOT/logs" "$ROOT/downloads/63efba5a000000001001c0e3"
cd "$ROOT/MediaCrawler"

uv run --frozen main.py \
  --platform xhs \
  --lt qrcode \
  --type creator \
  --start "${1:-1}" \
  --creator_id "$CREATOR_URL" \
  --crawler_max_notes_count 10000 \
  --max_concurrency_num 1 \
  --get_media true \
  --get_comment false \
  --save_data_option json \
  --save_data_path "$ROOT/downloads/63efba5a000000001001c0e3" \
  2>&1 | tee "$ROOT/logs/creator_$(date +%Y%m%d_%H%M%S).log"
