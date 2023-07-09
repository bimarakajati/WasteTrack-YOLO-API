FROM python:3.9-alpine
COPY main.py main.py
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "main.py"]