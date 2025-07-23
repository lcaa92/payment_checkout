.PHONY: help run_gateway run_provider1 run_provider2 docker_compose_up docker_compose_down docker_compose_down_volumes linter_gateway linter_provider1 linter_provider2 tests_gateway
help: # Show help for each of the Makefile target.
	@grep -E '^[a-zA-Z0-9 _]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

# Development
run_gateway: # Run the gateway API.
	cd gateway && uv run uv run fastapi dev main.py

run_provider1: # Run the provider1 API.
	cd provider1 && uv run fastapi dev main.py --port 8001

run_provider2: # Run the provider2 API.
	cd provider2 && uv run fastapi dev main.py --port 8002


# Linter
linter_gateway: # Run linter checks for the gateway API.
	cd gateway && uv run flake8 .

linter_provider1: # Run linter checks for the provider1 API.
	cd provider1 && uv run flake8 .

linter_provider2: # Run linter checks for the provider2 API.
	cd provider2 && uv run flake8 .

# Tests
tests_gateway: # Run tests for the gateway API.
	cd gateway && uv run pytest

docker_compose_up: # Start all services using Docker Compose.
	docker compose up -d

docker_compose_down: # Stop all services using Docker Compose.
	docker compose down

docker_compose_down_volumes: # Stop all services and remove volumes using Docker Compose.
	docker compose down -v