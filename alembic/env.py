from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config, pool

from alembic import context

from app.config.settings import settings
from app.config.test_settings import test_settings
from app.database.base import Base
import app.models.asset
import app.models.user

# Alembic Config object
config = context.config

# Choose database based on environment
database_url = (
    test_settings.database_url if os.getenv("TESTING") == "1" else settings.database_url
)

config.set_main_option("sqlalchemy.url", database_url)

# Configure Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata from SQLAlchemy models
target_metadata = Base.metadata


# Ignore PostGIS system tables
def include_object(object, name, type_, reflected, compare_to):
    postgis_tables = {
        "spatial_ref_sys",
        "geometry_columns",
        "geography_columns",
        "raster_columns",
        "raster_overviews",
        "topology",
        "layer",
    }

    if type_ == "table" and reflected and name in postgis_tables:
        return False

    return True


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
