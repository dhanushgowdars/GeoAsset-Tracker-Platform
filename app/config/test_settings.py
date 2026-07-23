from pydantic_settings import BaseSettings, SettingsConfigDict


class TestSettings(BaseSettings):
    database_url: str = "postgresql://geouser:geopass@127.0.0.1:5433/geoasset_test"

    jwt_secret: str = "your-super-secret-key"

    jwt_algorithm: str = "HS256"

    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


test_settings = TestSettings()
