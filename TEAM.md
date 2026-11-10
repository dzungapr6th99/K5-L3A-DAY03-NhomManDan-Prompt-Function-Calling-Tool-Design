# Team

## Thông tin nhóm

- Tên nhóm: **Nhóm Mân Đàn (NhomManDan)**.
- Lớp: **L3A**.
- Repo nhóm hiện tại: `K5-L3A-DAY03-NhomManDan-Prompt-Function-Calling-Tool-Design`.
- URL repo: https://github.com/dzungapr6th99/K5-L3A-DAY03-NhomManDan-Prompt-Function-Calling-Tool-Design
- Nhánh nộp: `main`.
- Commit nộp: `HEAD` trên nhánh `main` tại thời điểm nộp link Git.
- Báo cáo nhóm: [report/team/group_report.md](report/team/group_report.md).
- Báo cáo chung của lab: [starter_v0/artifacts/REPORT.md](starter_v0/artifacts/REPORT.md).

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
| 1 | Tạ Công Bình | 2A202603628 | — | [BinhTa2004](https://github.com/BinhTa2004) | Người 1: prompt, tool declaration, version v0–v3 và tích hợp bản nộp |
| 2 | Phạm Hồng Khánh Huy | 2A202603588 | — | — | Người 2: phân tích log, eval nhóm, so sánh version và reflection |
| 3 | Nguyễn Tuấn Dũng | 2A202603608 | — | [dzungapr6th99](https://github.com/dzungapr6th99) | Người 3: tool mới, contract, unit test và registry |
| 4 | Nguyễn Minh Thông | 2A202603637 | — | [ToyzZone](https://github.com/ToyzZone) | Người 4: UI Streamlit, demo, transcript và tổng hợp report |

## Cá nhân

Báo cáo cá nhân của từng thành viên được lưu theo dạng:

```text
report/team/MSSV_HoTen.md
```

Tên file của 4 thành viên:

| Thành viên | File báo cáo riêng |
| --- | --- |
| Tạ Công Bình | [2A202603628_TaCongBinh.md](report/team/2A202603628_TaCongBinh.md) |
| Phạm Hồng Khánh Huy | [2A202603588_PhamHongKhanhHuy.md](report/team/2A202603588_PhamHongKhanhHuy.md) |
| Nguyễn Tuấn Dũng | [2A202603608_NguyenTuanDung.md](report/team/2A202603608_NguyenTuanDung.md) |
| Nguyễn Minh Thông | [2A202603637_NguyenMinhThong.md](report/team/2A202603637_NguyenMinhThong.md) |

Đã hoàn thành 4 báo cáo cá nhân theo phân công bên dưới.

## TaCongBinh-2A202603628

### Phần việc phụ trách

- Quản lý `system_prompt.md` và `tools.yaml` trên bản tích hợp.
- Chạy baseline v0, tối ưu v1/v2/v3, ghi giả thuyết, metric, hash và snapshot.
- Nhận phân tích từ Huy, tool/test từ Dũng và UI từ Thông để tích hợp, xử lý conflict và kiểm tra bản nộp.

### Đóng góp cụ thể

- Chỉnh prompt/declaration xử lý routing, thiếu identifier, xác nhận gửi, ngữ cảnh nhiều lượt và conventions của arguments.
- Đo và lưu kết quả base v0 70% → v1 75% → v2 90% → v3 100%; snapshot và run cuối cùng khớp artifact.
- Tích hợp 13 tool và đủ code, eval, test, transcript, report trong cùng repo.

### Bằng chứng

- [System prompt](starter_v0/artifacts/system_prompt.md), [tool declaration](starter_v0/artifacts/tools.yaml).
- [Version log](starter_v0/artifacts/version_log.csv), [snapshots](starter_v0/artifacts/versions/).
- [Run base v3 — 20/20](starter_v0/runs/v3_B_base_openrouter_20261110T143325569018.json).
- [Report B1–B2](starter_v0/artifacts/REPORT.md).

## PhamHongKhanhHuy-2A202603588

### Phần việc phụ trách

- Đọc log từ v0, phân loại lỗi và so sánh mỗi version để đề xuất giả thuyết tiếp theo.
- Xây 10 case nhóm gồm 5 single turn và 5 multi turn; thống nhất tên tool/args với người viết tool.
- Tổng hợp phân tích, version evidence, team eval và reflection trong report B1–B3/B6.

### Đóng góp cụ thể

- Phân tích sai tool, sai args, thiếu thông tin, ngoài phạm vi và lỗi API; lập bảng so sánh từng version.
- Bộ eval nhóm có đúng 10 case, dùng schema `expect`/`args`, kiểm tra cả các tool mới và xác nhận gửi.
- Report ghi rõ khác biệt giữa eval ép tool calling và chat live: model có thể xin URL bằng text thay vì gọi clarify.

### Bằng chứng

- [Eval nhóm](starter_v0/data/eval_group.json).
- [So sánh v0–v1](starter_v0/analysis/v0_vs_v1.csv), [v1–v2](starter_v0/analysis/v1_vs_v2.csv), [v2–v3](starter_v0/analysis/v2_vs_v3_base.csv).
- [Kết quả group](starter_v0/analysis/v3_group_results.csv), [run group v3 — 10/10](starter_v0/runs/v3_B_group_openrouter_20261110T143410949838.json).
- [Report B1–B3/B6](starter_v0/artifacts/REPORT.md).

## NguyenTuanDung-2A202603608

### Phần việc phụ trách

- Contract và implementation tool: tên, signature, input/output, nhánh lỗi và `TOOL.md`.
- Tích hợp registry; phối hợp Bình khai báo YAML và Huy xây case cho tool mới.
- Hoàn thiện unit test, kiểm tra contract và bổ sung regression test cho lỗi đã sửa.

### Đóng góp cụ thể

- Phần tool mới trong bản nộp gồm `deduplicate`, `get_yahoo_finance_data`, `date`, có code/tài liệu/registry/declaration đồng bộ.
- Test bao phủ happy path, input xấu, HTTP 429/timeout, thiếu dữ liệu giá, thứ tự loại trùng và lịch/offset; mỗi tool mới có ít nhất 3 test.
- Kết quả chung của suite là 139 passed, 0 failed, 0 skipped; có regression cho offset vô hạn và console Windows cp1252.

### Bằng chứng

- [Deduplicate](starter_v0/tools/deduplicate/), [Yahoo Finance](starter_v0/tools/yahoo_finance/), [date](starter_v0/tools/date/).
- [Registry](starter_v0/tools/__init__.py), [tests](starter_v0/tests/), [pytest output](starter_v0/analysis/pytest.txt).
- [Run date — 3/3](starter_v0/runs/v3_B_extension_openrouter_20261110T143438392011.json).
- [Report B5](starter_v0/artifacts/REPORT.md).

## NguyenMinhThong-2A202603637

### Phần việc phụ trách

- UI Streamlit, chọn version theo snapshot, lịch sử chat, xem tool calls/results và tạo phiên mới.
- Demo local, câu hỏi mẫu, transcript với version/hash của artifact thực tế.
- Report Phần A và B4; tổng hợp nội dung phân tích/test từ các thành viên vào báo cáo chung.

### Đóng góp cụ thể

- UI có lựa chọn v0–v3, bảng điểm khớp hash và hiển thị trạng thái gọi tool/hỏi lại; có hướng dẫn và script chạy local trên Windows.
- Bằng chứng UI gồm AppTest và HTTP 200 cho trang chính/health; log console được kiểm thử tương thích cp1252 và khởi động UTF-8.
- Ghi transcript 7 lượt, đối chiếu hash và kiểm tra các bước tìm tin, bổ sung dữ liệu, xác nhận/hủy gửi.

### Bằng chứng

- [App](starter_v0/app.py), [chat loop](starter_v0/chat.py), [cấu hình UI](starter_v0/.streamlit/config.toml).
- [UI tests](starter_v0/tests/test_ui.py), [encoding tests](starter_v0/tests/test_console_encoding.py), [UI verification](starter_v0/analysis/ui_verification.json).
- [Transcript 7 lượt](starter_v0/transcripts/v3_openrouter_20261110T143528494225.transcript.json).
- [Hướng dẫn chạy local](starter_v0/RUN_LOCAL.md), [START_LOCAL.ps1](starter_v0/START_LOCAL.ps1).
- [Report A/B4](starter_v0/artifacts/REPORT.md).
