#  Provider 1

The payment provider has been developed using Python FastAPI framework to simulate a real payment provider

## Virutal Env

For manage virtual environment, it was used uv[https://docs.astral.sh/uv/] to manage virtual environments. Each API has its own packages dependecies.

## Python versions

Python 3.11

## Setup

Use the command bellow to install packages dependencies. (The uv will install python version)

```
uv sync
```

## Running project

On first running, create a `.env` file (there is a `.env_example`) and setup env vars. Then run:

```
cd gateway && uv run uv run fastapi dev main.py  --port 8001
```
