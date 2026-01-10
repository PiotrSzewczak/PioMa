import logging
from typing import List

from domain.entities import Apartment
from infrastructure.repositories.apartment_repository import ApartmentRepository

logger = logging.getLogger(__name__)


class DynamicSearchUseCase:
    """Use case for fuzzy searching apartments by address."""

    def __init__(self, repository: ApartmentRepository):
        self.repository = repository

    def execute(self, search_query: str, limit: int = 10) -> List[Apartment]:
        """
        Execute fuzzy search and return matching apartments.

        Args:
            search_query: Address fragment to search for.
            limit: Maximum number of results (default 10, for autocomplete).

        Returns:
            List of Apartment entities matching the search criteria.
        """
        if not search_query or not search_query.strip():
            return []

        logger.info(f"Searching for: {search_query}")
        apartments = self.repository.search_by_address(search_query, limit=limit)
        logger.info(f"Found {len(apartments)} matches")

        return apartments


class GetApartmentsByIdsUseCase:
    """Use case for fetching apartments by their IDs."""

    def __init__(self, repository: ApartmentRepository):
        self.repository = repository

    def execute(self, apartment_ids: List[str]) -> List[Apartment]:
        """
        Fetch apartments by list of IDs.

        Args:
            apartment_ids: List of apartment IDs to fetch.

        Returns:
            List of Apartment entities.
        """
        if not apartment_ids:
            return []

        logger.info(f"Fetching {len(apartment_ids)} apartments")
        apartments = self.repository.get_by_ids(apartment_ids)
        logger.info(f"Retrieved {len(apartments)} apartments")

        return apartments

    def execute_single(self, apartment_id: str) -> Apartment | None:
        """
        Fetch a single apartment by ID.

        Args:
            apartment_id: The apartment ID to fetch.

        Returns:
            Apartment entity or None if not found.
        """
        if not apartment_id:
            return None

        return self.repository.get_by_id(apartment_id)
