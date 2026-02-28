from model.user import User, db

def add_user(username, email):
    existing_user = find_user_by_email(email)
    if existing_user:
        return None, 'Email already exists.'
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user, None

def get_all_users():
    return User.query.filter_by(deleted_at=None).all()

def find_user_by_email(email):
    return User.query.filter_by(email=email).first()