# Báo cáo cá nhân — PhamHongKhanhHuy-2A202603588

## 1. Thông tin thành viên

- Họ tên: **Phạm Hồng Khánh Huy**.
- MSSV: **2A202603588**.
- GitHub: Pham Hong Khanh Huy.
- Nhóm/lớp: Nhóm Mân Đàn — L3A.
- Vai trò: **Người 2 — Phân tích log, eval và reflection**.

## 2. Phần việc phụ trách

- Phụ trách phân tích log và so sánh kết quả v0–v3.
- Xây eval nhóm và tổng hợp report B1–B3/B6.

## 3. Đóng góp cụ thể

- Phân tích lỗi v0–v3 và lập CSV so sánh tool calls, arguments, kết quả trước/sau.
- Hoàn thiện 10 case nhóm gồm 5 single turn và 5 multi turn; sửa cấu trúc expect/args cho khớp tool.
- Tổng hợp phân tích và reflection trong report B1–B3/B6, ghi rõ khác biệt giữa eval và chat live.

## 4. Bằng chứng

- [10 case nhóm](../../starter_v0/data/eval_group.json) và [3 case date](../../starter_v0/data/eval_date.json).
- [v0–v1](../../starter_v0/analysis/v0_vs_v1.csv), [v1–v2](../../starter_v0/analysis/v1_vs_v2.csv), [v2–v3](../../starter_v0/analysis/v2_vs_v3_base.csv).
- [Kết quả group CSV](../../starter_v0/analysis/v3_group_results.csv) và [group run 10/10](../../starter_v0/runs/v3_B_group_openrouter_20261110T143410949838.json).
- [Transcript 7 lượt](../../starter_v0/transcripts/v3_openrouter_20261110T143528494225.transcript.json).
- [Report B1–B3/B6](../../starter_v0/artifacts/REPORT.md) và [TEAM.md](../../TEAM.md).

**Công cụ sử dụng:** Codex/ChatGPT hỗ trợ phân tích; đối chiếu expected, actual calls và failures trong JSON/CSV.

## 5. Tự đánh giá

- Hoàn thiện 10 case nhóm và bảng phân tích lỗi từng version.
- Ghi nhận lượt hỏi URL bằng text trong transcript để bổ sung đánh giá live.
- Hướng tiếp theo: thêm case kiểm tra hủy, đổi nội dung và giữ ngữ cảnh nhiều lượt.
