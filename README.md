# DevOps Demo App

Minimal HTTP application for a DevOps practice task. The app has no external runtime dependencies.

## Endpoints

- `GET /health` returns application health.
- `GET /version` returns application name and version.
- `GET /metrics` returns Prometheus-compatible metrics.

## Run Locally

```bash
python3 app.py
```

The app listens on port `8000` by default.

Configuration:

- `HOST`: bind address, default `0.0.0.0`
- `PORT`: bind port, default `8000`
- `APP_NAME`: app name, default `devops-demo-app`
- `APP_VERSION`: app version, default `0.1.0`

Example:

```bash
PORT=8080 APP_VERSION=local python3 app.py
```

## Test

```bash
python3 -m unittest -v
```

## DevOps Scope

Add the DevOps layer around this app:

- `Dockerfile`
- `.dockerignore`
- `docker-compose.yml`
- CI pipeline with tests and image build
- CD pipeline that publishes an image
- Terraform for a VM deployment
