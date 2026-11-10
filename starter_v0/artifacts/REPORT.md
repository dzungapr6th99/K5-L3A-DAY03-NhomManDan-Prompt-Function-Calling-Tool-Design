# Day 03 Lab v2 Report — Research Agent

Báo cáo kết quả Research Agent của nhóm Mân Đàn, gồm giới thiệu sản phẩm, quá trình tối ưu và bằng chứng kiểm tra.

## Team

- Team: Nhóm Mân Đàn
- Members: Bình (prompt/tools, version), Huy (eval, phân tích log), Dũng (tool mới, unit test), Thông (UI, demo, report)
- Provider/model: OpenRouter / `openai/gpt-4o-mini`

---

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

Research agent tiếng Việt: tìm tin trên web và X/Twitter (theo từ khóa hoặc theo tài khoản), đọc nội dung URL và paper arXiv, tra chính sách nội bộ và kiến thức nền trên Wikipedia, gom kết quả thành bản tin markdown, và chỉ gửi lên Telegram sau khi người dùng xác nhận. Thiếu thông tin (tài khoản nào, URL nào) thì agent hỏi lại thay vì tự đoán.

**Dùng thử:** demo local bằng `.\START_LOCAL.ps1` rồi mở `http://127.0.0.1:8501`.
Hướng dẫn chạy: `RUN_LOCAL.md`.
UI chạy snapshot v0–v5, mặc định v5 cuối; chỉ hiện điểm khi run khớp hash artifact (chấp nhận cả file LF và CRLF, vì run chạy trên Windows còn repo checkout trên macOS/Linux là LF).
Tab **Chat**: lịch sử chat, xem arguments/results, câu hỏi mẫu, đổi version và lưu transcript. Tab **Bảng điểm**: bộ test khởi đầu (20 case base) và bộ test mở rộng (nhóm tự viết, research extension, tool date, tool wikipedia) của version đang chọn.
UI đã được kiểm tra bằng Streamlit AppTest và HTTP 200 cho trang chính/health.

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
| date | Ngày hiện tại theo giờ Việt Nam, luôn kèm tuần trước / tuần này / tuần sau (Thứ Hai → Chủ Nhật); `offset_days` cho ngày lệch khác (hôm qua -1, 2 tuần trước -14) | **có** |
| wikipedia | Tóm tắt đầu trang Wikipedia (`vi`/`en`, không cần API key) cho câu hỏi kiến thức nền "X là gì / là ai"; báo `not_found` / `ambiguous` thay vì đoán | **có** (v4) |

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

Sáu nhãn nộp: v0–v3 là phần lab chính (v3 có **13 tool**, gồm 3 tool mới); v4 thêm tool mới thứ 4 `wikipedia` (bonus "hơn 3 tool"), v5 sửa case E06 bị tụt ở v4. **Bản nộp cuối là v5: 14 tool, gồm 4 tool mới.** Mỗi snapshot và các run của nó có cùng full hash.

