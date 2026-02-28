# Flask API User

A simple Flask REST API for user management using PostgreSQL and SQLAlchemy ORM.

## Features
- Add new users (username, email)
- List all users
- Prevent duplicate emails
- Timestamps for creation and update

## Project Structure
```
model/          # ORM models
service/        # Business logic
route/          # API routes
script/         # SQL scripts
app.py          # Main app entry
config.py       # Database config
.gitignore      # Git ignore rules
```

## Setup
1. Clone the repository
2. Install dependencies:
  ```
  pip install -r requirements.txt
  ```
3. Configure your database in `config.py` (see `config_example.py`)
4. Create database postgresql from script/001_create_users_table.sql
5. Run the app:
   ```
   flask run
   # or
   python app.py
   ```

## API Endpoints
### Add User
- **POST** `/users`
- Body:
  ```json
  {
    "username": "yourname",
    "email": "your@email.com"
  }
  ```

### List Users
- **GET** `/users`

## Postman
Import `Flask-API-User.postman_collection.json` for ready-to-use requests.

## License
MIT
