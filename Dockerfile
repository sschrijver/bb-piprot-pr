FROM python:3.9.6

USER root

RUN pip install piprot==0.9.11 requests==2.26.0

COPY pipe /

USER 1001

RUN ls

ENTRYPOINT ["python3", "/piprot_scan.py"]