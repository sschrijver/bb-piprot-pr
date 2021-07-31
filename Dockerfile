FROM python:3.9.6

USER root

RUN pip install piprot==0.9.11

COPY run.sh run.sh

RUN chmod +x run.sh

ENV REQUIREMENTS_FILE="requirements.txt"

USER 1001

ENTRYPOINT ["bin/bash"]

CMD ["run.sh"]