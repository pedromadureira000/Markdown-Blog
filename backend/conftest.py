import pytest
from model_bakery import baker
from django.utils.translation import activate
from rest_framework.test import APIClient

client = APIClient() # XXX If using the pytest client, it leads to (Unsupported Media Type) for PUT and PATCH methods.

@pytest.fixture
def logged_user(db, django_user_model):
    user = baker.make(django_user_model, username="test_user", email="test@user.anything")
    password = "safe_password_123"
    user.set_password(password)
    user.save()
    user
    return user


@pytest.fixture
def client_with_logged_user(logged_user):
    client.force_login(logged_user)
    return client

#  @pytest.fixture(autouse=True) <-- FIXME didn't work
#  def set_default_language():
    #  activate('en')
