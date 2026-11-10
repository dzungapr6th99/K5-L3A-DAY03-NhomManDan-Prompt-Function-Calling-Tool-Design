# Bàn giao vòng v2 — So sánh với v1

## Thay đổi duy nhất và giả thuyết

Trong artifacts/tools.yaml, riêng clarify đổi required: [question] thành required: [question, response_type]. Giữ nguyên prompt, các description, tool code và eval_base.json. Giả thuyết: bắt buộc response_type trong schema khiến model truyền explicit argument, khắc phục R10/R11 bị thiếu trường trong v1.

## Bằng chứng

- V1: `runs/v1_B_base_openrouter_20261110T111643249913.json`.
- V2: `runs/v2_B_base_openrouter_20261110T113708805712.json`.
- Provider/model không đổi: openrouter / openai/gpt-4o-mini.
- Snapshot: artifacts/versions/v2/system_prompt.md và tools.yaml.
- Contract test trước eval: 55 passed.
- Kết quả và full hash đã ghi artifacts/version_log.csv.

| Metric | v1 | v2 |
|---|---:|---:|
| Case đúng | 15/20 | 18/20 |
| Case accuracy | 0.75 | 0.90 |
| Tool routing accuracy | 0.90 | 0.90 |
| Argument accuracy | 0.75 | 0.90 |
| Multi-turn accuracy | 0.8333 | 0.8333 |
| Provider errors | 0 | 0 |

## Phân tích

- R10/R11 chuyển FAIL → PASS. Model gọi clarify với response_type="text" đúng kỳ vọng. Kết quả hỗ trợ giả thuyết schema required của vòng này.
- R13 chuyển FAIL → PASS, nay gọi đủ lookup(query="AI", topic="news", timeframe="day") và social_search. Vì chỉ thay schema clarify, không khẳng định đây là tác động trực tiếp hoặc ổn định của thay đổi đó; một run chưa đủ kết luận nhân quả cho R13.
- Không có case từ PASS ở v1 thành FAIL ở v2.
- R12 vẫn FAIL: model gọi send(text="Bản tin này") trước xác nhận; tool thực tế trả needs_confirmation, không gửi thành công.
- M02 vẫn FAIL: model gọi social_search(query="robotics", search_type="Latest", limit=5), kỳ vọng lookup(query="robotics", topic="news", timeframe="day"). Đây là lỗi chọn tool trong ngữ cảnh nhiều lượt, dù failure_type gán trong dataset là wrong_arg_value.

## Đề xuất cho v3 — chưa sửa/chạy

Ưu tiên một giả thuyết về xác nhận hành động: đoạn prompt hiện yêu cầu gửi ngay gây lỗi R12. Thay riêng đoạn đó bằng quy tắc trước khi gửi phải gọi clarify(response_type="yes_no") để xác nhận nội dung/đích gửi; chỉ gọi send(confirmed=true) khi user xác nhận rõ hành động đó và nội dung đã có; nếu thiếu nội dung thì hỏi bổ sung; không bịa nội dung. Giữ thay đổi schema v2. Chạy lại base và theo dõi toàn bộ regression.

M02 và các description/routing chưa rõ cần được ghi là tồn đọng; nếu sửa tiếp hãy dùng vòng riêng thay vì trộn giả thuyết xác nhận với routing. Đề xuất nhóm thêm eval mới kiểm tra carry-over nguồn web, timeframe và chuyển chủ đề.

## Nội dung bàn giao cho Người 2

Dùng v1_vs_v2.csv và run v2 cập nhật report B1/B2, kiểm tra các call thật và đề xuất eval nhóm. Tiếp tục viết đủ 10 case; không cần đợi việc đó để phân tích v2. V2 chưa phải bản cuối tích hợp tool/UI; không dùng nó làm bằng chứng tool mới đã chạy.
