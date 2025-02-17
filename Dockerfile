
FROM python:3.9-slim


WORKDIR /fastapi_application


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY . /fastapi_application


EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
