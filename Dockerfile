FROM python:3.12-slim
WORKDIR /app
COPY . .
CMD ["python","mlops_platform.py"]
