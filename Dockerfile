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
    FALSK_PORT=5000

CMD ["python", "app.py"]
