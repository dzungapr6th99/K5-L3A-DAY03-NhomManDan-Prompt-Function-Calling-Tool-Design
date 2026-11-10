# TEAM — Nhóm Mân Đàn (ManDan)

## 1. Thông tin project

- **Bài lab:** K5-L3A Day 03 — Prompt, Function Calling & Tool Design / Research Agent Tool Eval.
- **Repository:** https://github.com/dzungapr6th99/K5-L3A-DAY03-NhomManDan-Prompt-Function-Calling-Tool-Design
- **Thư mục nộp bài:** [`starter_v0/`](starter_v0/).
- **Sản phẩm:** Research Agent dùng tool để tìm tin web/X, đọc URL và paper arXiv, tra policy, tổng hợp bản tin, lọc trùng nguồn, lấy báo giá và thông tin ngày tháng.
- **Provider/model:** OpenRouter / `openai/gpt-4o-mini`.
- **Giao diện:** Streamlit chạy local, có chọn snapshot v0–v3, lịch sử chat, tool calls/results và lưu transcript.
- **Báo cáo chung:** [`REPORT.md`](starter_v0/artifacts/REPORT.md), gồm Phần A giới thiệu agent và Phần B bằng chứng/đánh giá.

## 2. Thành viên và phân công đã thống nhất

