from datetime import datetime
import os
import json
import psycopg2

# Database connection details
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PWD")
DB_PORT = os.environ.get("DB_PORT")
db_host = os.environ.get("DB_HOST")
db_name = os.environ.get("DB")

# Connect to the database
conn = psycopg2.connect(
    host=db_host,
    port=DB_PORT,
    database=db_name,
    user=db_user,
    password=db_password
)

# Create a cursor
cur = conn.cursor()

# Load books data from JSON file
with open('books.json') as books_file:
    books_data = json.load(books_file)

# Load reviews data from JSON file
with open('reviews.json') as reviews_file:
    reviews_data = json.load(reviews_file)

# Insert books data
for book in books_data:
    cur.execute("""
        INSERT INTO books (title, author, genre, published_year, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (title) DO NOTHING;  -- Prevents duplicate entries
    """, (book['title'], book['author'], book['genre'], book['published_year'],
          datetime.utcnow(), datetime.utcnow()))

# Insert reviews data
for review in reviews_data:
    # Assuming you have a way to get the corresponding book_id for each review
    # For example, you might need to query the database to find the book_id based on the title
    book_id = 1  # Replace with actual logic to get the book_id
    cur.execute("""
        INSERT INTO reviews (user_name, review_text, rating, book_id, created_at)
        VALUES (%s, %s, %s, %s, %s);
    """, (review['user_name'], review['review_text'], review['rating'], book_id,
          datetime.utcnow()))

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()

print("Data inserted successfully.")