| Version / suite | Changed Artifact | Hypothesis / interpretation | Before | After | Run JSON |
|---|---|---|---:|---:|---|
| v0 / base | starter baseline | Đo trước tối ưu | — | 70% | `runs/v0_B_base_openrouter_20261110T101810112659.json` |
| v1 / base | prompt | Hỏi lại thay vì đoán identifier | 70% | 75% | `runs/v1_B_base_openrouter_20261110T111643249913.json` |
| v2 / base | schema clarify | response_type bắt buộc | 75% | 90% | `runs/v2_B_base_openrouter_20261110T113708805712.json` |
| v3 / base | Final prompt + declarations + 13 tool integration | Routing, preconditions và dữ liệu thực | 90% | 20/20 (100%) | `runs/v3_B_base_openrouter_20261110T143325569018.json` |
| v3 / group | Final prompt + declarations + 13 tool integration | Routing, preconditions và dữ liệu thực | — | 10/10 (100%) | `runs/v3_B_group_openrouter_20261110T143410949838.json` |
| v3 / date extension | Final prompt + declarations + 13 tool integration | Routing, preconditions và dữ liệu thực | — | 3/3 (100%) | `runs/v3_B_extension_openrouter_20261110T143438392011.json` |
| v3 / research extension | Final prompt + declarations + 13 tool integration | Routing, preconditions và dữ liệu thực | — | 10/10 (100%) | `runs/v3_B_extension_openrouter_20261110T143526294257.json` |
| v4 / base | tool `wikipedia` + YAML + 1 dòng routing | Tool kiến thức nền không làm hỏng routing cũ | 100% | 20/20 (100%) | `runs/v4_B_base_openai_20261110T162659299468.json` |
| v4 / group | như trên | như trên | 100% | 10/10 (100%) | `runs/v4_B_group_openai_20261110T162735543072.json` |
| v4 / research extension | như trên | như trên | 100% | **9/10 (90%)** | `runs/v4_B_extension_openai_20261110T162810368821.json` |
| v4 / date extension | như trên | như trên | 100% | 3/3 (100%) | `runs/v4_B_extension_openai_20261110T162826795733.json` |
| v4 / wikipedia extension | như trên | Câu kiến thức nền → `wikipedia`; tin tức vẫn `lookup` | — | 3/3 (100%) | `runs/v4_B_extension_openai_20261110T162843970741.json` |
| v5 / base | prompt: 1 câu | Bản tin luôn cần `lookup(topic=news)` cùng lượt, kể cả khi user bảo kiểm tra policy trước | 100% | 20/20 (100%) | `runs/v5_B_base_openai_20261110T165452666998.json` |
| v5 / group | như trên | như trên | 100% | 10/10 (100%) | `runs/v5_B_group_openai_20261110T165517496503.json` |
| v5 / research extension | như trên | như trên | 90% | **10/10 (100%)** | `runs/v5_B_extension_openai_20261110T165540372874.json` |
| v5 / date extension | như trên | như trên | 100% | 3/3 (100%) | `runs/v5_B_extension_openai_20261110T165547136771.json` |
| v5 / wikipedia extension | như trên | như trên | 100% | 3/3 (100%) | `runs/v5_B_extension_openai_20261110T165552950134.json` |

**v4 làm tụt E06** ("Làm bản tin AI hôm nay, nhưng kiểm tra policy công ty về source/citation trước"): cả 3 lần chạy chỉ gọi `policy`, không gọi `lookup`; v3 đạt cả 3 lần. Bỏ dòng routing hoặc rút mô tả wikipedia còn 1 câu vẫn trượt (2/2 mỗi cách), nên nguyên nhân là việc thêm tool thứ 14. Một câu chung "first/before không phải lý do để chờ" không sửa được (0/2); câu cụ thể "bản tin luôn cần `lookup(topic=news)` cùng lượt" sửa được (2/2 thử, rồi 10/10 ở run chính thức v5).

Artifact cuối: `v5+p12885e0c0bf8+t9c8833e2d8b9`.
Prompt SHA-256: `12885e0c0bf887823732cb40f468ee7bdca2061b27594548d5f9ca8aacd3fc53`.
Tools SHA-256: `9c8833e2d8b995ae11202c19fa1b05a73cef18b71129289666933ddba75708a2`.
(v3: `v3+p840cbe5577ea+t82c24d53675e`, hash tính trên file CRLF của máy Windows; v4/v5 tính trên file LF.)

**v5: base 20/20, group 10/10, research extension 10/10, date 3/3, wikipedia 3/3; 0 provider error. Unit/UI tests: 153 passed, 0 failed, 0 skipped.**

Dùng `gpt-4o-mini` cho mọi version và các tool đọc dữ liệu qua API: v0–v3 gọi qua OpenRouter (`openai/gpt-4o-mini`); v4–v5 gọi thẳng OpenAI (`gpt-4o-mini`) vì key OpenRouter hết credit, cùng model nên vẫn so được. Kết quả 43 case cuối của v3 được lưu trong run JSON; tool results không có error dict (`analysis/v3_tool_errors.json`).

V3 hoàn thiện prompt, declaration và tích hợp 13 tool. Bản nộp giữ các run chính thức được trích dẫn trong bảng, với hash khớp artifact tương ứng.

