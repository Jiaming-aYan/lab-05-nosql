#!/usr/bin/env python3
"""Print the books linked to selected authors in the bookstore database."""

import logging
import os

from pymongo import MongoClient
from pymongo.errors import PyMongoError


MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.getenv("MONGODB_ATLAS_PWD")


def main() -> int:
    """Connect to Atlas and print each selected author's books."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    if not all((MONGODB_ATLAS_URL, MONGODB_ATLAS_USER, MONGODB_ATLAS_PWD)):
        logging.error("Set MONGODB_ATLAS_URL, MONGODB_ATLAS_USER, and MONGODB_ATLAS_PWD.")
        return 1

    # Include two starter authors and the author added in Case Study 1.
    author_ids = ["author_002", "author_003", "author_004"]
    client = None

    try:
        client = MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
            serverSelectionTimeoutMS=5000,
        )
        client.admin.command("ping")
        logging.info("Connected to MongoDB Atlas.")

        bookstore = client["bookstore"]
        authors = bookstore["authors"]
        books = bookstore["books"]

        author_count = authors.count_documents({"_id": {"$in": author_ids}})
        print(f"Authors: {author_count}")

        for author_id in author_ids:
            author = authors.find_one({"_id": author_id})
            if author is None:
                logging.warning("Author %s was not found.", author_id)
                continue

            print(f"\n{author['name']}")
            # Query author_ids on each book, so co-authored books appear for both authors.
            for book in books.find({"author_ids": author["_id"]}):
                print(f"  {book['title']} ({book['published_year']})")

    except PyMongoError:
        logging.exception("Could not read the bookstore data from MongoDB Atlas.")
        return 1
    finally:
        if client is not None:
            client.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
