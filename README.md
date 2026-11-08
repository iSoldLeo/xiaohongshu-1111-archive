# 小红书「1111」笔记归档

2026 年 11 月 8 日采集的完整快照，包含笔记文字、图片、核验结果和采集工具源码。

## 归档结果

| 项目 | 数量 |
| --- | ---: |
| 账号 ID | `63efba5a000000001001c0e3` |
| 去重后笔记 | 675 篇 |
| 原始采集记录 | 676 条，包含 1 条重复置顶笔记 |
| 图片 | 3,793 张 |
| 图片格式 | JPG 2,346 张，WebP 1,447 张 |
| 图片大小 | 383,529,726 字节，约 365.8 MiB |
| 图片缺失 / 解码损坏 | 0 / 0 |

笔记数据保存了标题、正文、话题、发布时间和原始链接。

## 数据入口

- [去重后的笔记数据](downloads/63efba5a000000001001c0e3/notes.json)
- [图片目录](downloads/63efba5a000000001001c0e3/xhs/media/)，按笔记 ID 分文件夹
- [原始采集记录](downloads/63efba5a000000001001c0e3/xhs/json/creator_contents_2026-11-08.json)
- [主页资料](downloads/63efba5a000000001001c0e3/profile.json)
- [采集笔记 ID 清单](downloads/63efba5a000000001001c0e3/note_ids.json)
- [完整性核验报告](downloads/63efba5a000000001001c0e3/download_report.json)

## 本地核验

安装 `uv` 后，在仓库根目录运行：

```sh
uv run --project MediaCrawler --frozen python verify_download.py
```

核验脚本对照笔记 ID 清单和主页数量，检查每篇笔记的图片序号，并逐张解码图片；结果写入 `download_report.json`。核验通过时退出码为 `0`。

## 采集工具

`MediaCrawler/` 保存了实际使用的源码快照，包含网页状态解析、按页续传和登录态保存修复。上游为 [NanmiCoder/MediaCrawler](https://github.com/NanmiCoder/MediaCrawler)，固定提交和本地修改摘要见 [UPSTREAM.json](UPSTREAM.json)，源码许可见 [MediaCrawler/LICENSE](MediaCrawler/LICENSE)。

准备 `uv`、Node.js 和 Chrome 后，可在仓库根目录运行：

```sh
./download_creator.sh
```

指定开始页：

```sh
./download_creator.sh 10
```

采集配置为下载笔记媒体、单并发、JSON 保存和关闭评论采集。登录态、浏览器缓存与运行日志保存在采集机器本地。
