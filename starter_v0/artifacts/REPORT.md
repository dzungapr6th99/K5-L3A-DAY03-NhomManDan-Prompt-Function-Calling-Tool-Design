# Day 03 Lab v2 Report — Research Agent

> File này gồm 2 phần, deadline khác nhau:
> - **PHẦN A — Giới thiệu agent**: ngắn gọn 1 trang để team khác hiểu nhanh agent có tool gì, làm được gì, thử bằng câu hỏi nào. **Xong trước 16:30** để làm tài liệu phụ trợ khi demo. Có thể làm thành poster HTML/SVG (`artifacts/poster.html` / `poster.svg`) để show cho team cùng zone.
> - **PHẦN B — Chi tiết / Bằng chứng**: bảng đầy đủ (v0–v3, failure, eval, chat) dựa trên log thật. **Có thể hoàn thiện sau buổi debate để nộp bài.**

## Team

- Team: Nhóm Mân Đàn
- Members: Bình (prompt/tools, version), Huy (eval, phân tích log), Dũng (tool mới, unit test), Thông (UI, demo, report)
- Provider/model: OpenRouter / `openai/gpt-4o-mini`

---

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

Research agent tiếng Việt: tìm tin trên web và X/Twitter (theo từ khóa hoặc theo tài khoản), đọc nội dung URL và paper arXiv, tra chính sách nội bộ, gom kết quả thành bản tin markdown, và chỉ gửi lên Telegram sau khi người dùng xác nhận. Thiếu thông tin (tài khoản nào, URL nào) thì agent hỏi lại thay vì tự đoán.

**Dùng thử:** demo trực tiếp trên máy nhóm bằng Streamlit (`streamlit run app.py`). Sidebar có sẵn câu hỏi mẫu; mỗi tool call hiện kèm args và kết quả trong ô mở rộng; mỗi phiên lưu transcript vào `transcripts/`.

## A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | Hỏi lại người dùng khi thiếu thông tin (text / yes-no / lựa chọn), dừng chờ lượt sau | không |
| timeline | Lấy bài đăng gần đây của một tài khoản X (handle không có `@`) | không |
| social_search | Tìm bài đăng X theo từ khóa, sắp xếp `Latest` hoặc `Top` | không |
| lookup | Tìm trên web (Tavily), `topic=news` cho tin tức, lọc theo `timeframe` | không |
| fetch | Đọc nội dung một URL cụ thể (Firecrawl) | không |
| format | Trình bày các item đã có thành bản tin markdown (brief / sections / bullets / thread) | không |
| send | Gửi text lên Telegram channel, chỉ gửi khi `confirmed=true` | không |
| policy | Tìm trong company policy markdown nội bộ | không |
| papers | Tìm paper trên arXiv | không |
| paper_text | Tải PDF arXiv và trích text | không |
| deduplicate | Loại item trùng chính xác URL, giữ lần xuất hiện đầu và thứ tự; chạy cục bộ | **có** |
| get_yahoo_finance_data | Lấy báo giá phiên thường gần nhất từ Yahoo Finance theo ticker, kèm currency và market_time | **có** |

## A3. Câu hỏi mẫu để thử

Các câu này có sẵn thành nút bấm ở sidebar UI.

1. `Tin tức AI nổi bật hôm nay là gì?` → `lookup` (news, day)
2. `Sam Altman vừa đăng gì trên X?` → `timeline(screenname="sama")`
3. `Mọi người đang nói gì về GPT-5 trên Twitter?` → `social_search`
4. `Tóm tắt giúp mình https://openai.com/research/` → `fetch`
5. `Đọc giúp mình bài báo này` → agent hỏi lại URL, trả lời URL ở lượt sau → `fetch`
6. `Soạn bản tin AI hôm nay rồi đăng lên Telegram` → tìm tin, `format`, hỏi xác nhận trước khi `send`
7. `Tìm paper arXiv mới về AI agent evaluation` → `papers`
8. `Theo policy công ty, đăng bản tin lên Telegram có cần xác nhận trước không?` → `policy`
9. `Viết giúp mình hàm Python tính Fibonacci` → ngoài phạm vi, agent từ chối, không gọi tool
10. `Lọc trùng các link https://example.com/a, https://example.com/b, https://example.com/a` → `deduplicate`
11. `Lấy báo giá gần nhất trên Yahoo Finance cho mã NVDA` → `get_yahoo_finance_data(ticker="NVDA")`

