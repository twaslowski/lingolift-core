.PHONY: backend frontend bot stop

backend:
	@echo "starting backend"
	@./scripts/run_backend.sh

frontend:
	@echo "Starting frontend..."
	@./scripts/run_frontend.sh

bot:
	@echo "Starting bot..."
	@./scripts/run_bot.sh

stop:
	@kill $(pgrep -f python)