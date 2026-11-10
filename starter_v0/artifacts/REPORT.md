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

**Dùng thử:** demo local bằng `.\START_LOCAL.ps1` rồi mở `http://127.0.0.1:8501`.
Nhóm chủ động không nộp link public theo phạm vi đã thống nhất. Hướng dẫn đầy đủ: `RUN_LOCAL.md`.
UI chạy snapshot v0–v3, mặc định v3 cuối; chỉ hiện điểm khi run khớp hash artifact (có xử lý LF/CRLF).
Có lịch sử chat, xem arguments/results, câu hỏi mẫu, đổi version và lưu transcript.
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

Bốn nhãn nộp: v0, v1, v2, v3. Bản v3 cuối có **13 tool**, gồm 3 tool mới. Prompt/tools hiện hành, snapshot v3 và các run cuối dưới đây có cùng full hash. Không lấy điểm từ run lịch sử khác hash để gán cho bản hiện tại.

| Version / suite | Changed Artifact | Hypothesis / interpretation | Before | After | Run JSON |
|---|---|---|---:|---:|---|
| v0 / base | starter baseline | Đo trước tối ưu | — | 70% | `runs/v0_B_base_openrouter_20261110T101810112659.json` |
| v1 / base | prompt | Hỏi lại thay vì đoán identifier | 70% | 75% | `runs/v1_B_base_openrouter_20261110T111643249913.json` |
| v2 / base | schema clarify | response_type bắt buộc | 75% | 90% | `runs/v2_B_base_openrouter_20261110T113708805712.json` |
| v3 / base | Final prompt + declarations + 13 tool integration | Routing, preconditions và dữ liệu thực | 90% | 20/20 (100%) | `runs/v3_B_base_openrouter_20261110T143325569018.json` |
| v3 / group | Final prompt + declarations + 13 tool integration | Routing, preconditions và dữ liệu thực | — | 10/10 (100%) | `runs/v3_B_group_openrouter_20261110T143410949838.json` |
| v3 / date extension | Final prompt + declarations + 13 tool integration | Routing, preconditions và dữ liệu thực | — | 3/3 (100%) | `runs/v3_B_extension_openrouter_20261110T143438392011.json` |
| v3 / research extension | Final prompt + declarations + 13 tool integration | Routing, preconditions và dữ liệu thực | — | 10/10 (100%) | `runs/v3_B_extension_openrouter_20261110T143526294257.json` |

Artifact cuối: `v3+p840cbe5577ea+t82c24d53675e`.
Prompt SHA-256: `840cbe5577ea892139828e9501fe492bfd149291c28e88b5efb660afd6b8fcd7`.
Tools SHA-256: `82c24d53675e9f9acfc9aff61ba7df709c012561d77cd62dfd5f89446cc2e80a`.

**Base 20/20, group 10/10, date 3/3, research extension 10/10; 0 provider error. Unit/UI tests: 139 passed, 0 failed, 0 skipped.**

Model: OpenRouter / openai/gpt-4o-mini. Read tools chạy thật; send được mô phỏng và đánh dấu trong metadata. Không có error dict ở tool results của 43 case cuối (`analysis/v3_tool_errors.json`).

So v2–v3 là kết quả tổng thể: tập tool và nhiều quy tắc đã được hoàn thiện, không phải bằng chứng một chỉnh sửa đơn lẻ gây toàn bộ cải thiện. Bản nộp giữ run chính thức được trích dẫn cho từng version; các log thử nghiệm không dùng đã được dọn. Điểm bản cuối chỉ lấy từ các run khớp hash hiện hành.

Giới hạn chấm: base/group đánh giá tool calls/args; case cần tool dùng tool_choice=required. Chat live dùng lựa chọn tự động nên có thể hỏi bằng text thay vì clarify. Điểm 100% trên bộ case không chứng minh mọi hội thoại live đều đúng; xem B4/B6.

## B2. Failure Analysis

Chi tiết: `analysis/v0_vs_v1.csv`, `analysis/v1_vs_v2.csv`, `analysis/v2_vs_v3_base.csv`.

