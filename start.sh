#!/bin/sh

ARGS=""

# Base Config from Environment or CLI
[ -n "$BASE_URL" ] && ARGS="${ARGS} --base-url $BASE_URL"
[ -n "$API_KEY" ] && ARGS="${ARGS} --api-key $API_KEY"
[ -n "$MODEL_NAME" ] && ARGS="${ARGS} --model-name $MODEL_NAME"

# Model Config
[ -n "$TEMPERATURE" ] && ARGS="${ARGS} --temperature $TEMPERATURE"
[ -n "$MAX_TOKENS" ] && ARGS="${ARGS} --max-tokens $MAX_TOKENS"
[ -n "$FREQUENCY_PENALTY" ] && ARGS="${ARGS} --frequency-penalty $FREQUENCY_PENALTY"
[ -n "$PRESENCE_PENALTY" ] && ARGS="${ARGS} --presence-penalty $PRESENCE_PENALTY"

# Server Config
[ -n "$HOST" ] && ARGS="${ARGS} --host $HOST"
[ -n "$PORT" ] && ARGS="${ARGS} --port $PORT"

# History Config
[ -n "$USE_HISTORY" ] && [ "$USE_HISTORY" != "0" ] && ARGS="${ARGS} --use-history"
[ -n "$MAX_HISTORY" ] && ARGS="${ARGS} --max-history $MAX_HISTORY"
[ "$USE_LATEST_HISTORY" != "0" ] && ARGS="${ARGS} --use-latest-history"

# Database Config
[ -n "$DB_TYPE" ] && ARGS="${ARGS} --db-type $DB_TYPE"
[ "$CACHE_TRANSLATION" != "0" ] && ARGS="${ARGS} --cache-translation"
[ "$USE_CACHED_TRANSLATION" != "0" ] && ARGS="${ARGS} --use-cached-translation"
[ "$USE_LATEST_RECORDS" != "0" ] && ARGS="${ARGS} --use-latest-records"
[ -n "$INIT_LATEST_RECORDS" ] && ARGS="${ARGS} --init-latest-records $INIT_LATEST_RECORDS"

# PostgreSQL Config
[ -n "$POSTGRES_HOST" ] && ARGS="${ARGS} --postgres-host $POSTGRES_HOST"
[ -n "$POSTGRES_PORT" ] && ARGS="${ARGS} --postgres-port $POSTGRES_PORT"
[ -n "$POSTGRES_USER" ] && ARGS="${ARGS} --postgres-user $POSTGRES_USER"
[ -n "$POSTGRES_PASSWORD" ] && ARGS="${ARGS} --postgres-password $POSTGRES_PASSWORD"
[ -n "$POSTGRES_DB" ] && ARGS="${ARGS} --postgres-db $POSTGRES_DB"

# SQLite Config
[ -n "$SQLITE_DB_PATH" ] && ARGS="${ARGS} --sqlite-db-path $SQLITE_DB_PATH"

# Logging Config
[ -n "$LOG_FILE" ] && ARGS="${ARGS} --log-file $LOG_FILE"
[ -n "$LOG_LEVEL" ] && ARGS="${ARGS} --log-level $LOG_LEVEL"

# Prompt Config
[ -n "$TASK_TEMPLATE" ] && ARGS="${ARGS} --task-template '$TASK_TEMPLATE'"
[ "$SPECIFY_LANGUAGE" != "0" ] && ARGS="${ARGS} --specify-language"
[ -n "$LANGUAGE_TEMPLATE" ] && ARGS="${ARGS} --language-template '$LANGUAGE_TEMPLATE'"

# Tag Config
[ -n "$SRC_START" ] && ARGS="${ARGS} --src-start $SRC_START"
[ -n "$SRC_END" ] && ARGS="${ARGS} --src-end $SRC_END"
[ -n "$TGT_START" ] && ARGS="${ARGS} --tgt-start $TGT_START"
[ -n "$TGT_END" ] && ARGS="${ARGS} --tgt-end $TGT_END"

# System Prompt Config
[ "$USE_SYSTEM_PROMPT" != "0" ] && ARGS="${ARGS} --use-system-prompt"
[ -n "$SYSTEM_PROMPT" ] && ARGS="${ARGS} --system-prompt '$SYSTEM_PROMPT'"

# Configuration Files
[ -n "$CONFIG" ] && ARGS="${ARGS} --config $CONFIG"

echo "ARGS: $ARGS"
exec python3 main.py $ARGS