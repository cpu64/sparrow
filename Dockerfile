FROM cpu64/python3.13_postgresql

WORKDIR /app

COPY ./app/requirements.txt .

RUN MAKEFLAGS="-j$(nproc)" pip install --prefer-binary --no-cache-dir --break-system-packages --root-user-action ignore -r ./requirements.txt

COPY ./app/ .

CMD ["python", "app.py"]
