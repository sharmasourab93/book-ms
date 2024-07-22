# Book Management System
The Book Management System is an intelligent book management application built using Python, FastAPI, a locally running Llama3 generative AI model, and AWS cloud infrastructure. It allows users to manage books, generate summaries using Llama3, provide book recommendations based on user preferences, and manage user reviews.

### Features
- Add, retrieve, update, and delete books from a PostgreSQL database hosted on AWS RDS
- Generate summaries for books using the Llama3 model
- Provide book recommendations based on genre and average rating
- Manage user reviews and generate rating and review summaries for books
- RESTful API accessible via the internet
- Asynchronous operations for database interactions and AI model predictions
- Basic authentication for the API
- Secure communication with the database and API endpoints

### API Endpoints
1. POST /books: Add a new book
2. GET /books: Retrieve all books
3. GET /books/{id}: Retrieve a specific book by its ID
4. PUT /books/{id}: Update a book's information by its ID
5. DELETE /books/{id}: Delete a book by its ID
6. POST /books/{id}/reviews: Add a review for a book
7. GET /books/{id}/reviews: Retrieve all reviews for a book
8. GET /books/{id}/summary: Get a summary and aggregated rating for a book
9. GET /recommendations: Get book recommendations based on user preferences
10. POST /generate-summary: Generate a summary for a given book content

### Technologies Used
- Python
- FastAPI
- SQLAlchemy
- asyncpg
- PostgreSQL
- AWS RDS
- AWS S3
- AWS Lambda
- AWS CodePipeline

### Getting Started
- *Set up the database*: Create a PostgreSQL database on AWS RDS and run the SQL script to create the books and reviews tables.
- *Configure environment variables*: Set the necessary environment variables for the database connection, AWS credentials, and Llama3 model path.
- *Install dependencies*: Create a virtual environment and install the required dependencies using `pip install -r requirements.txt `
- *Run the application*: Start the FastAPI server using `uvicorn app.main:app --reload`.
- *Access the API*: The API will be accessible at `http://localhost:8000`. You can use tools like Postman or curl to interact with the endpoints.

### Testing
The application includes unit tests for the API endpoints. You can run the tests using the following command:
```bash 
pytest tests/ 
```

### Deployment
The application is deployed on AWS using the following services:
    - EC2: Hosting the FastAPI application
    - Lambda: Running the Llama3 model for generating summaries
    - S3: Storing the Llama3 model files
    - CodePipeline: Automating the deployment process

### Documentation
The API documentation is generated using Swagger and can be accessed at http://localhost:8000/docs.

### Future Improvements
Implement caching for book recommendations using AWS ElastiCache
Use AWS SageMaker for deploying and managing the machine learning model
Add integration tests for the AI model

### Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please create a new issue or submit a pull request.