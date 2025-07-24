# Payment Checkout

This repo contains 3 differents projects to simulate an payment orchestrator with 2 payments providers

## Services / Directories / Files:
- db_init -- directory with SQL scripts to start database
- gateway -- payment orchestrator source code
- provider1 -- mock payment provider 1 source code
- provider2 -- mock payment provider 2 source code
- Makefile -- some commands to help manage projects
- docker-compose.yaml -- config to run services (including DB) on docker

## Python Virtual Environments:

To develop all APIs, it was used [uv](https://docs.astral.sh/uv/) to manage virtual environments. Each API has its own packages dependecies.

## How to run

### Running local from source

If you rather to run the project from source, you can run directly from the source code (gateway, provider1 or provider2 directory). Inside each directory, there is README.md file explaining how to run.

### Running from docker compose

On this root directory it's possible to start all servie using docker compose tool.

#### Starting services

```
docker compose up -d
```
if it's running on first time, the SQL scripts will be run to create databases

#### Stopping services

```
docker compose down
```
if necessary recreate database structure, it will be necessary destroy the volumes before start containers again


```
docker compose down -v
```



ToDo list:

### General
- [X] Pipeline CI/CD

### Gateway
- [X] Basic Structure
- [X] Integration with providers
- [X] Linter
- [X] Tests
- [X] Logs
- [X] Implement get payments route
- [ ] Implement Refund route

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
