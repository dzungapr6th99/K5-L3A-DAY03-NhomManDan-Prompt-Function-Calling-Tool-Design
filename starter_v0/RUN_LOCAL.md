# Chạy và kiểm tra bản nộp local

Nhóm chọn demo local; không cung cấp link public theo quyết định của nhóm.

## Windows / PowerShell

Chạy trong `starter_v0/`:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Nếu chưa có `.env`, copy `.env.example` thành `.env` và tự điền key trên máy chạy.
Không đưa `.env`, API key hoặc `.venv` vào bài nộp. Provider: OpenRouter,
model `openai/gpt-4o-mini`; cần Tavily, Firecrawl và RapidAPI cho các nguồn tương ứng.

```powershell
.\START_LOCAL.ps1
```

Mở `http://127.0.0.1:8501`. UI mặc định dùng snapshot khớp artifact cuối (v3).
Đổi v0/v1/v2 để xem bản cũ; điểm chỉ hiển thị khi run khớp artifact đang chọn.
Chat mới sau khi đổi artifact. UI và CLI tạo transcript JSON trong `transcripts/`.

## Kiểm tra

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts/eval_group_safe.py --provider openrouter --model openai/gpt-4o-mini --version v3 --suite base --eval-cases data/eval_base.json
.\.venv\Scripts\python.exe scripts/eval_group_safe.py --provider openrouter --model openai/gpt-4o-mini --version v3 --suite group --eval-cases data/eval_group.json
.\.venv\Scripts\python.exe scripts/eval_group_safe.py --provider openrouter --model openai/gpt-4o-mini --version v3 --suite extension --eval-cases data/eval_date.json
.\.venv\Scripts\python.exe scripts/chat_demo_safe.py --provider openrouter --model openai/gpt-4o-mini --version v3
```

Unit test chạy offline với dữ liệu giả lập. Eval/chat dùng provider và read tools thật.
Hai script `*_safe.py` chỉ mô phỏng thao tác `send`, không gửi Telegram; metadata
trong run/transcript ghi rõ điều này. Đây không phải bằng chứng giao tin Telegram thật.
`chat.py` và UI vẫn có tool gửi thật nếu cấu hình token/channel; chưa cấu hình Telegram
thì tool trả lỗi rõ ràng. Không dùng kịch bản có xác nhận gửi thật khi không chủ ý gửi.

## Phạm vi bàn giao

Bốn nhãn nộp là v0–v3; v3 chứa 13 tool gồm `deduplicate`,
`get_yahoo_finance_data`, `date`. Bằng chứng của bản cuối được liệt kê trong
`artifacts/REPORT.md` và `artifacts/version_log.csv`.
Các run cũ khác hash chỉ là lịch sử, không được dùng để gán điểm cho artifact mới.
Bonus local model và poster không thực hiện; không tính là phần bắt buộc còn thiếu.
