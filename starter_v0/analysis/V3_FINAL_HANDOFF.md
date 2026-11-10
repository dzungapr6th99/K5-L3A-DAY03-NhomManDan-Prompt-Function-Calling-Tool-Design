# BÀN GIAO V3 — BẢN NỘP CHÍNH THỨC

- Dùng nhãn v3 trong UI, chat CLI và report. Artifact hiện hành khớp snapshot artifacts/versions/v3.
- Base 20/20 (100%), group 10/10 (100%), routing/argument/multi-turn 100%, provider errors 0.
- Unit tests 116 passed, 0 failed, 0 skipped.
- V0 70% → v1 75% → v2 90% → v3 100% trên base.
- Model và read tools thật; send mô phỏng, không gửi Telegram.
- Đây là artifact cuối được chọn và chuẩn hóa nhãn; không chạy API lại hoặc thay đổi metric. So v2 với v3 là so kết quả tổng thể, không phải thí nghiệm một thay đổi đơn lẻ.

## Bằng chứng cần nhận

- Base: runs/v3_B_base_openrouter_20261110T123220151282.json
- Group: runs/v3_B_group_openrouter_20261110T123259318689.json
- analysis/v2_vs_v3_base.csv; analysis/v3_group_results.csv; analysis/v3_tool_errors.json.
- artifacts/version_log.csv; artifacts/REPORT.md B1–B3 đã đồng bộ.
- Snapshot: artifacts/versions/v3/.

## Công việc bàn giao

Huy: đối chiếu raw calls/results và CSV; hoàn thiện reflection/report; dùng đúng các đường dẫn trên.
Thông: chọn v3, tạo phiên mới; kiểm tra UI/link, ghi chat live thành công ≥3 lượt và điền report B4. Transcript phải khớp hash artifact hiện hành; transcript cũ lỗi key không đạt yêu cầu.
Dũng: xác nhận tool mới và toàn bộ test được nộp kèm; không bỏ TOOL.md/registry/YAML.
Bình: duyệt đủ yêu cầu nộp; mọi thay đổi prompt/tools sau đây cần được đo lại. Điểm 100% không thay thế UI/link/transcript/report còn thiếu.
