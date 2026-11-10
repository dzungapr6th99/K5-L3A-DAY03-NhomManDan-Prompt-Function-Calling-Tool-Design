# Báo cáo cá nhân — NguyenMinhThong-2A202603637

## 1. Thông tin thành viên

- Họ tên: **Nguyễn Minh Thông**.
- MSSV: **2A202603637**.
- GitHub: [ToyzZone](https://github.com/ToyzZone).
- Nhóm/lớp: Nhóm Mân Đàn — L3A.
- Vai trò: **Người 4 — UI, demo, transcript và tổng hợp report**.

## 2. Phần việc phụ trách

- Phụ trách UI Streamlit, demo local và transcript.
- Tổng hợp report Phần A/B4 và hướng dẫn chạy.

## 3. Đóng góp cụ thể

- Xây UI Streamlit với chọn version, lịch sử chat, bảng điểm và hiển thị tool calls/results.
- Hoàn thiện chạy local trên Windows, kiểm tra UI và phối hợp sửa lỗi kết nối API/Unicode.
- Chuẩn bị câu hỏi demo, ghi transcript 7 lượt và tổng hợp report Phần A/B4.

## 4. Bằng chứng

- [App](../../starter_v0/app.py), [chat loop](../../starter_v0/chat.py), [cấu hình giao diện](../../starter_v0/.streamlit/config.toml).
- [UI tests](../../starter_v0/tests/test_ui.py), [encoding tests](../../starter_v0/tests/test_console_encoding.py), [UI verification](../../starter_v0/analysis/ui_verification.json).
- [Transcript 7 lượt](../../starter_v0/transcripts/v3_openrouter_20261110T143528494225.transcript.json).
- [RUN_LOCAL.md](../../starter_v0/RUN_LOCAL.md), [START_LOCAL.ps1](../../starter_v0/START_LOCAL.ps1), [safe demo runner](../../starter_v0/scripts/chat_demo_safe.py).
- [Report A/B4](../../starter_v0/artifacts/REPORT.md) và [TEAM.md](../../TEAM.md).

**Công cụ sử dụng:** Codex/ChatGPT hỗ trợ UI và tài liệu; kiểm tra bằng Streamlit AppTest, HTTP health check và phiên chat API.

## 5. Tự đánh giá

- Hoàn thiện UI local, hướng dẫn chạy và transcript 7 lượt.
- Kiểm tra đổi version, lưu lịch sử, chat mới và xử lý lỗi kết nối/Unicode.
- Hướng tiếp theo: bổ sung kiểm thử hội thoại dài và thông báo lỗi dễ hiểu hơn.
