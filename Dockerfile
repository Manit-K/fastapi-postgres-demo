# ================================
# 1) Build Stage
# ================================
FROM python:3.11-slim AS builder

WORKDIR /app

# ลดขนาด image + เตรียมระบบให้รองรับ psycopg2/asyncpg
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ติดตั้ง dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


# ================================
# 2) Final Runtime Image
# ================================
FROM python:3.11-slim AS runner

WORKDIR /app

# ติดตั้ง libpq-client ให้รองรับ asyncpg/psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# คัดลอก dependencies จาก builder
COPY --from=builder /root/.local /root/.local

# เพิ่ม PATH เพื่อให้เห็น pip ที่ install แบบ --user
ENV PATH=/root/.local/bin:$PATH

# คัดลอกโค้ดทั้งหมด
COPY . .

# Cloud Run จะส่ง ENV PORT มาอัตโนมัติ
ENV PORT=8080

# เปิดพอร์ต 8080 สำหรับ Cloud Run
EXPOSE 8080

# คำสั่งรัน FastAPI ด้วย Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
