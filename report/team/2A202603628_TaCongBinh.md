# Báo cáo cá nhân — TaCongBinh-2A202603628

## 1. Thông tin thành viên

- Họ tên: **Tạ Công Bình**.
- MSSV: **2A202603628**.
- GitHub: [BinhTa2004](https://github.com/BinhTa2004).
- Nhóm/lớp: Nhóm Mân Đàn — L3A.
- Vai trò: **Người 1 — Prompt, tool declaration, version và tích hợp**.

## 2. Phần việc phụ trách

- Phụ trách system prompt, tool declaration và version v0–v3.
- Tích hợp code, eval, test và kiểm tra bản nộp.

## 3. Đóng góp cụ thể

- Chỉnh system prompt và tools.yaml để sửa routing, hỏi lại khi thiếu thông tin và xác nhận trước khi gửi.
- Chạy v0–v3, lưu run JSON, snapshot và version log; base tăng từ 70% lên 100%.
- Tích hợp tool, eval và UI; xử lý conflict, dọn log thừa và kiểm tra bản nộp.

## 4. Bằng chứng

- [System prompt](../../starter_v0/artifacts/system_prompt.md) và [tools.yaml](../../starter_v0/artifacts/tools.yaml).
- [Version log](../../starter_v0/artifacts/version_log.csv) và [snapshot v3](../../starter_v0/artifacts/versions/v3/).
- [Base v3 20/20](../../starter_v0/runs/v3_B_base_openrouter_20261110T143325569018.json).
- [So sánh v2–v3](../../starter_v0/analysis/v2_vs_v3_base.csv).
- [Báo cáo chung B1/B2](../../starter_v0/artifacts/REPORT.md) và [phân công nhóm](../../TEAM.md).

**Công cụ sử dụng:** Codex/ChatGPT hỗ trợ chỉnh prompt và tài liệu; kiểm tra bằng Python eval, pytest, Git và run JSON.

## 5. Tự đánh giá

- Hoàn thiện prompt/declaration và tích hợp bản v3, base đạt 20/20.
- Lưu đủ version log, snapshot và bằng chứng so sánh v0–v3.
- Hướng tiếp theo: bổ sung kiểm thử nguyên hội thoại để cải thiện bước hỏi lại.