Base/group kiểm tra tên tool và arguments. B4 ghi kết quả kiểm tra hội thoại qua transcript.

## B2. Failure Analysis

Chi tiết: `analysis/v0_vs_v1.csv`, `analysis/v1_vs_v2.csv`, `analysis/v2_vs_v3_base.csv`.

| Case / phiên bản phát hiện | Lỗi | Cách xử lý / kết quả cuối |
|---|---|---|
| R10/R11 v0 | Đoán account/URL thay vì hỏi lại. |  Ép buộc model gọi `clarify` khi thiếu thông tin; bắt buộc schema `response_type` (v2). Kết quả: v3 PASS. |
| R08/R14 v0 | Gọi tool `send` bừa bãi cho yêu cầu toán/code. |  Thêm Guardrail ranh giới công việc vào Prompt, bắt buộc từ chối và không dùng tool. Kết quả: v3 PASS. |
| R13 v0/v1 | Lỗi sai tham số query/topic của lookup. |  Làm rõ Convention Arguments trong mô tả YAML để model biết cách tách chuỗi. Kết quả: v3 PASS. |
| M02 v1/v2 | Hội thoại nhiều lượt bị lạc sang tool `social_search`. |  Bổ sung rule định hướng context multi-turn: giữ nguồn (web), chủ đề, timeframe (day) khi đổi nội dung tìm. Kết quả: v3 PASS. |
| R12 v0–v2 | Gọi `send` trước bước xác nhận. |  Ưu tiên nhánh xác nhận (Guardrail cứng): Bắt buộc dùng `clarify(response_type="yes_no")` trước mọi hành động write/send. Kết quả: v3 PASS. |
| Định danh tài khoản / v3 | Phân biệt tên đã biết với tài khoản chưa được nêu. |  Cho phép ánh xạ tên đã biết, hỏi lại khi tài khoản chưa được xác định. Kết quả: v3 PASS. |
| Xác nhận đã có / v3 | Không hỏi lặp sau khi user duyệt đúng nội dung. |  Nếu có text đồng ý, kiểm tra lời gọi `send(confirmed=true)` với đúng nội dung được duyệt. Kết quả: v3 PASS. |

## B3. Team Eval Cases

10 case: 5 single + 5 multi, giữ nguyên kỳ vọng khi hoàn thiện bản cuối. Run `runs/v3_B_group_openrouter_20261110T143410949838.json`.

| Case ID | What it tests | Expected | Result |
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

Tool date có thêm 3 case trong `data/eval_date.json`: hỏi ngày hôm nay, hôm qua (-1), hai tuần trước (-14); cả 3 PASS. Các ngày thực tế được kiểm thử bằng clock cố định trong unit test.

Tool wikipedia (v4) có 3 case riêng trong `data/eval_wikipedia.json` để `eval_group.json` giữ đúng 5 single + 5 multi: hỏi "Anthropic là công ty gì? Tra Wikipedia" (tiếng Việt), "Who is Demis Hassabis?" (tiếng Anh), và một case đối chứng "tin mới nhất về Anthropic hôm nay" phải ở lại `lookup`. Kết quả: xem B1.

## B4. Live Chat Evidence

Phiên 7 lượt trên đúng artifact cuối: `transcripts/v3_openrouter_20261110T143528494225.transcript.json`.

Chạy 7 lượt qua `chat.py.main` bằng `scripts/chat_demo_safe.py`, dùng OpenRouter và các tool đọc dữ liệu. Transcript có hash khớp snapshot và eval cuối.

