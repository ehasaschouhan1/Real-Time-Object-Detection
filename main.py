import sys

from database import initialize_database
from ui import DetectionUI


def main():
    print("Starting VisionLog...")
    print("Checking MySQL database...")

    try:
        initialize_database()
        print("MySQL database is ready.")
    except Exception as error:
        print("\nMySQL connection failed.")
        print("Make sure MySQL is running and .env credentials are correct.")
        print(f"Details: {error}")
        sys.exit(1)

    app = DetectionUI()
    app.run()


if __name__ == "__main__":
    main()
