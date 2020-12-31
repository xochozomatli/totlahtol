from app.models  import User

def test_simplest():
    assert True

def test_user():
    u = User()
    assert User() is not None
