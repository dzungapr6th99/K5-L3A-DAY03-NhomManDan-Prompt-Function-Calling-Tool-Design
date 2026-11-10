---
name: date
track: bonus
kind: local_knowledge
provider: system_clock
requires_env: []
inputs: [offset_days]
outputs: [now, today, last_week, this_week, next_week, offset_days, date, weekday, week_of_date]
side_effect: false
---
# date

Trả về ngày hiện tại theo giờ Việt Nam (UTC+7) để model không phải tự đoán. Không có tool này,
gpt-4o-mini trả lời câu "hôm nay là ngày nào" bằng "27/10/2023" (ngày lấy từ dữ liệu huấn luyện).

- `last_week` / `this_week` / `next_week` (Thứ Hai → Chủ Nhật) luôn có trong kết quả. Lý do:
  gpt-4o-mini hay chỉ gọi `date()` một lần rồi tự gọi tuần này là "last week", nên "tuần trước",
  "thứ Sáu tuần sau" phải đọc ra được ngay từ lần gọi đó.
- `offset_days` dùng cho các ngày lệch khác: hôm qua = -1, ngày mai = 1, "2 tuần trước" = -14,
  "10 ngày nữa" = 10. Kết quả có thêm `date`, `weekday` và `week_of_date`. Chỉ nhận số nguyên
  trong khoảng ±3660; sai kiểu hoặc vượt khoảng thì trả về error dict chứ không raise.
- Chưa hỗ trợ "tháng trước" hay "năm sau" theo lịch (offset_days=-30 chỉ là xấp xỉ).
