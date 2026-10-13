#!/usr/bin/env python3
import logging
import os

from pymongo import MongoClient
from pymongo.errors import PyMongoError

MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.getenv("MONGODB_ATLAS_PWD")


def main():
    """Print the books linked to selected authors."""
    logging.basicConfig(level=logging.INFO)
    client = None

    try:
        client = MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
        )
        bookstore = client["bookstore"]
        authors = bookstore["authors"]
        books = bookstore["books"]
        author_ids = ["author_002", "author_003", "author_004"]

        # Count the selected authors in the database.
        author_count = authors.count_documents({"_id": {"$in": author_ids}})
        logging.info("Connected to MongoDB Atlas.")
        print(f"Authors: {author_count}")

        for author in authors.find({"_id": {"$in": author_ids}}):
            print(f"\n{author['name']}")
            # Find books whose author_ids include this author.
            for book in books.find({"author_ids": author["_id"]}):
                print(f"  {book['title']} ({book['published_year']})")

    except PyMongoError as error:
        logging.error("MongoDB error: %s", error)
    finally:
        if client is not None:
            client.close()


if __name__ == "__main__":
    main()
