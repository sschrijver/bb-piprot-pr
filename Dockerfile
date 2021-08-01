FROM python:3.9.6

WORKDIR /app

USER root

RUN pip install piprot==0.9.11 requests==2.26.0

COPY piprot_scan.py piprot_scan.py

ENV REQUIREMENTS_FILE="requirements.txt"

USER 1001

CMD ["python3", "piprot_scan.py"]