# Library Management System

A Flask-based API for managing a library system, allowing CRUD operations for books and members. The API includes search functionality and pagination.

## How to Run the Project

### Prerequisites

Ensure the following are installed on your system:

- Python (3.8 or later)
- pip (Python package manager)

### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/atulguptag/library_management_system.git
   cd library_management
   ```

2. **Set up a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the Database**
   Initialize the SQLite database and create the required tables:

   ```bash
   python -c "from app import db; db.create_all()"
   ```

5. **Run the Application**
   Start the Flask development server:
   ```bash
   python app.py
   ```
   The application will be accessible at `http://127.0.0.1:5000`.


## Design Choices Made

### 1. **Framework and Tools**

- **Flask:** Chosen for its simplicity and lightweight nature, suitable for small to medium-scale projects.
- **SQLAlchemy:** Used as the ORM for database interactions to simplify query handling and ensure better maintainability.
- **SQLite:** Used as the database for its ease of use and zero-configuration setup, suitable for development and small-scale applications.

### 2. **Modular Design**

- The project is divided into `app.py` (application logic) and `models.py` (database models), ensuring clear separation of concerns.

### 3. **Validation**

- Custom validation functions are implemented to ensure data integrity for books and members.
- Regular expressions and third-party libraries (e.g., `email_validator`) are used for robust input validation.

### 4. **Pagination**

- Pagination is implemented for retrieving books to handle large datasets efficiently.
- Customizable through `page` and `per_page` query parameters.

### 5. **RESTful API**

- CRUD operations for `books` and `members` are implemented as RESTful endpoints.
- The design ensures scalability and easy integration with frontend clients or other services.

### 6. **Error Handling**

- Errors are returned with appropriate HTTP status codes and messages for better API usability and debugging.


## Assumptions or Limitations

### Assumptions

1. **Book Availability:**
   - Each book has a boolean `available` field to indicate whether it is available for borrowing.
2. **Unique Member Emails:**
   - Each library member must have a unique email address.

### Limitations

1. **Database:**
   - SQLite is used, which is not suitable for production environments with high concurrency or large datasets. Consider upgrading to PostgreSQL or MySQL for production.
2. **Authentication:**
   - The application currently does not implement user authentication or authorization.
3. **Frontend:**
   - No frontend interface is included; all interactions are via RESTful API endpoints.
4. **Scalability:**
   - The current design is suitable for small to medium-scale applications. For larger systems, enhancements like caching, load balancing, and more advanced database optimizations would be required.

## API Endpoints

### Books

- **Create Book:**

  - `POST /books`
  - Request Body: `{ "title": "Book Title", "author": "Author Name", "available": true }`

- **Update Book:**

  - `PUT /books/<book_id>`
  - Request Body: `{ "title": "Updated Title", "author": "Updated Author", "available": false }`

- **Delete Book:**

  - `DELETE /books/<book_id>`

- **Get Books (Paginated):**

  - `GET /books?page=1&per_page=10`

- **Search Books:**
  - `GET /books/search?title=example&author=authorname`

### Members

- **Create Member:**
  - `POST /members`
  - Request Body: `{ "name": "Member Name", "email": "member@example.com" }`

## Test Endpoints Using Postman

1. **Setup:**

   - Install Postman from [postman.com](https://www.postman.com/).
   - Open Postman and create a new request.

2. **Test Book Endpoints:**

   - **Create Book:**
     - Method: `POST`
     - URL: `http://127.0.0.1:5000/books`
     - Body (JSON):
       ```json
       {
         "title": "Book Name",
         "author": "Author Name",
         "available": true
       }
       ```
   - **Update Book:**
     - Method: `PUT`
     - URL: `http://127.0.0.1:5000/books/<book_id>`
     - Body (JSON):
       ```json
       {
         "title": "Updated Book Title",
         "author": "Updated Author",
         "available": false
       }
       ```
   - **Delete Book:**
     - Method: `DELETE`
     - URL: `http://127.0.0.1:5000/books/<book_id>`
   - **Get Books:**
     - Method: `GET`
     - URL: `http://127.0.0.1:5000/books?page=1&per_page=10`
   - **Search Books:**
     - Method: `GET`
     - URL: `http://127.0.0.1:5000/books/search?title=example&author=authorname`

3. **Test Member Endpoints:**

   - **Create Member:**
     - Method: `POST`
     - URL: `http://127.0.0.1:5000/members`
     - Body (JSON):
       ```json
       {
         "name": "John Doe",
         "email": "john.doe@example.com"
       }
       ```

4. **Verify Responses:**
   - Check the status codes and response messages for correctness.
   - Use Postman's history or saved collections to organize and repeat tests.