| Turn | User request | Tool calls thực tế | Status | Quan sát |
|---|---|---|---|
| 1 | Tin tức AI nổi bật hôm nay là gì? | lookup | answered | Tra tin web news/day và trả nguồn. |
| 2 | Đọc giúp mình bài báo này | — | answered | Hỏi người dùng bổ sung URL bằng text. |
| 3 | https://openai.com/research/ | fetch | answered | Dùng URL bổ sung từ lượt sau, đọc bằng fetch. |
| 4 | Hôm nay là ngày nào, thứ mấy theo giờ Việt Nam? | date | answered | Gọi date, trả ngày/thứ theo giờ Việt Nam. |
| 5 | Chỉ lọc trùng URL trong danh sách đã có này, không tìm thêm: [{"title":"A","url":"https://example.com/a"},{"title":"A copy","url":"https://example.com/a"},{"title":"B","url":"https://example.com/b"}] | deduplicate | answered | Loại 1 URL trùng, giữ 2 nguồn. |
| 6 | Đăng lên Telegram câu này: Bản tin AI hôm nay đã sẵn sàng. | clarify | waiting_for_user | clarify yes_no đúng nội dung; dừng chờ, chưa gửi. |
| 7 | Thôi không gửi nữa, cảm ơn. | — | answered | Hủy đúng, không gọi send. |

Đã kiểm tra 7 lượt gồm tìm tin, bổ sung URL, tra ngày, lọc trùng, xác nhận và hủy gửi. 7 lượt hoàn tất, không có provider/tool error.

## B5. Tool tests, UI và bonus

| Hạng mục | Evidence | Kết quả |
|---|---|---|
| Unit + UI tests | `analysis/pytest.txt`, `tests/` | 139 PASS ở bản v3; sau khi thêm wikipedia và sửa UI: 153 PASS, 0 failed/skipped; kiểm tra contract, input và xử lý kết quả |
| Streamlit local | `analysis/ui_verification.json`, `tests/test_ui.py`, `START_LOCAL.ps1` | Trang chính/health HTTP 200; AppTest kiểm tra load v3, đổi version, chat, transcript, chat mới |
| 4 tool mới (bonus "hơn 3 tool") | `tools/deduplicate/`, `tools/yahoo_finance/`, `tools/date/`, `tools/wikipedia/` | Code, TOOL.md, registry và YAML đồng bộ; mỗi tool có ít nhất 3 test (`tests/test_tool_wikipedia.py`: 8 test gồm URL/User-Agent, 404 → `not_found`, trang định hướng, input sai, lỗi mạng) và eval case route tới (wikipedia: `data/eval_wikipedia.json`) |
| UI: bảng điểm theo bộ test | `app.py`, `tests/test_ui.py` | Tab Bảng điểm tách bộ khởi đầu / mở rộng; sửa lỗi bảng điểm báo "Chưa đo" trên macOS/Linux (run Windows hash CRLF, checkout LF) và lỗi các bộ cùng `suite=extension` đè nhau; có regression test |
| arXiv / company policy | `runs/v3_B_extension_openrouter_20261110T143526294257.json` | 10/10 đúng routing và arguments |
| Calendar extension | `runs/v3_B_extension_openrouter_20261110T143438392011.json` | 3/3; tests cố định clock kiểm tra múi giờ, tuần và offset |
| Telegram | `transcripts/v3_openrouter_20261110T143528494225.transcript.json`, group 06/07 | Kiểm tra lời gọi xác nhận/hủy và arguments của send; không gửi tin lên Telegram: Telegram bắt trả phí SMS khi đăng ký tài khoản bằng số Việt Nam, nhóm không ai có tài khoản nên `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID` để trống. Một phiên live riêng (không nộp, nhóm giữ một transcript) cho thấy lượt "Có, gửi đi" gọi đúng 1 lần `send(confirmed=true)`, tool trả lỗi thiếu token và agent báo gửi lỗi chứ không nhận vơ đã gửi |

Đã bổ sung 2 regression test cho console Windows cp1252: log gọi tool và phản hồi tiếng Việt/emoji không làm dừng agent; UI khởi động ở UTF-8.

Tool tests kiểm tra request, mapping kết quả, input sai, HTTP 429/timeout, dữ liệu giá, lọc trùng và lịch tuần. Đã sửa lỗi `date(offset_days=inf)` và bổ sung regression cho ±inf.


## B6. Reflection

