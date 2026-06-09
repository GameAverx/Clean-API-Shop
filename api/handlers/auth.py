from ..models import query
import hashlib
from ..security import SECRET_KEY
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
        return (400, {'Success': False, "payload": 'Name, email and password required'})

    if not email or not password or not name:
        return (400, {'Success': False, 'payload': 'Name, email and password required'})

    exiting = query(
        '''SELECT id FROM users WHERE email= ?''', (email,), True)
    if exiting:
        return (409, {'Success': False, 'payload': 'User already exists'})

    # хешируем пароль
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        request_db = '''INSERT INTO users (name, email, hashed_password, role) VALUES (?,?,?,?)'''
        query(request_db, (name, email, hashed_password, role))
        return (201, {'Success': True, 'payload': 'User created'})

    except Exception as error:
        print(f"Database error: {error}")
        return (500, {'Success': False, 'payload': 'Internal server error'})


# без валидации данных
def login(body):
    if body:
        email = body.get('email').strip()
        password = body.get('password').strip()
    else:
        return (400, {'Success': False, 'payload': 'Email and password required'})

    if not email or not password:
        return (400, {'Success': False, 'payload': 'Email and password required'})

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
        return (200, {'Success': True, 'token': token, 'payload': 'Successful login'})
    else:
        return (401, {'Success': False, 'payload': 'Invalid data'})



