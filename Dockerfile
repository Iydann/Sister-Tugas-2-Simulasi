# 1. Gunakan image Python resmi yang ringan
FROM python:3.9-slim

# 2. Tentukan folder kerja di dalam container
WORKDIR /app

# 3. Copy file requirements ke dalam container
COPY requirements.txt .

# 4. Install library yang dibutuhkan
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy semua file proyek ke dalam container
COPY . .

# 6. Ekspos port yang digunakan Streamlit (default 8501)
EXPOSE 8501

# 7. Perintah untuk menjalankan aplikasi
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]