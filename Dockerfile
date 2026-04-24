FROM python:3.11-slim

WORKDIR /app


COPY requirements.txt .

# Устанавливаем пакеты по одному с увеличенным таймаутом
RUN pip install --no-cache-dir --default-timeout=300 fastapi
RUN pip install --no-cache-dir --default-timeout=300 uvicorn
RUN pip install --no-cache-dir --default-timeout=300 sqlalchemy
RUN pip install --no-cache-dir --default-timeout=300 psycopg2-binary
RUN pip install --no-cache-dir --default-timeout=300 alembic
RUN pip install --no-cache-dir --default-timeout=300 bcrypt
RUN pip install --no-cache-dir --default-timeout=300 PyJWT
RUN pip install --no-cache-dir --default-timeout=300 python-dotenv
RUN pip install --no-cache-dir --default-timeout=300 email-validator
RUN pip install --no-cache-dir --default-timeout=300 pydantic-settings 

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]