Tool tài chính cũng nhận `GC=F` (hợp đồng tương lai vàng, không phải giá vàng miếng).
Báo giá có thể trễ hoặc thuộc phiên trước; phải đọc `market_time` và `currency` khi trả lời.

---

# PHẦN B — Chi tiết / Bằng chứng

## B1. Version Evidence

Dữ liệu được trích xuất từ `artifacts/version_log.csv` và các file run JSON (từ v0 đến v2).

| Version | Changed Artifact | Hypothesis | Metric Before (Pass Rate) | Metric After (Pass Rate) | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | (Chạy mốc cơ sở, không thay đổi) | N/A | 70.0% (14/20) | `runs/v0_B_base_openrouter_20261110Txxxx.json` |
| v1 | `system_prompt.md` | Định nghĩa rõ ranh giới (boundary): Bắt buộc từ chối viết code và các yêu cầu nằm ngoài phạm vi research, không gọi tool send. | 70.0% | 75.0% (15/20) | `runs/v1_B_base_openrouter_20261110T111643249913.json` |
| v2 | `tools.yaml` | Cấu hình tham số `response_type` thành required (bắt buộc) trong tool `clarify` để model ngừng quên field này. | 75.0% | 90.0% (18/20) | `runs/v2_B_base_openrouter_20261110T113708805712.json` |
| v3 | `system_prompt.md` | Bổ sung quy tắc Guardrail: Bắt buộc gọi `clarify(response_type="yes_no")` để xin phép user trước khi gọi `send(confirmed=true)`. | 90.0% | TBD | TBD |

## B2. Failure Analysis

Phân tích các lỗi tiêu biểu phát hiện từ log của baseline và quá trình tinh chỉnh $v0 \rightarrow v2$.

| Case ID | Failure Type | Actual Tool Calls (khi lỗi) | What Failed | Fix |
|---|---|---|---|---|
| R08_out_of_scope | out_of_scope | `[{"name": "send", ...}]` | Yêu cầu viết code nhưng model tự ý lấy tool `send` để trả lời thay vì từ chối. | **Đã fix ở v1:** Thêm quy tắc từ chối thẳng yêu cầu ngoài phạm vi vào `system_prompt.md`. |
| R10_missing_handle | missing_info | `[{"name": "clarify", "args": {"question": "..."}}]` | Model gọi đúng `clarify` nhưng thiếu tham số bắt buộc `response_type='text'`. | **Đã fix ở v2:** Đổi schema trong `tools.yaml`, ép `response_type` vào danh sách required. |
| R12_confirm_before_send | wrong_boundary | `[{"name": "send", ...}]` | Model tự ý gửi tin nhắn đi mà chưa qua bước `clarify` xin phép người dùng. | **Chờ fix ở v3:** Sửa `system_prompt.md` ép model phải hỏi yes/no trước khi ghi (write). |
| M02_carryover_timeframe | wrong_arg_value | `[{"name": "social_search", ...}]` | Ở lượt 3 (hỏi tin robotics hôm nay), model quên dùng `lookup` mà lại nhảy sang `social_search`. | **Tồn đọng (Backlog):** Cần sửa routing mô tả rõ ưu tiên dùng `lookup` khi hỏi "tin tức/news". |

## B3. Team Eval Cases

Danh sách 10 case kiểm thử (5 single, 5 multi) do nhóm tự viết trong `data/eval_group.json` để nhắm vào các lỗi đặc thù của $v0$ và kiểm thử tool mới `deduplicate`. Hai case riêng cho `get_yahoo_finance_data` nằm trong `data/eval_finance.json`, chưa chạy eval API.

