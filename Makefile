.PHONY: help run_gateway run_provider1 run_provider2
help: # Show help for each of the Makefile target.
	@grep -E '^[a-zA-Z0-9 _]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

# Development
run_gateway: # Run the gateway API.
	cd gateway && uv run uv run fastapi dev main.py

run_provider1: # Run the provider1 API.
	cd provider1 && uv run fastapi dev main.py --port 8001

run_provider2: # Run the provider2 API.
	cd provider2 && uv run fastapi dev main.py --port 8002