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
| deduplicate | Loại item trùng URL giống hệt nhau, giữ nguồn đầu tiên | **có** |
| get_yahoo_finance_data | Lấy giá niêm yết Yahoo theo ticker, kèm currency và thời điểm báo giá; có thể trễ | **có** |

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

---

# PHẦN B — Chi tiết / Bằng chứng

## B1. Version Evidence

Bản nộp dùng bốn nhãn v0, v1, v2, v3. V3 là artifact cuối đã chọn; chuẩn hóa tên không thay đổi thời điểm chạy, tool calls, results, hash hay điểm đo. Base và group được chấm riêng. Provider/model: OpenRouter / openai/gpt-4o-mini.

| Version / suite | Changed Artifact | Hypothesis / Interpretation | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 / base | baseline | Đo starter gốc | — | 0.70 | `runs/v0_B_base_openrouter_20261110T101810112659.json` |
| v1 / base | system_prompt.md | Hỏi lại thay vì đoán account/URL | 0.70 | 0.75 | `runs/v1_B_base_openrouter_20261110T111643249913.json` |
| v2 / base | tools.yaml | clarify bắt buộc response_type | 0.75 | 0.90 | `runs/v2_B_base_openrouter_20261110T113708805712.json` |
| v3 / base | prompt + YAML + tool integration | Làm rõ routing, định danh và trạng thái xác nhận | 0.90 | 1.00 | `runs/v3_B_base_openrouter_20261110T123220151282.json` |
| v3 / group | cùng artifact v3 | Kiểm tra 10 case và tool mới | — | 1.00 | `runs/v3_B_group_openrouter_20261110T123259318689.json` |

**V3: base 20/20, group 10/10; routing/arguments/multi-turn đều 100%; provider errors 0; pytest 116 passed, 0 failed, 0 skipped.** Điểm phản ánh bộ case hiện tại, không khẳng định đúng mọi tình huống.

So v2 với v3 là so sánh tổng thể vì tập tool đã mở rộng và prompt/declaration đã được hoàn thiện; không quy toàn bộ cải thiện cho một dòng sửa. Lần v1 lỗi kết nối có 0 measured cases được ghi riêng và không coi là điểm chất lượng.

Model/read tools chạy thật. Send được mô phỏng và được đánh dấu trong run JSON; không phải bằng chứng giao tin Telegram. Kiểm tra tool results cuối không có error dict: `analysis/v3_tool_errors.json`.

## B2. Failure Analysis

Chi tiết: `analysis/v0_vs_v1.csv`, `analysis/v1_vs_v2.csv`, `analysis/v2_vs_v3_base.csv`.

| Case / phiên bản phát hiện | Lỗi | Cách xử lý / kết quả cuối |
|---|---|---|
| R10/R11 v0 | Đoán account/URL | Hỏi clarify khi thực sự thiếu; bắt buộc response_type; v3 PASS |
| R08/R14 v0 | Gọi tool cho toán/code ngoài phạm vi | Làm rõ phạm vi, trả text không tool; v3 PASS |
| R13 v0/v1 | Sai query/topic của lookup | Làm rõ routing và convention args; v3 PASS |
| M02 v1/v2 | social_search thay lookup news/day | Giữ nguồn, topic, timeframe khi đổi chủ đề; v3 PASS |
| R12 v0–v2 | Chưa hỏi xác nhận đúng trước gửi | Ưu tiên nhánh xác nhận và yes_no; v3 PASS |
| Định danh tài khoản / v3 | Phân biệt tên đã biết với tài khoản chưa được nêu | Cho phép ánh xạ tên đã biết, cấm placeholder; v3 PASS |
| Xác nhận đã có / v3 | Không hỏi lặp sau khi user duyệt đúng nội dung | send đúng text và confirmed=true trong eval mô phỏng; v3 PASS |

## B3. Team Eval Cases

10 case: 5 single + 5 multi; **v3 đạt 10/10**. Run `runs/v3_B_group_openrouter_20261110T123259318689.json`.

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| team_case_01_lookup_news_args | Kiểm tra model bóc tách đúng topic='news' thay vì nhét chữ 'news' vào query (Khắc phục lỗi v0). | lookup | PASS |
| team_case_02_missing_url_clarify | Kiểm tra model dừng lại dùng clarify hỏi URL thay vì tự bịa URL để gọi fetch. | clarify | PASS |
| team_case_03_missing_handle_timeline | User chưa xác định tài khoản nào và lịch sử không có tài khoản; agent phải gọi clarify hỏi lại, không tự chọn người. | clarify | PASS |
| team_case_04_deduplicate_sources | Route danh sách đã có tới tool mới deduplicate, không tìm kiếm; unit test kiểm tra dữ liệu và kết quả loại trùng. Ngoài phạm vi coding đã có base R14. | deduplicate | PASS |
| team_case_05_new_tool_finance_single | Gọi tool tài chính thật cho ticker GC=F, không nhầm vàng bán lẻ. Tool result cần có currency/as_of; eval tự động chỉ chấm routing/args. | get_yahoo_finance_data | PASS |
| team_case_06_send_guardrail_multiturn | Kiểm tra model chờ xác nhận. Lượt này chỉ được phép dùng clarify để hỏi lại, tuyệt đối chưa gọi send. | clarify | PASS |
| team_case_07_send_confirmed_multiturn | Sau 3 lượt hội thoại và có lệnh 'đồng ý' rõ ràng, agent gọi tool send với confirmed=true. | send | PASS |
| team_case_08_fetch_resolved_multiturn | Kiểm tra model nhớ URL được cung cấp ở lượt 2 để ghép vào argument của tool fetch. | fetch | PASS |
| team_case_09_social_search_multiturn | Kiểm tra trí nhớ ngắn hạn. Model phải cập nhật search_type='Top' theo yêu cầu lượt 2. | social_search | PASS |
| team_case_10_new_tool_finance_multiturn | Kiểm tra model gọi tool mới đúng lúc khi ngữ cảnh hội thoại kéo dài 2 lượt. | get_yahoo_finance_data | PASS |

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
| Tool unit tests (`tests/`) | `pytest` output |  |  |

Tool unit tests: số test đã viết, số bug tìm được trong tool có sẵn (nếu có), và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

### Kết quả bổ sung tool và unit test

- Đã triển khai `get_yahoo_finance_data` và đăng ký `deduplicate` (tổng 12 tool), có TOOL.md và YAML đồng bộ.
- Pytest: **116 passed, 0 failed, 0 skipped**. Các test dùng dữ liệu giả lập, chặn HTTP thật; không diễn giải dữ liệu mock thành giá thị trường.
- Kiểm tra tài chính gồm request/response mapping, ticker lỗi, timeout/HTTP 429, thiếu price/currency/timestamp; lỗi trả dict thay vì bịa giá.
- Deduplicate có test giữ thứ tự/bản đầu, input lỗi, URL lỗi và item thiếu URL; chỉ so URL giống hệt.
- Group eval gọi Yahoo thật thành công cho GC=F và NVDA. Tool trả currency/as_of; quote có thể thuộc phiên trước, không đảm bảo realtime.
- Case xác nhận gửi của v3 đã PASS; send trong eval được mô phỏng, không phải bằng chứng giao tin Telegram thật.
- CSV phân tích: `analysis/v3_group_results.csv`.

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
