FROM debian:bullseye

RUN apt update && apt install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libxml2-dev \
    libxslt-dev && \
    apt clean && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY . /app

CMD ["python3","app.py"]
