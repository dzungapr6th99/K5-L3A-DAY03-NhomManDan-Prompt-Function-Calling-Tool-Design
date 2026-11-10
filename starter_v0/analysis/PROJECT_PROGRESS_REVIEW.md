# Tiến độ hiện tại — nhãn nộp v0/v1/v2/v3

Đã có 12 tool (2 tool mới: deduplicate và get_yahoo_finance_data), unit test 116 passed/0 skipped, 10 group cases (5 single/5 multi), run JSON và snapshot cho v0–v3. Base: 70% → 75% → 90% → 100%; v3 group 10/10. Report A và B1–B3 có nội dung.

V3 là artifact cuối được chọn và chuẩn hóa nhãn, không thay đổi dữ liệu đo. Bằng chứng hiện hành và bàn giao: analysis/V3_FINAL_HANDOFF.md. Gửi Telegram được mô phỏng trong eval; không phải bằng chứng delivery thật.

Còn cần nhóm hoàn tất: xác minh UI chạy và link demo, tạo transcript live thành công ≥3 lượt trên artifact v3, điền B4, hoàn thiện reflection/report B6 và rà checklist nộp. Transcript cũ một lượt lỗi key không đủ. Cài dependency Streamlit trong môi trường chạy UI nếu chưa có.
