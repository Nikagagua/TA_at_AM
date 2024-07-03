# Categories API

This is a simple Categories API that stores a category tree in the database and returns category parents, children, and siblings by category ID.

## Requirements

- Python 3.4+
- Django Framework (or Django Rest Framework)

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/Nikagagua/test_assignment_at_admirals.git
    ```

2. Navigate to the project directory:

    ```sh
    cd test_assignment_at_admirals
    ```

3. Create a virtual environment:

    ```sh
    python -m venv venv
    ```

4. Activate the virtual environment:

    ```sh
    source venv/bin/activate
    ```

5. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

6. Run the migrations:

    ```sh
    python manage.py migrate
    ```

7. Run the development server:

    ```sh
    python manage.py runserver
    ```

## Running Tests

To run the tests, use the following command:

```sh
python manage.py test categories
