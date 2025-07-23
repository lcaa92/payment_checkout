# Payment Checkout

## Python Virtual Environments:

To develop all APIs, it was used uv[https://docs.astral.sh/uv/] to manage virtual environments. Each API has its own packages dependecies.

## How to run

### Starting services

```
docker compose up -d
```
if it's running on first time, the SQL scripts will be run to create databases

### Stopping services

```
docker compose down
```
if necessary recreate database structure, it will be necessary destroy the volumes before start containers again


```
docker compose down -v
```

## Services / Directories:

### Gateway / orchestrator
    Payment orchestrator that consumes services from provers 1 and 2

### Provider 1 and Provider 2
    Mocks as payment provider


ToDo list:

### General
- [X] Pipeline CI/CD

### Gateway
- [X] Basic Structure
- [X] Integration with providers
- [X] Linter
- [ ] Tests
    - [X] Basic structure
    - [ ] Complete tests cases
- [ ] Improve logs
- [ ] Implement get payments route

### Provider 1
- [X] Basic Structure
- [X] Linter
- [ ] Tests
    - [X] Basic structure
    - [ ] Complete tests cases
- [ ] Improve logs

### Provider 2
- [X] Basic Structure
- [X] Linter
- [ ] Tests
    - [X] Basic structure
    - [ ] Complete tests cases
- [ ] Improve logs
