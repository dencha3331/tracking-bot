DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
BOT_FILE = docker_compose/bot.yaml
POSTGRES_FILE = docker_compose/postgresql.yaml
BOT_CONTAINER = spam-bot
ENV = --env-file .env

.PHONY: app
bot:
	${DC} ${ENV} -f ${BOT_FILE} up --build -d

.PHONY: postgres
postgres:
	${DC} ${ENV} -f ${POSTGRES_FILE} up --build -d

.PHONY: all
all:
	${DC} ${ENV} -f ${POSTGRES_FILE} -f ${APP_FILE} up --build -d

.PHONY: all-down
all-down:
	${DC} ${ENV} -f ${POSTGRES_FILE} -f ${APP_FILE} down

.PHONY: app-down
app-down:
	${DC} ${ENV} -f ${POSTGRES_FILE} down

.PHONY: postgres-down
postgres-down:
	${DC} ${ENV} -f ${POSTGRES_FILE} down

.PHONY: app-shell
app-shell:
	${EXEC} ${BOT_CONTAINER} bash

.PHONY: app-logs
app-logs:
	${LOGS} ${BOT_CONTAINER} -f

.PHONY: test
test:
	${EXEC} ${BOT_CONTAINER} pytest