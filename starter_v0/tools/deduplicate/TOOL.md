---
name: deduplicate
track: bonus
kind: local_formatter
requires_env: []
inputs: [items]
outputs: [items, removed_count]
side_effect: false
---
# deduplicate

Loại item trùng chính xác chuỗi URL, giữ item xuất hiện đầu tiên và thứ tự ban đầu.
Item thiếu URL, URL rỗng hoặc None được giữ lại. Không sửa danh sách đầu vào.
Input phải là list các dictionary; URL nếu có phải là string hoặc None.
Input sai trả error='invalid_input'. Không gọi mạng, không cần API key.