- **System prompt:** Đã sửa phạm vi research, quy tắc hỏi lại khi thiếu dữ liệu, xác nhận trước send và giữ ngữ cảnh nhiều lượt.
- **Tools.yaml:** Đã bổ sung response_type vào required của clarify, làm rõ topic/timeframe/search_type, điều kiện dùng timeline và các tool mới.
- **Đánh giá thủ công:** Đã đọc tool calls/results và transcript; ghi nhận lượt 2 hỏi URL bằng text thay vì gọi clarify.
- **Hướng cải tiến:** Thêm eval chạy nguyên hội thoại, kiểm tra việc hủy/đổi yêu cầu và chất lượng nội dung tóm tắt.

## B7. Small Local Model Challenge (bonus)

Ollama 0.40 trên MacBook M1 16 GB, 2 model 3B có tag `tools`: `qwen2.5:3b` và `llama3.2:3b`. Chạy bộ base 20 case. Mốc là prompt/tools **v3** (snapshot `artifacts/versions/v3`, 13 tool) đúng như README; tool `wikipedia` của v4/v5 không đưa vào để so được với cloud v3. Bản local riêng: `artifacts/tools_local.yaml`, `artifacts/system_prompt_local.md`; snapshot từng vòng ở `artifacts/versions_local/`. Mọi run có dòng trong `version_log.csv`. Poster HTML/SVG không thực hiện.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---:|---:|---:|---:|---|
| v3 | gpt-4o-mini (OpenRouter) | v3 | 1.00 | 1.00 | 1.00 | 1.00 | `runs/v3_B_base_openrouter_20261110T143325569018.json` |
| v3-qwen3b | qwen2.5:3b (ollama) | v3 | 0.65 | 0.65 | 0.65 | 0.83 | `runs/v3-qwen3b_B_base_ollama_20261110T160639195922.json` |
| v3-llama3b | llama3.2:3b (ollama) | v3 | 0.37 (7/19 đo được; R12 treo) | 0.58 | 0.37 | 0.17 | `runs/v3-llama3b_B_base_ollama_20261110T163852778155.json` |
| v4-local-qwen3b | qwen2.5:3b (ollama) | prompt v3 + `tools_local.yaml` | 0.70 | 0.70 | 0.70 | 1.00 | `runs/v4-local-qwen3b_B_base_ollama_20261110T164101897585.json` |
| v4-local-llama3b | llama3.2:3b (ollama) | prompt v3 + `tools_local.yaml` | **0.65** | 0.65 | 0.65 | 0.83 | `runs/v4-local-llama3b_B_base_ollama_20261110T164244131650.json` |
| v5-local-qwen3b | qwen2.5:3b (ollama) | `system_prompt_local.md` (few-shot) + `tools_local.yaml` | 0.70 | 0.70 | 0.70 | 1.00 | `runs/v5-local-qwen3b_B_base_ollama_20261110T164426692671.json` |
| v5-local-llama3b | llama3.2:3b (ollama) | `system_prompt_local.md` (few-shot) + `tools_local.yaml` | 0.50 | 0.55 | 0.50 | 0.67 | `runs/v5-local-llama3b_B_base_ollama_20261110T164605090190.json` |
| v4-local-cloud | gpt-4o-mini (OpenAI) | v4-local | 0.90 | 0.95 | 0.90 | 0.83 | `runs/v4-local-cloud_B_base_openai_20261110T163002247385.json` |
| v5-local-cloud | gpt-4o-mini (OpenAI) | v5-local | 0.90 | 0.95 | 0.90 | 0.83 | `runs/v5-local-cloud_B_base_openai_20261110T163140114567.json` |

Hai vòng tối ưu, mỗi vòng một giả thuyết:

- **v4-local:** chỉ đổi `description` của tool (giữ nguyên tên, tham số, enum), mỗi mô tả ngắn theo khuôn USE / DO NOT USE / ví dụ args. Giả thuyết: model 3B chọn tool theo mô tả tool nhiều hơn theo prompt văn xuôi dài.
- **v5-local:** v4-local + 6 dòng few-shot "dạng yêu cầu → hành động" (URL → `fetch`, thiếu URL/handle → `clarify(text)`, Telegram → `clarify(yes_no)`, toán/code → không gọi tool).

Lỗi đặc thù của model nhỏ (đếm từ run JSON; số dạng qwen / llama; cloud v3 không mắc lỗi nào):

