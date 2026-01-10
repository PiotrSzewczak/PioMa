"""
Main entry point demonstrating use cases.
This file shows how to use the refactored architecture.
In production, this will be replaced by FastAPI endpoints.
"""

import logging

import pandas as pd

from config.config import (
    get_insert_apartments_use_case,
    get_dynamic_search_use_case,
    get_apartments_by_ids_use_case,
)


def main():
    """Example usage of the refactored architecture."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    # Example 1: Insert apartments from CSV
    logger.info("=" * 50)
    logger.info("Example 1: Insert apartments from CSV")
    logger.info("=" * 50)

    addresses_df = pd.read_csv("addresses.csv", sep=";")
    addresses_df = addresses_df.rename(
        columns={
            "ID_new": "apartment_id",
            "Ulica": "street",
            "Numer domu": "house_nr",
            "Miasto": "city",
            "Concat": "full_address",
            "Longitude": "longitude",
            "Latitude": "latitude",
        }
    )

    insert_use_case = get_insert_apartments_use_case()
    result = insert_use_case.execute_from_dataframe(addresses_df)

    logger.info(f"Inserted: {result.inserted_count}")
    logger.info(f"Skipped (duplicates): {result.skipped_count}")
    logger.info(f"Failed: {result.failed_count}")

    # Example 2: Dynamic search (returns full apartment data for autocomplete)
    logger.info("=" * 50)
    logger.info("Example 2: Dynamic search")
    logger.info("=" * 50)

    search_use_case = get_dynamic_search_use_case()
    apartments = search_use_case.execute("Warszawa", limit=5)

    logger.info(f"Found {len(apartments)} apartments:")
    for apt in apartments:
        logger.info(
            f"  - {apt.apartment_id}: {apt.full_address} ({apt.latitude}, {apt.longitude})"
        )

    # Example 3: Get single apartment by ID
    logger.info("=" * 50)
    logger.info("Example 3: Get apartment by ID")
    logger.info("=" * 50)

    if apartments:
        get_by_ids_use_case = get_apartments_by_ids_use_case()
        single_apt = get_by_ids_use_case.execute_single(apartments[0].apartment_id)

        if single_apt:
            logger.info(f"Found: {single_apt.to_dict()}")


if __name__ == "__main__":
    main()
