FROM python:3.10-slim

WORKDIR /app

COPY app/ ./app/

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser

EXPOSE 8000

CMD ["python", "app/app.py"]


