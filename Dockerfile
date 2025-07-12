# Sử dụng image Python nhẹ
FROM python:3.11-slim

# Cài các gói hệ thống cần thiết (nếu có Plotly hoặc Pandas, cần lib này)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Tạo thư mục làm việc
WORKDIR /app

# Copy file requirements trước để tận dụng cache Docker layer
COPY requirements.txt .

# Cài thư viện Python
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn
COPY . .

# Expose cổng Dash sử dụng (8051 như bạn định nghĩa)
EXPOSE 8051

# Lệnh chạy app
CMD ["python", "app.py"]
