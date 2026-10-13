// Step 2: select the bookstore database.
db = db.getSiblingDB("bookstore");

// Step 3: replace the authors collection with the starter data.
db.authors.drop();
var authorDocs = JSON.parse(fs.readFileSync("authors.json", "utf8"));
db.authors.insertMany(authorDocs);

// Step 4: replace the books collection with the starter data.
db.books.drop();
var bookDocs = JSON.parse(fs.readFileSync("books.json", "utf8"));
db.books.insertMany(bookDocs);

// Step 5: list all starter authors and books.
printjson(db.authors.find().toArray());
printjson(db.books.find().toArray());

// Step 6: add two books. Emma uses an existing author; Animal Farm uses a new one.
db.books.insertMany([
  {
    title: "Emma",
    published_year: 1815,
    author_ids: ["author_001"]
  },
  {
    title: "Animal Farm",
    published_year: 1945,
    author_ids: ["author_004"]
  }
]);

// Step 7: add the missing author referenced by Animal Farm.
db.authors.insertOne({
  _id: "author_004",
  name: "George Orwell",
  nationality: "British",
  bio: {
    short: "British novelist and essayist.",
    long: "George Orwell wrote novels and essays about politics, society, and language."
  }
});

// Step 8: find books by an existing author and the newly added author.
printjson(db.books.find({
  author_ids: { $in: ["author_001", "author_004"] }
}).toArray());
