# Custom PostgreSQL image for local Compose (major {{ cookiecutter.postgres_version }}).
# Extend this file to install server extensions via apt, or add scripts under
# docker-entrypoint-initdb.d/ for CREATE EXTENSION and one-time setup.
FROM postgres:{{ cookiecutter.postgres_version }}-bookworm

# Install Debian packages that ship PostgreSQL extensions (uncomment / adjust).
# Package names vary by Postgres major; some extensions need PGDG (see README).
# RUN set -eux; \
#   apt-get update; \
#   apt-get install -y --no-install-recommends \
#     postgresql-contrib-{{ cookiecutter.postgres_version }} \
#     postgresql-{{ cookiecutter.postgres_version }}-postgis-3 \
#   ; \
#   rm -rf /var/lib/apt/lists/*

COPY docker/postgres/docker-entrypoint-initdb.d/ /docker-entrypoint-initdb.d/
