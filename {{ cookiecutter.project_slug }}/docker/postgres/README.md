# PostgreSQL image (Docker Compose `db` service)

The `db` service is built from this directory so you can pin the **Postgres major ({{ cookiecutter.postgres_version }})** and add **extensions / plugins** without relying on a generic upstream tag alone.

## Layout

| Path | Role |
|------|------|
| `Dockerfile` | `FROM postgres:{{ cookiecutter.postgres_version }}-bookworm` plus optional `RUN apt-get …` for extra packages |
| `docker-entrypoint-initdb.d/` | Scripts run **once** on first init (empty volume). Use `.sql` or `.sh` for `CREATE EXTENSION`, roles, etc. |

## Installing server-side extensions (plugins)

1. **Debian packages** (PostGIS, contrib modules, PGDG packages): add a `RUN apt-get update && apt-get install -y …` block in `Dockerfile`. Names depend on the Postgres major and whether you use [PGDG](https://wiki.postgresql.org/wiki/Apt) repos.
2. **Enable extensions in the database**: add SQL under `docker-entrypoint-initdb.d/`, for example:
   ```sql
   CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
   ```
3. **Rebuild after Dockerfile changes**: `docker compose build db` (use `--no-cache` if apt layers changed). **New extension SQL** only runs on **first** cluster init; for an existing volume, run `CREATE EXTENSION` manually or recreate the volume.

## Changing the Postgres major

Regenerate the project with a different `postgres_version`, or edit the `FROM` line in `Dockerfile` and `docker-compose.yml` image tag to match.
