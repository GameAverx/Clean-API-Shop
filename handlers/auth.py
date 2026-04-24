from models import query
import hashlib
from security import SECRET_KEY
import jwt
from datetime import datetime, timedelta


# без валидации данных
def register(body):
    if body:
        name = body.get('name').strip()
        email = body.get('email').strip()
        password = body.get('password').strip()
        role = body.get('role').strip()
    else:
        return (400, {'error': 'name, email and password required'})

    if not email or not password or not name:
        return (400, {'error': 'name, email and password required'})

    exiting = query(
        '''SELECT id FROM users WHERE email= ?''', (email,), True)
    if exiting:
        return (409, {'error': 'user already exists'})

    # хешируем пароль
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        request_db = '''INSERT INTO users (name, email, hashed_password, role) VALUES (?,?,?,?)'''
        query(request_db, (name, email, hashed_password, role))
        return (201, {'message': 'user created'})

    except Exception as error:
        print(f"Database error: {error}")
        return (500, {'error': 'Internal server error'})

# без валидации данных
def login(body):
    if body:
        email = body.get('email').strip()
        password = body.get('password').strip()
    else:
        return (400, {'error': 'email and password required'})

    if not email or not password:
        return (400, {'error': 'email and password required'})

    # exiting = query(
    #     '''SELECT id FROM users WHERE email= ?''', (email,), True)
    # if not exiting:
    #     return (409, {'error': 'user not found'})

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    user = query('''SELECT id FROM users WHERE email= ? AND hashed_password= ?''',
                 (email, hashed_password), True)
    if user:
        token = jwt.encode({'user_id': user['id'], 'exp': datetime.now() + timedelta(days=1)},
                           SECRET_KEY,
                           algorithm="HS256")
        return (200, {'token': token, 'message': 'Successful login'})
    else:
        return (401, {'error': 'Invalid data'})



