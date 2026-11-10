---
name: get_yahoo_finance_data
track: bonus
kind: live_api
provider: Yahoo Finance
requires_env: []
inputs: [ticker]
outputs: [ticker, name, price, currency, exchange, instrument_type, market_time, source, source_url, freshness]
side_effect: false
---
# get_yahoo_finance_data

Lấy giá phiên giao dịch thường gần nhất do Yahoo Finance cung cấp cho một ticker.
Ví dụ: AAPL, NVDA, GC=F (hợp đồng tương lai vàng, không phải giá vàng miếng tại Việt Nam).
Không dự đoán giá hay đưa khuyến nghị mua/bán. Nếu thiếu ticker rõ ràng thì hỏi lại bằng clarify.

Trả timestamp UTC của báo giá; không khẳng định dữ liệu luôn là giá realtime hoặc giá hôm nay.
HTTP error, timeout, ticker không có dữ liệu và response thiếu giá/thời gian đều trả error dict.

Dùng chart endpoint công khai, không chính thức của Yahoo; có thể bị giới hạn hoặc thay đổi.
Không cần thêm dependency ngoài requests đã có. Unit test mock HTTP, không tốn API credit.
Tham khảo implementation dùng chart endpoint: https://github.com/ranaroussi/yfinance/blob/main/yfinance/scrapers/history.py
