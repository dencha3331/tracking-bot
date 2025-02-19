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
	${DC} ${ENV} -f ${POSTGRES_FILE} -f ${BOT_FILE} up --build -d

.PHONY: all-down
all-down:
	${DC} ${ENV} -f ${POSTGRES_FILE} -f ${BOT_FILE} down

.PHONY: bot-down
bot-down:
	${DC} ${ENV} -f ${BOT_FILE} down

.PHONY: postgres-down
postgres-down:
	${DC} ${ENV} -f ${POSTGRES_FILE} down

.PHONY: bot-shell
bot-shell:
	${EXEC} ${BOT_CONTAINER} bash

.PHONY: bot-logs
bot-logs:
	${LOGS} ${BOT_CONTAINER} -f

.PHONY: test
test:
	${EXEC} ${BOT_CONTAINER} pytest