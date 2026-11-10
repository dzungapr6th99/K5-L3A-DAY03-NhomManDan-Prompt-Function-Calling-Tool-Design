# Bàn giao vòng v1 — Người 1 cho Người 2

## Thay đổi và giả thuyết

Chỉ thay đoạn system prompt khuyến khích đoán tài khoản/URL bằng quy tắc kiểm tra lịch sử, gọi clarify với response_type="text" khi vẫn thiếu và chờ user bổ sung. tools.yaml và eval_base.json không đổi. Giả thuyết: quy tắc này cải thiện hành vi hỏi lại thay vì bịa dữ liệu.

## Bằng chứng chạy thật

- Baseline: `runs/v0_B_base_openrouter_20261110T101810112659.json`.
- V1 hợp lệ: `runs/v1_B_base_openrouter_20261110T111643249913.json`.
- Lần thử lỗi kết nối: `runs/v1_B_base_openrouter_20261110T111510958096.json`; 20 APIConnectionError, 0 measured cases. Không diễn giải case_accuracy=0 của lần này là chất lượng prompt.
- Model giữ nguyên: OpenRouter / openai/gpt-4o-mini.
- Snapshot: artifacts/versions/v0 và artifacts/versions/v1. Hash hai artifact khớp run tương ứng.
- version_log.csv giữ nguyên dòng baseline OpenAI đã có; thêm baseline OpenRouter đúng run dùng để so v1. Không trộn hai provider khi so sánh.

| Metric | v0 | v1 |
|---|---:|---:|
| Case đúng | 14/20 | 15/20 |
| Case accuracy | 0.70 | 0.75 |
| Tool routing accuracy | 0.75 | 0.90 |
| Argument accuracy | 0.70 | 0.75 |
| Multi-turn accuracy | 1.00 | 0.8333 |
| Provider errors (run hợp lệ) | 0 | 0 |

## Kết quả cần đọc đúng

- R08 và R14: FAIL → PASS (không gọi tool). Đây là kết quả quan sát; không khẳng định prompt đã có chính sách phạm vi đầy đủ.
- R10/R11: đã chuyển sang clarify đúng mục đích, nhưng vẫn FAIL vì raw arguments chỉ có question, thiếu response_type="text". Schema hiện coi response_type là optional và có default; evaluator chấm raw call, không áp default của hàm. Đây là khác biệt giữa hành vi tool chạy và tiêu chí chấm.
- R12: vẫn gọi send chưa được xác nhận; code trả needs_confirmation. Không có bằng chứng gửi Telegram thành công.
- R13: đã gọi lookup + social_search, nhưng lookup thiếu topic="news"; lỗi arguments.
- M02: PASS → FAIL; chọn social_search cho robotics thay vì lookup(news/day). Đây là regression cần giữ trong report, không che bằng điểm tổng.

## Gợi ý vòng v2, chưa thực hiện

Giả thuyết: nếu response_type là required trong schema clarify, model sẽ truyền explicit thay vì dựa vào default; R10/R11 có thể qua evaluator mà không đổi logic tool. Thay required của clarify từ [question] thành [question, response_type], giữ các thay đổi khác cho vòng sau. Chạy base cùng model, đọc cả regression và metric, không mặc định chắc chắn tăng.

Các việc tiếp theo khác: xác nhận trước send; routing web/social và carry-over; bỏ chỉ dẫn ép một bước; hoàn thiện descriptions trong YAML. Mỗi thí nghiệm ghi riêng, không thay toàn bộ cùng lúc rồi quy kết cho một nguyên nhân.

## Unit test và giới hạn

Đã chạy pytest offline: 62 passed, 17 skipped. Chưa viết/sửa test thuộc phần Người 3. Eval PASS không chứng minh tool API trả dữ liệu tốt: phải kiểm tra tool_results. Multi-turn eval không thay thế transcript live.

Người 2 nhận: v0_vs_v1.csv và run JSON; xác nhận các lỗi trên, dùng chúng để viết 10 case nhóm và đề xuất thay đổi vòng sau. Tài liệu này không thay thế REPORT.md cuối cùng của nhóm.