| Case / phiên bản phát hiện | Lỗi | Cách xử lý / kết quả cuối |
|---|---|---|
| R10/R11 v0 | Đoán account/URL thay vì hỏi lại. | **Xử lý:** Ép buộc model gọi `clarify` khi thiếu thông tin; bắt buộc schema `response_type` (v2). **Kết quả:** v3 PASS. |
| R08/R14 v0 | Gọi tool `send` bừa bãi cho yêu cầu toán/code. | **Xử lý:** Thêm Guardrail ranh giới công việc vào Prompt, bắt buộc từ chối và không dùng tool. **Kết quả:** v3 PASS. |
| R13 v0/v1 | Lỗi sai tham số query/topic của lookup. | **Xử lý:** Làm rõ Convention Arguments trong mô tả YAML để model biết cách tách chuỗi. **Kết quả:** v3 PASS. |
| M02 v1/v2 | Hội thoại nhiều lượt bị lạc sang tool `social_search`. | **Xử lý:** Bổ sung rule định hướng context multi-turn: giữ nguồn (web), chủ đề, timeframe (day) khi đổi nội dung tìm. **Kết quả:** v3 PASS. |
| R12 v0–v2 | Gửi `send` thẳng tay mà chưa xin phép. | **Xử lý:** Ưu tiên nhánh xác nhận (Guardrail cứng): Bắt buộc dùng `clarify(response_type="yes_no")` trước mọi hành động write/send. **Kết quả:** v3 PASS. |
| Định danh tài khoản / v3 | Phân biệt tên đã biết với tài khoản chưa được nêu. | **Xử lý:** Cho phép ánh xạ tên đã biết, cấm dùng placeholder giả mạo. **Kết quả:** v3 PASS. |
| Xác nhận đã có / v3 | Không hỏi lặp sau khi user duyệt đúng nội dung. | **Xử lý:** Nếu có text đồng ý, gọi thẳng `send(confirmed=true)` (được đánh dấu mô phỏng trong eval). **Kết quả:** v3 PASS. |

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

## B4. Live Chat Evidence

Phiên 7 lượt trên đúng artifact cuối: `transcripts/v3_openrouter_20261110T143528494225.transcript.json`.

Phiên chạy trực tiếp `chat.py.main` qua `scripts/chat_demo_safe.py`: input kịch bản do nhóm chuẩn bị, model/read tools là API thật, chỉ delivery Telegram được mô phỏng. Không sửa nội dung phản hồi hay giả lập kết quả research. Hash khớp snapshot và eval cuối.

| Turn | User request | Tool calls thực tế | Status | Quan sát |
|---|---|---|---|
| 1 | Tin tức AI nổi bật hôm nay là gì? | lookup | answered | Tra tin web news/day và trả nguồn. |
| 2 | Đọc giúp mình bài báo này | — | answered | Không bịa URL, nhưng hỏi bằng text thay vì gọi clarify: hạn chế live còn tồn tại, không ghi PASS giả. |
| 3 | https://openai.com/research/ | fetch | answered | Dùng URL bổ sung từ lượt sau, đọc bằng fetch. |
| 4 | Hôm nay là ngày nào, thứ mấy theo giờ Việt Nam? | date | answered | Gọi date, trả ngày/thứ theo giờ Việt Nam. |
| 5 | Chỉ lọc trùng URL trong danh sách đã có này, không tìm thêm: [{"title":"A","url":"https://example.com/a"},{"title":"A copy","url":"https://example.com/a"},{"title":"B","url":"https://example.com/b"}] | deduplicate | answered | Loại 1 URL trùng, giữ 2 nguồn. |
| 6 | Đăng lên Telegram câu này: Bản tin AI hôm nay đã sẵn sàng. | clarify | waiting_for_user | clarify yes_no đúng nội dung; dừng chờ, chưa gửi. |
| 7 | Thôi không gửi nữa, cảm ơn. | — | answered | Hủy đúng, không gọi send. |

Cả 7 lượt không có provider error/tool error; phiên có research, hỏi lại/bổ sung, date, deduplicate và xác nhận/hủy gửi. Khác biệt hỏi URL bằng text đã được ghi trung thực để cải tiến sau; không ảnh hưởng bằng chứng API chạy thật.

## B5. Tool tests, UI và bonus

| Hạng mục | Evidence | Kết quả / giới hạn |
|---|---|---|
| Unit + UI tests | `analysis/pytest.txt`, `tests/` | 139 PASS; 0 failed/skipped; offline, HTTP mock |
| Streamlit local | `analysis/ui_verification.json`, `tests/test_ui.py`, `START_LOCAL.ps1` | Trang chính/health HTTP 200; AppTest kiểm tra load v3, đổi version, chat, transcript, chat mới |
| 3 tool mới | `tools/deduplicate/`, `tools/yahoo_finance/`, `tools/date/` | Code, TOOL.md, registry và YAML đồng bộ; mỗi tool có ít nhất 3 test |
| arXiv / company policy | `runs/v3_B_extension_openrouter_20261110T143526294257.json` | 10/10 đúng routing/args; nội dung truy hồi vẫn cần xem xét thủ công |
| Calendar extension | `runs/v3_B_extension_openrouter_20261110T143438392011.json` | 3/3; tests cố định clock kiểm tra múi giờ, tuần và offset |
| Telegram | `transcripts/v3_openrouter_20261110T143528494225.transcript.json`, group 06/07 | Xác nhận/hủy có bằng chứng; send mô phỏng, không nộp bonus delivery thật |
| Public link | Không thực hiện theo yêu cầu nhóm | Demo local; không có URL public |

