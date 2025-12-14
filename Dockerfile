FROM cpu64/python3.13_postgresql

WORKDIR /app

COPY ./app/requirements.txt .

RUN MAKEFLAGS="-j$(nproc)" pip install --prefer-binary --no-cache-dir --break-system-packages --root-user-action ignore -r ./requirements.txt

COPY ./app/ .

ENV PGDATABASE=sparrow \
    PGUSER=sparrow \
    PGPASSWORD=overwriteme \
    PGHOST=localhost \
    PGPORT=5432 \
    FALSK_HOST=0.0.0.0 \
    FALSK_PORT=5000 \
    GMAIL_ADDRESS=sparrowedsparrow@gmail.com \
    GMAIL_APP_PASSWORD=overwriteme

ENV GOOGLE_APPLICATION_CREDENTIALS=/auth/gcs-key.json \
    GCS_BUCKET_NAME=sparrow-flask-images-2025

CMD ["python", "app.py"]
