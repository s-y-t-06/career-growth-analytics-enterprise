"""Initialize the SQLite database for the enterprise backend."""

from backend.app.database import init_database
from backend.app.services.data_service import seed_database


def main() -> None:
    """Create tables and seed data from CSV files."""
    init_database()
    seed_database()
    print("Database initialized and seeded successfully.")


if __name__ == "__main__":
    main()
