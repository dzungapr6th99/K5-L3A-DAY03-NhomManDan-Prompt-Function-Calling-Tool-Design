---
name: wikipedia
track: bonus
kind: live_api
provider: Wikipedia REST API (page/summary)
requires_env: []
inputs: [title, lang]
outputs: [lang, title, description, summary, url, ambiguous]
side_effect: false
---
# wikipedia

Lấy đoạn tóm tắt đầu trang của một bài Wikipedia (`vi` hoặc `en`), không cần API key.
Dùng cho câu hỏi kiến thức nền kiểu "X là gì / là ai / là công ty gì", hoặc khi user nói rõ "tra Wikipedia".
Trước khi có tool này, agent đẩy các câu đó sang `lookup` (tìm tin tức), nên câu trả lời là tin mới nhất
chứ không phải định nghĩa (kịch bản GM05 "Tra Wikipedia" trong stress test).

- `title` là tên trang, ví dụ `Anthropic`, `Transformer (deep learning architecture)`. Khoảng trắng được đổi thành `_`.
- `lang` chỉ nhận `vi` hoặc `en`. Trang tiếng Việt hay thiếu với chủ đề AI, nên khi gặp `not_found` thì thử `en`.
- Không có trang → `{"error": "not_found"}`. Thiếu title hoặc sai lang → `{"error": "invalid_input"}`. Lỗi mạng/HTTP → error dict, không raise.
- `ambiguous: true` khi trang là trang định hướng (nhiều nghĩa): nên hỏi lại user muốn nghĩa nào.
- Không dùng cho tin tức mới (dùng `lookup`) hay bài trên X.
