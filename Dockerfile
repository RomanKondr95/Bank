FROM python:3.11-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# WORKDIR /app/bank
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
# EXPOSE 8000
# CMD ["python", "manage.py", "runserver"]