### Project structure
```shell
.
├── .envs
│   ├── .local # local env files
│   ├── .pord # prod env files (not commited to git)
│   ├── .pord.example # prod example env files
├── myapp
│   ├── auth # authentication app
│   ├── book # book app
│   │   ├── tests # book unit tests
│   ├── core # global and common codes
│   ├── users # users app
│   │   ├── tests # users unit tests
├── compose
│   ├── local # docker compose config files for local env
│   └── prod # docker compose config files for prod env
├── config
│   ├── settings
│   │   ├── base.py # django base settings
│   │   ├── local.py # django settings for local env
│   │   ├── prod.py # django settings for production env
│   │   └── test.py # django settings for testing env
├── .gitlab-ci.yml # CI/CD config
├── .pre-commit-config.yml # pre-commit
├── pyproject.toml # python tools config and poetry
├── setup.cfg # python tools config
└── tests # api tests
```

## Tools
#### See [pyproject.toml](./pyproject.toml)

## Run local
- postgres:
```shell
docker compose -f docker-compose.local.yml up postgres -d
```
- poetry:
```shell
poetry shell
poetry install --with dev
```
- migrate:
```shell
python manage.py migrate
```
- run:
```shell
python manage.py runserver 127.0.0.1:8000
```
- #### `schema` at: [http://localhost:8000/docs/](http://localhost:8000/docs/)
- #### `admin` at: [http://localhost:8000/admin/](http://localhost:8000/admin/)

## Run local (docker)
- run:
```shell
docker compose -f docker-compose.local.yml up -d
```
- #### `schema` at: [http://localhost:8000/docs/](http://localhost:8000/docs/)
- #### `admin` at: [http://localhost:8000/admin/](http://localhost:8000/admin/)

## Run prod (docker)
- Make a copy of `.postgres.example`, rename it to `.postgres` and configure the env variables:
```
cp -r .envs/.prod.example .envs/.prod
```
- configure [traefik](./compose/prod/traefik/traefik.yml):

- run:
```shell
docker compose -f docker-compose.prod.yml up -d
```

- migrate:
```shell
docker compose -f docker-compose.prod.yml exec django python manage.py migrate
```
- #### `traefik` default config is to listen on `http://myapp.localhost`
- #### `admin` and `schema` are disable in prod
