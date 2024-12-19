import re
from models import Book, Member, db
from flask import Flask, request, jsonify
from email_validator import validate_email

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db.init_app(app)

with app.app_context():
    db.create_all()

# Custom validation functions
def validate_book_data(data):
    """Validate book input data."""
    if not data:
        return False, "No data provided"

    required_fields = ['title', 'author']
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
        if not isinstance(data[field], str):
            return False, f"{field} must be a string"
        if not data[field].strip():
            return False, f"{field} cannot be empty"

    return True, ""


def validate_member_data(data):
    """Validate member input data."""
    if not data:
        return False, "No data provided"

    required_fields = ['name', 'email']
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
        if not isinstance(data[field], str):
            return False, f"{field} must be a string"
        if not data[field].strip():
            return False, f"{field} cannot be empty"

    # Validate name format
    if not re.match(r'^[a-zA-Z\s-]{2,50}$', data['name']):
        return False, "Name must be 2-50 characters and contain only letters, spaces, and hyphens"

    # Validate email
    if not validate_email(data['email']):
        return False, "Invalid email address"

    return True, ""


def validate_pagination_params(page: str, per_page: str) -> tuple[bool, str, dict]:
    """Validate pagination parameters."""
    try:
        page_num = int(page) if page else 1
        items_per_page = int(per_page) if per_page else 10

        if page_num < 1:
            return False, "Page number must be positive", {}

        if items_per_page < 1 or items_per_page > 100:
            return False, "Items per page must be between 1 and 100", {}

        return True, "", {"page": page_num, "per_page": items_per_page}

    except ValueError:
        return False, "Invalid pagination parameters", {}


# CRUD Operations for Books
@app.route('/books', methods=['POST'])
def create_book():
    """Create a new book entry"""
    data = request.get_json()

    # Validate input data
    is_valid, error_message = validate_book_data(data)
    if not is_valid:
        return jsonify({'error': 'Validation failed', 'message': error_message}), 400

    # Create and save new book
    new_book = Book(
        title=data['title'].strip(),
        author=data['author'].strip(),
        available=data.get('available', True)
    )
    db.session.add(new_book)
    db.session.commit()

    return jsonify({
        'message': 'Book created successfully',
        'book': new_book.to_dict()
    }), 201


@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """Update a specific book's information"""
    data = request.get_json()

    # Validate input data if provided
    if any(key in data for key in ['title', 'author']):
        is_valid, error_message = validate_book_data(data)
        if not is_valid:
            return jsonify({'error': 'Validation failed', 'message': error_message}), 400

    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Not found', 'message': 'Book not found'}), 404

    # Update book fields
    if 'title' in data:
        book.title = data['title'].strip()
    if 'author' in data:
        book.author = data['author'].strip()
    if 'available' in data:
        book.available = bool(data['available'])

    db.session.commit()

    return jsonify({
        'message': 'Book updated successfully',
        'book': book.to_dict()
    }), 200


@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Delete a specific book"""
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Not found', 'message': 'Book not found'}), 404

    db.session.delete(book)
    db.session.commit()

    return jsonify({'message': 'Book deleted successfully'}), 200

# CRUD Operations for Members


@app.route('/members', methods=['POST'])
def create_member():
    """Create a new library member"""
    data = request.get_json()

    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Validation failed", "message": "Name and Email are required"}), 400

    new_member = Member(name=data['name'], email=data['email'])
    db.session.add(new_member)
    db.session.commit()

    return jsonify({
        'message': 'Member created successfully',
        'member': new_member.to_dict()
    }), 201


@app.route('/books/search', methods=['GET'])
def search_books():
    """Search books by title and/or author"""
    title = request.args.get('title', '').strip()
    author = request.args.get('author', '').strip()

    if not title and not author:
        return jsonify({'error': 'Bad request', 'message': 'At least one search parameter (title or author) is required'}), 400

    query = Book.query
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))

    books = query.all()

    return jsonify({
        'count': len(books),
        'books': [book.to_dict() for book in books]
    }), 200


@app.route('/books', methods=['GET'])
def get_books():
    """Get paginated list of books"""
    is_valid, error_message, params = validate_pagination_params(
        request.args.get('page'),
        request.args.get('per_page')
    )

    if not is_valid:
        return jsonify({'error': 'Bad request', 'message': error_message}), 400

    books_pagination = Book.query.paginate(
        page=params['page'],
        per_page=params['per_page'],
        error_out=False
    )

    return jsonify({
        'total_books': books_pagination.total,
        'total_pages': books_pagination.pages,
        'current_page': books_pagination.page,
        'per_page': books_pagination.per_page,
        'has_next': books_pagination.has_next,
        'has_prev': books_pagination.has_prev,
        'books': [book.to_dict() for book in books_pagination.items]
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
