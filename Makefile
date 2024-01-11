.PHONY: backend frontend bot mock

backend:
	@echo "starting backend"
	@./scripts/run_backend.sh


mock:
	@echo "starting mock backend"
	@./scripts/run_backend.sh --mock

frontend:
	@echo "Starting streamlit frontend..."
	@./scripts/run_frontend.sh

bot:
	@echo "Starting bot..."
	@./scripts/run_bot.sh

stop:
	@kill $(pgrep -f python)