Đã bổ sung 2 regression test cho console Windows cp1252: log gọi tool và phản hồi tiếng Việt/emoji không làm dừng agent; UI khởi động ở UTF-8.

Tool tests assert cả request gửi đi và mapping kết quả; bao phủ ticker/URL/input sai, HTTP 429/timeout, thiếu price/currency/timestamp, giữ thứ tự loại trùng và lịch tuần. Đã tìm và sửa lỗi `date(offset_days=inf)` gây OverflowError thay vì error dict; giữ regression test cho ±inf. Đây là lỗi code mà eval routing không phát hiện.

Send thật chưa được kiểm chứng. Stress test lịch sử từng ghi nhận nguy cơ gửi lặp/nhầm nội dung được xem như xác nhận; prompt cuối nhấn mạnh không lấy chữ trong draft làm authorization và không gửi lặp sau thành công, nhưng chưa có bằng chứng đảm bảo idempotency ở tầng delivery. Không tuyên bố đã giải quyết hoàn toàn rủi ro production.

## B6. Reflection

- **Which fixes belonged in `system_prompt.md`?** 
  Các lỗi mang tính chất định hướng hành vi, giới hạn ranh giới, và luồng nghiệp vụ. Cụ thể: Bắt buộc từ chối các yêu cầu ngoài phạm vi (code, toán) để fix lỗi `R08`, `R14`; ép buộc quy trình xác nhận an toàn trước khi gọi công cụ có rủi ro (lỗi `R12` gọi `send` bừa bãi); và quy tắc duy trì ngữ cảnh công cụ (chủ đề, nguồn web) qua nhiều lượt hội thoại (`M02`).

- **Which fixes belonged in `tools.yaml`?**
  Các lỗi mang tính chất ràng buộc dữ liệu đầu vào (schema validation) và quy ước truyền tham số. Cụ thể: Đổi schema của công cụ `clarify` để đưa `response_type` thành trường bắt buộc (required) giúp khắc phục triệt để lỗi thiếu tham số ở `R10` và `R11`. Đồng thời, tinh chỉnh phần description để làm rõ cấu trúc "Convention Arguments" cho các trường `topic` và `timeframe` (fix lỗi `R13`).

- **Which failure needed manual review instead of automatic grading?**
  Lỗi logic nội dung sau khi ghép chuỗi. Bộ Eval cơ sở hiện tại chủ yếu chấm độ chuẩn xác của Routing và Argument Matching (gọi đúng tool, đúng tham số). Tuy nhiên, nếu model lấy thông tin từ web (lookup) nhưng tổng hợp sai lệch ý nghĩa (hallucination trong quá trình summarize), hoặc nội dung chắt lọc ở `fetch` không khớp với policy công ty, thì hệ thống chấm điểm tự động không thể bắt được. Những lỗi sai ngữ nghĩa này cần sự can thiệp và đánh giá thủ công của con người (qua quá trình Live Chat).

- **What would you improve next?**
  (1) Tích hợp một Evaluator Model chuyên biệt để chấm điểm chéo (LLM-as-a-Judge) nhằm bắt các lỗi logic, hallucination thay vì chỉ chấm bằng code Python cứng. (2) Siết chặt hơn cơ chế Fallback: Nếu API tài chính hoặc search bị timeout/rate-limit, agent nên biết cách gọi `clarify` để thông báo cho user thay vì crash hoặc bịa data.

### Quan sát cuối từ kiểm tra thực tế

Bộ eval ép gọi tool ở các case có expected tool; UI/chat không ép nên hành vi có thể khác. Ở lượt 2 của transcript cuối, model xin URL bằng text dù prompt yêu cầu clarify. Vì vậy ưu tiên tiếp theo là eval đa lượt chạy nguyên vòng hội thoại và kiểm tra điều kiện dừng/hỏi lại, cùng guard xác nhận/idempotency ở tầng ứng dụng trước khi cho gửi thật. Không dùng điểm routing 100% để khẳng định chất lượng tóm tắt hoặc an toàn delivery 100%.

## B7. Small Local Model Challenge (bonus)

Không thực hiện. Nhóm tập trung bản cloud chạy thật, 3 tool mới, UI local, eval và bằng chứng. Poster HTML/SVG không thực hiện. Với 3 tool mới, nhóm không nhận bonus yêu cầu hơn 3 tool mới (tức ít nhất 4).
