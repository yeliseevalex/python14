FROM python:3.14

WORKDIR /app

ENV PYTHONWRITEBYTECODE=1
ENV PYTHONNUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
