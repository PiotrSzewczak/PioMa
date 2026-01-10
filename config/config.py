import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

from infrastructure.database import Database
from infrastructure.repositories.apartment_repository import ApartmentRepository
from services.geocoder import GeocoderService
from application.use_cases import (
    InsertApartmentsUseCase,
    DynamicSearchUseCase,
    GetApartmentsByIdsUseCase,
)

load_dotenv()


@dataclass
class Settings:
    """Application settings from environment variables."""

    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    @classmethod
    def from_env(cls) -> "Settings":
        """Create settings from environment variables."""
        return cls(
            db_host=os.getenv("POSTGRES_HOST", "localhost"),
            db_port=int(os.getenv("POSTGRES_PORT", "5432")),
            db_name=os.getenv("POSTGRES_DB", "postgres"),
            db_user=os.getenv("POSTGRES_USER", "postgres"),
            db_password=os.getenv("POSTGRES_PASSWORD", ""),
        )


@lru_cache
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings.from_env()


def get_database() -> Database:
    """Create database instance from settings."""
    settings = get_settings()
    return Database(
        host=settings.db_host,
        port=settings.db_port,
        database=settings.db_name,
        user=settings.db_user,
        password=settings.db_password,
    )


def get_repository() -> ApartmentRepository:
    """Create apartment repository with database."""
    db = get_database()
    return ApartmentRepository(db)


def get_geocoder() -> GeocoderService:
    """Create geocoder service."""
    return GeocoderService()


# Use case factories - these are what FastAPI will use
def get_insert_apartments_use_case() -> InsertApartmentsUseCase:
    """Create InsertApartmentsUseCase with dependencies."""
    return InsertApartmentsUseCase(
        repository=get_repository(),
        geocoder=get_geocoder(),
    )


def get_dynamic_search_use_case() -> DynamicSearchUseCase:
    """Create DynamicSearchUseCase with dependencies."""
    return DynamicSearchUseCase(repository=get_repository())


def get_apartments_by_ids_use_case() -> GetApartmentsByIdsUseCase:
    """Create GetApartmentsByIdsUseCase with dependencies."""
    return GetApartmentsByIdsUseCase(repository=get_repository())
