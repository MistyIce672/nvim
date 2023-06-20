FROM python:3.11
WORKDIR /broadcast
COPY . .
RUN pip install -r requirements.txt
CMD ["python3","main.py"]
