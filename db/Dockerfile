FROM python:3.8

WORKDIR /app

COPY ./db /app/

COPY ./get_data.sh /app/
RUN ./get_data.sh

CMD ["python", "init-script.py"]