| Người phụ trách | Họ và tên | MSSV | Vai trò Day 03 | Tài khoản GitHub / tên hiển thị |
|---|---|---|---|---|
| **Người 1 — Bình** | Tạ Công Bình | 2A202603628 | Prompt, tool declaration, tối ưu v0–v3 và tích hợp bản nộp | [BinhTa2004](https://github.com/BinhTa2004) |
| **Người 2 — Huy** | Phạm Hồng Khánh Huy | 2A202603588 | Phân tích log, viết eval nhóm, so sánh version và reflection | Pham Hong Khanh Huy |
| **Người 3 — Dũng** | Nguyễn Tuấn Dũng | 2A202603608 | Tool mới, contract, unit test và kiểm tra registry/YAML | [dzungapr6th99](https://github.com/dzungapr6th99) |
| **Người 4 — Thông** | Nguyễn Minh Thông | 2A202603637 | UI Streamlit, demo local, transcript và tổng hợp report | [ToyzZone](https://github.com/ToyzZone) |

Bảng ghi trách nhiệm chính theo phân công; các sản phẩm được nhóm phối hợp và kiểm chéo. Không dùng bảng này để suy ra tỷ lệ đóng góp hoặc khẳng định một người tự viết toàn bộ code/tài liệu.

## 3. Trách nhiệm và sản phẩm của từng thành viên

### Tạ Công Bình — Prompt, version và tích hợp

- Quản lý `system_prompt.md` và `tools.yaml` trên bản tích hợp; xử lý routing, thiếu identifier, phạm vi công việc, ngữ cảnh nhiều lượt và xác nhận gửi.
- Chạy baseline v0, cải tiến theo phân tích log rồi đo lại v1/v2/v3; lưu giả thuyết, metric, full hash và run file.
- Nhận phân tích từ Huy, tool/test từ Dũng và UI từ Thông để đồng bộ bản cuối; xử lý conflict và kiểm tra file nộp.
- Kiểm tra snapshot, run và transcript cùng artifact; không dùng điểm của bản cũ cho prompt/tools đã thay đổi.
- Phụ trách duyệt nội dung kỹ thuật và version evidence trong report trước khi nộp.

**Sản phẩm đối chiếu:** [system prompt](starter_v0/artifacts/system_prompt.md), [tools.yaml](starter_v0/artifacts/tools.yaml), [version log](starter_v0/artifacts/version_log.csv), [snapshots](starter_v0/artifacts/versions/), [runs](starter_v0/runs/).

### Phạm Hồng Khánh Huy — Phân tích log và eval

- Đọc log từ v0 ngay khi có baseline; tiếp tục nhận và so sánh từng run v1/v2/v3.
- Phân loại sai tool, sai args, thiếu thông tin, ngoài phạm vi, lỗi provider và lỗi thực thi; báo cả cải thiện lẫn regression cho Bình.
- Phụ trách 10 case nhóm: 5 single turn và 5 multi turn; thống nhất tên tool/args với Dũng, dùng đúng cấu trúc `expect` và `args`.
- Đối chiếu metric với actual tool calls/results; không coi routing PASS là bằng chứng mọi nội dung trả lời đều đúng.
- Tổng hợp report B1–B3 và B6; ghi rõ khác biệt giữa eval ép tool calling và chat live lựa chọn tự động.

**Sản phẩm đối chiếu:** [eval nhóm](starter_v0/data/eval_group.json), [so sánh v0–v1](starter_v0/analysis/v0_vs_v1.csv), [v1–v2](starter_v0/analysis/v1_vs_v2.csv), [v2–v3](starter_v0/analysis/v2_vs_v3_base.csv), [kết quả group](starter_v0/analysis/v3_group_results.csv), report B1–B3/B6.

### Nguyễn Tuấn Dũng — Tool và unit test

- Phụ trách contract và kiểm tra implementation của tool: tên, signature, input/output, nhánh lỗi và tài liệu `TOOL.md`.
- Phối hợp tích hợp các tool mới `deduplicate`, `get_yahoo_finance_data`, `date`; đồng bộ `TOOL_FUNCTIONS` và gửi đề xuất declaration cho Bình.
- Kiểm tra ≥3 test/tool mới, gồm dữ liệu hợp lệ, input xấu và nhánh lỗi; tool API dùng mock HTTP trong unit test.
- Hoàn thiện test TODO; kiểm tra contract giữa code/YAML/eval và giữ regression test cho bug đã sửa.
- Phối hợp xử lý lỗi ngày lệch không hợp lệ và console Windows; cung cấp kết quả test cho report B5.

**Sản phẩm đối chiếu:** [deduplicate](starter_v0/tools/deduplicate/), [Yahoo Finance](starter_v0/tools/yahoo_finance/), [date](starter_v0/tools/date/), [registry](starter_v0/tools/__init__.py), [tests](starter_v0/tests/), [pytest output](starter_v0/analysis/pytest.txt).

### Nguyễn Minh Thông — UI, demo và report

- Phụ trách UI Streamlit, cấu hình giao diện, chọn đúng snapshot version, lịch sử chat, hiển thị arguments/results và nút chat mới.
- Tái sử dụng vòng lặp tool của `chat.py`; lưu transcript với version/hash của artifact thực tế.
- Chuẩn bị câu hỏi mẫu, kiểm tra UI local, hỗ trợ chạy trên Windows và ghi phiên chat API thật trên bản cuối.
- Viết report Phần A và B4; nhận phần phân tích/test từ Huy và Dũng để tổng hợp báo cáo chung.
- Nhóm chọn demo local; không nộp public link theo phạm vi đã thống nhất.

**Sản phẩm đối chiếu:** [app.py](starter_v0/app.py), [chat.py](starter_v0/chat.py), [cấu hình UI](starter_v0/.streamlit/config.toml), [UI tests](starter_v0/tests/test_ui.py), [UI verification](starter_v0/analysis/ui_verification.json), [transcript](starter_v0/transcripts/), [hướng dẫn chạy](starter_v0/RUN_LOCAL.md), [khởi động Windows](starter_v0/START_LOCAL.ps1), report A/B4.

## 4. Kết quả project hiện tại

Các số liệu dưới đây được đối chiếu với run JSON và kết quả test, không phải số liệu dự kiến.

| Hạng mục | Kết quả / bằng chứng |
|---|---|
| Baseline v0 | 14/20 base — 70% |
| V1 | 15/20 base — 75% |
| V2 | 18/20 base — 90% |
| V3 cuối | 20/20 base — 100%; 10/10 group — 100% |
| Eval mở rộng trên cùng artifact cuối | Date 3/3; research extension 10/10 |
| Tool | 13 tool, gồm 3 tool mới: `deduplicate`, `get_yahoo_finance_data`, `date` |
| Unit/UI tests | 139 passed, 0 failed, 0 skipped; có regression test cho console Windows cp1252 |
| Chat live | 1 phiên chính thức 7 lượt; API model/read tools thật, không có provider/tool error |
| UI | Streamlit local; đã kiểm tra HTTP 200, đổi version, chat, transcript và chat mới |
| Bản nộp | Code, report A/B, 7 run JSON, 1 transcript chính thức và CSV phân tích |

**Run v3 cuối:**

- [Base 20/20](starter_v0/runs/v3_B_base_openrouter_20261110T143325569018.json).
- [Group 10/10](starter_v0/runs/v3_B_group_openrouter_20261110T143410949838.json).
- [Date 3/3](starter_v0/runs/v3_B_extension_openrouter_20261110T143438392011.json).
- [Research extension 10/10](starter_v0/runs/v3_B_extension_openrouter_20261110T143526294257.json).
- [Chat live 7 lượt](starter_v0/transcripts/v3_openrouter_20261110T143528494225.transcript.json).

## 5. Cách phối hợp và kiểm chéo

1. **Bình chạy một version → Huy đọc log → hai người chốt giả thuyết tiếp theo.** V1/v2/v3 làm tuần tự, không sửa artifact giữa lúc eval chạy.
2. **Dũng làm tool/test và Thông dựng UI song song** với vòng tối ưu; Huy soạn eval từ lỗi thực tế và contract tool đã thống nhất.
3. Dũng bàn giao implementation/TOOL.md/registry/test; Huy bàn giao case; Thông bàn giao UI/transcript. Bình tích hợp và kiểm tra lại.
4. Cả nhóm đối chiếu report với đúng run/hash; không sửa base eval hoặc nới kỳ vọng để làm đẹp điểm.
5. Mỗi người dùng nhánh/clone riêng, một đầu mối tích hợp. Không đưa `.env`, API key, `.venv` hay cache vào Git.

## 6. Phạm vi và giới hạn đã ghi nhận

- Telegram trong eval/demo được **mô phỏng**, không phải bằng chứng gửi tin thật hoặc bảo đảm idempotency khi chạy production.
- Trong transcript live, có lượt xin URL bằng text thay vì gọi `clarify`; report B4/B6 đã ghi rõ. Điểm eval 100% chỉ phản ánh các bộ case đã đo.
- Public link, poster và Small Local Model Challenge không thực hiện. Nhóm có 3 tool mới, không nhận bonus yêu cầu hơn 3 tool mới.
- Nhóm sử dụng AI hỗ trợ phân tích log, chỉnh prompt/code và soạn tài liệu; bằng chứng là các lần chạy thực tế được lưu trong repo.
