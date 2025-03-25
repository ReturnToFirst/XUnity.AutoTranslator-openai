FROM python:3.12-slim

ENV BASE_URL=""
ENV API_KEY=""
ENV MODEL_NAME=""
ENV TEMPERATURE=""
ENV MAX_TOKENS=""
ENV FREQUENCY_PENALTY=""
ENV PRESENCE_PENALTY=""
ENV HOST=""
ENV PORT=""
ENV USE_HISTORY=""
ENV MAX_HISTORY=""
ENV USE_LATEST_HISTORY=""
ENV DB_TYPE=""
ENV CACHE_TRANSLATION=""
ENV USE_CACHED_TRANSLATION=""
ENV USE_LATEST_RECORDS=""
ENV INIT_LATEST_RECORDS=""
ENV POSTGRES_HOST=""
ENV POSTGRES_PORT=""
ENV POSTGRES_USER=""
ENV POSTGRES_PASSWORD=""
ENV POSTGRES_DB=""
ENV SQLITE_DB_PATH=""
ENV LOG_FILE=""
ENV LOG_LEVEL=""
ENV TASK_TEMPLATE=""
ENV SPECIFY_LANGUAGE=""
ENV LANGUAGE_TEMPLATE=""
ENV SRC_START=""
ENV SRC_END=""
ENV TGT_START=""
ENV TGT_END=""
ENV USE_SYSTEM_PROMPT=""
ENV SYSTEM_PROMPT=""
ENV CONFIG=""

RUN mkdir -p /app
WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x start.sh
CMD ["./start.sh"]