FROM python:3.9
ARG DEBIAN_FRONTEND=noninteractive
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
RUN apt-get update -y
RUN apt-get install -y netcat-openbsd
WORKDIR /app
COPY pyproject.toml entrypoint.sh /app/
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-ansi -n
COPY ./loro /app/loro
RUN chmod +x entrypoint.sh
CMD ["sh", "entrypoint.sh"]
#CMD ["poetry" "run" "loro"]
#RUN poetry run loro