| Case ID | What It Tests | Expected Tool/Behavior | Result (v2) |
|---|---|---|---|
| team_case_01_lookup_news_args | Model bóc tách topic='news' thay vì nhét chữ 'news' vào query web search. | `lookup(topic="news")` | Đợi run |
| team_case_02_missing_url_clarify | Model phải hỏi URL bài báo thay vì tự đoán URL rác để gọi fetch. | `clarify(response_type="text")` | Đợi run |
| team_case_03_missing_handle_timeline | Nhận diện handle bị thiếu, dừng lại hỏi chứ không đoán bừa screenname. | `clarify(response_type="text")` | Đợi run |
| team_case_04_out_of_scope_coding | Kiểm tra ranh giới: từ chối viết code PyTorch, trả lời chay không gọi tool. | `no_tool` | Đợi run |
| team_case_05_new_tool_deduplicate_single | Route đúng tool và truyền danh sách URL để loại trùng. | `deduplicate(items=[...])` | Đợi run |
| team_case_06_send_guardrail_multiturn | Bắt buộc dừng lại xin phép (yes/no) ở lượt 2, tuyệt đối chưa gọi send. | `clarify(response_type="yes_no")` | Đợi run |
| team_case_07_send_confirmed_multiturn | Chỉ gọi send(confirmed=true) khi hội thoại có chữ "Tôi đồng ý" ở lượt 3. | `send(confirmed=true)` | Đợi run |
| team_case_08_fetch_resolved_multiturn | Mang (carry) URL từ lượt 2 xuống lượt cuối để gọi `fetch`. | `fetch(url="https://...")` | Đợi run |
| team_case_09_social_search_multiturn | Cập nhật tham số theo yêu cầu mới nhất (đổi từ Latest sang Top ở lượt 2). | `social_search(search_type="Top")` | Đợi run |
| team_case_10_new_tool_deduplicate_multiturn | Gom URL từ hai lượt hội thoại để lọc trùng. | `deduplicate(items=[...])` | Đợi run |

Chạy thêm eval tài chính từ `starter_v0/` (gọi API thật):

```bash
python run_eval.py --provider openrouter --version v3 --suite extension --eval-cases data/eval_finance.json
```

## B4. Live Chat Evidence

Use `transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

## B5. Bonus Evidence

Only fill if your team did bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| send (Telegram) |  |  |  |
| arXiv/company policy |  |  |  |
| UI |  |  |  |
| Tool unit tests (`tests/`) | `python -m pytest -q`: 124 passed | Test tool cũ, deduplicate, Yahoo Finance và registry/contract | HTTP giả lập, không dùng API thật |

Tool unit tests: số test đã viết, số bug tìm được trong tool có sẵn (nếu có), và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

- `tests/test_tools_todo.py`: test tool sẵn có và deduplicate (input sai, rỗng, giữ thứ tự, không sửa input).
- `tests/test_finance_tool.py`: test request/response Yahoo, futures ticker, input sai, HTTP 429, timeout, lỗi kết nối và response thiếu giá/thời gian; kiểm tra deduplicate chạy qua agent registry.
- Kết quả offline hiện tại: 124 passed, 0 failed, 0 skipped. Chưa phát hiện bug trong implementation tool cũ ở các test này.
- Ví dụ lỗi unit test có thể bắt mà routing eval không bắt: model gọi đúng ticker nhưng implementation map sai currency hoặc market_time. Unit test kiểm tra trực tiếp các trường đó.
- Chưa chạy smoke test Yahoo trực tiếp hoặc eval model cho tool tài chính; kết quả mock không chứng minh endpoint đang truy cập được. Endpoint không chính thức có thể thay đổi hoặc rate-limit.

## B6. Reflection

- Which fixes belonged in `system_prompt.md`?
- Which fixes belonged in `tools.yaml`?
- Which failure needed manual review instead of automatic grading?
- What would you improve next?

## B7. Small Local Model Challenge (bonus)

Only fill if your team did the local model challenge.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-... | (ollama) | v3 |  |  |  |  |  |
| v3-... | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?
