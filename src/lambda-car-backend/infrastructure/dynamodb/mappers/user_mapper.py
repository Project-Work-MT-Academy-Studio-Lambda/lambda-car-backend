from domain.user import User
from uuid import UUID

def user_to_dynamodb_item(user: User) -> dict:
    return {
        'id': str(user.id),
        'name': user.name,
        'email': user.email,
        'password': user.password,
        'role': user.role.value
    }

def dynamodb_item_to_user(item: dict) -> User:
    return User(
        id=UUID(item['id']),
        name=item['name'],
        email=item['email'],
        password=item['password'],
        role=item['role']
    )