| Failure Pattern | Count (v3 → v4-local → v5-local) | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong tool (không có tool bịa tên) | qwen 1→0→0; llama 4→1→3 | R05 llama: `social_search("Elon Musk")` thay vì `timeline(elonmusk)` | mô tả USE / DO NOT USE (v4) | **Có** với llama; few-shot làm tệ lại |
| arg sai kiểu/enum (JSON vẫn parse được, `_invalid_json_arguments` = 0) | số dạng chuỗi: llama 4→0→0; enum sai: cả 2 model | llama v3 `limit: "10"`; qwen `lookup(topic="math")` ngoài enum; llama sinh text vỡ dấu `"ĝuyờnưng tin náy lùp Telegram"` | ghi "as an integer", liệt kê enum trong mô tả | Một phần: hết số dạng chuỗi, enum sai vẫn còn |
| không gọi tool / sinh text không dừng | qwen 1→1→1; llama 1 treo →0→0 | R11 qwen hỏi URL bằng text; R12 llama v3 sinh text tới timeout (~30 phút) | ví dụ few-shot | Không |
| bỏ qua `clarify` | qwen 2→2→2; llama 2→3→3 | R10: qwen v3 `timeline("your_twitter_screen_name")`, v4-local `timeline("elonmusk")` (chép đúng ví dụ trong mô tả), v5-local `timeline("twitter")`; R12: cả 2 model gọi `send(confirmed=false/null)` thay vì hỏi | mô tả clarify + few-shot | **Không**. `send` tự chặn khi chưa `confirmed=true` nên không có tin nào bị gửi |
| gọi tool khi không cần | qwen 2→2→2; llama 2→3→3 | R08 toán: `lookup(query="x^2", topic="math")`; R14 code: llama gọi `deduplicate`, qwen gọi `clarify` | few-shot "toán/code → không gọi tool" | Không |

- **Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?** Viết lại mô tả tool ngắn theo khuôn USE / DO NOT USE / ví dụ: llama 7/19 → **13/20** (multiturn 0.17 → 0.83), qwen 13 → 14/20. Few-shot trong prompt không giúp: qwen giữ 14, llama tụt 13 → 10 (prompt dài hơn, lại chọn sai tool ở R05/M01/M03: `social_search`, `fetch`, `clarify` thay vì `timeline`). Ví dụ args là con dao hai lưỡi: model 3B chép giá trị ví dụ vào args khi thiếu thông tin (handle `elonmusk` ở R10). Một lần thử phụ trên v3 cũ (trước khi nhóm làm lại v3, commit `727cf51`) thay ví dụ bằng placeholder `<...>` còn tệ hơn: qwen 13 → 9/20, vì placeholder không phải JSON hợp lệ nên model không gọi được tool. Cùng lần thử đó cũng ra xu hướng như trên (mô tả ngắn: llama 8 → 12; few-shot: qwen +1, llama −1).
- **Bản prompt tối ưu cho local chạy trên model cloud thì sao?** Tụt từ 20/20 xuống **18/20** ở cả v4-local và v5-local: R12 hỏi bằng `clarify(text)` thay vì `yes_no` (mô tả ngắn mất chi tiết "yes_no cả khi chưa có nội dung"), M06 vẫn gọi thêm `social_search` dù user đã bảo bỏ Twitter. Chưa tìm được một bản dùng tốt cho cả hai: cloud cần mô tả đầy đủ ranh giới, model 3B cần mô tả ngắn.
- **Khi nào nhóm sẽ chọn model local thay vì cloud?** Chỉ cho tra cứu đơn giản có đủ thông tin (tin web, tweet theo handle rõ ràng) khi dữ liệu không được rời máy hoặc phải chạy offline. Không dùng local cho luồng cần hỏi lại hay gửi Telegram: không bản local nào gọi `clarify` đúng ở R10/R11/R12. Tốc độ: mỗi model chạy 20 case trong khoảng 2–3 phút, nhưng chỉ một case sinh text không dừng (llama v3 ở R12) là kéo lần chạy lên 32 phút, vì client chờ timeout rồi thử lại.
