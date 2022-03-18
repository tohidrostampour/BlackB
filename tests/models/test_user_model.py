import pytest

from app.accounts.services.user import SQLAlchemyRepository, FakeRepository
from app.accounts.schemas import user as schema_user
from app.accounts.models import user as model_user


@pytest.fixture
def user_models():
    user_1 = model_user.User(
        username='test1',
        email='test1@gmail.com',
        password='test_password',
        name='test1'
    )
    user_2 = model_user.User(
        username='test2',
        email='test2@gmail.com',
        password='test_password',
        name='test2'
    )
    return [user_1, user_2]


def test_user_model_creation_in_db():
    obj = model_user.User(
        username='test',
        email='test@gmail.com',
        password='test_password',
        name='test'
    )
    repo = FakeRepository([])
    created_user = repo.create(obj)

    assert obj.username == created_user.username


def test_get_user(user_models):
    repo = FakeRepository(user_models)
    usr = repo.get(user_models[0].id)
    assert user_models[0].username == usr.username


def test_delete_user(user_models):
    repo = FakeRepository(user_models)

    msg = repo.delete(user_models[0].id)
    assert msg == 'deleted successfully'


def test_list_users(user_models):
    repo = FakeRepository(user_models)
    ls = repo.list()

    assert ls == user_models
