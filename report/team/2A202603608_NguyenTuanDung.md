# Báo cáo cá nhân — NguyenTuanDung-2A202603608

## 1. Thông tin thành viên

- Họ tên: **Nguyễn Tuấn Dũng**.
- MSSV: **2A202603608**.
- GitHub: [dzungapr6th99](https://github.com/dzungapr6th99).
- Nhóm/lớp: Nhóm Mân Đàn — L3A.
- Vai trò: **Người 3 — Tool, contract và unit test**.

## 2. Phần việc phụ trách

- Phụ trách implementation, contract và tài liệu của tool.
- Hoàn thiện unit test, registry và kiểm tra tích hợp.

## 3. Đóng góp cụ thể

- Phối hợp hoàn thiện 3 tool mới: deduplicate, get_yahoo_finance_data và date.
- Đồng bộ code, TOOL.md, registry và khai báo YAML; bổ sung test input hợp lệ, input lỗi và HTTP mock.
- Hoàn thiện test TODO và regression cho date/console Windows; kiểm tra suite chung đạt 139 PASS, không failed/skipped.

## 4. Bằng chứng

- [deduplicate code/TOOL.md](../../starter_v0/tools/deduplicate/), [Yahoo Finance code/TOOL.md](../../starter_v0/tools/yahoo_finance/), [date code/TOOL.md](../../starter_v0/tools/date/).
- [Registry](../../starter_v0/tools/__init__.py) và [tool declaration](../../starter_v0/artifacts/tools.yaml).
- [Tool tests hoàn thiện](../../starter_v0/tests/test_tools_todo.py), [finance tests](../../starter_v0/tests/test_yahoo_finance.py), [date tests](../../starter_v0/tests/test_tool_date.py).
- [Console regression tests](../../starter_v0/tests/test_console_encoding.py), [pytest output](../../starter_v0/analysis/pytest.txt).
- [Report B5](../../starter_v0/artifacts/REPORT.md) và [TEAM.md](../../TEAM.md).

**Công cụ sử dụng:** Codex/ChatGPT hỗ trợ triển khai và test; chạy pytest với fake_http, monkeypatch và dữ liệu kiểm thử.

## 5. Tự đánh giá

- Đồng bộ tool, TOOL.md, registry và YAML; hoàn thiện test TODO.
- Kiểm tra suite chung đạt 139 PASS, có regression cho date và console Windows.
- Hướng tiếp theo: mở rộng test dữ liệu provider và xử lý timeout.
