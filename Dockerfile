# Base image
FROM python:3.11-slim

# Working directory
WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Cloud Run ต้องการให้แอพฟังบน PORT ที่กำหนดใน ENV
# ใส่ค่า default เพื่อรัน local แต่เมื่อขึ้น Cloud Run มันจะ override ด้วย $PORT
ENV PORT=8080

# Expose port (optional เพราะ Cloud Run ไม่ได้ใช้ EXPOSE)
EXPOSE 8080

# ใช้ gunicorn + uvicorn worker เพื่อให้รองรับ production
CMD exec gunicorn main:app \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --worker-class uvicorn.workers.UvicornWorker
