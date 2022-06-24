import json
from django.urls import reverse
import pytest
from model_bakery import baker
from django_assertions import assert_iqual, assert_json_equal

#XXX This is needed for PUT and PATCH methods, since the client from pytest (django.test.Client instance) leads to "Unsupported Media Type" error
from rest_framework.test import APIClient
drf_client = APIClient()  


@pytest.fixture
def user(django_user_model):
    user = baker.make(django_user_model)
    password = "ThisPassword123@"
    user.set_password(password)
    user.save()
    user.plain_text_password = password
    return user

#--------------------------------------/ getcsrf


@pytest.fixture
def get_csrf_token(client):
    return client.get(reverse('get_csrf_token'))

def test__get_csrf_token(get_csrf_token):
    assert get_csrf_token.status_code == 200
    assert_iqual(get_csrf_token.content, b'"The CSRF cookie was sent"')

#--------------------------------------/ Login

@pytest.fixture
def login_fail__without_credentials(client):
    return client.post(reverse('login'))

def test__login_fail__without_credentials(login_fail__without_credentials):
    assert login_fail__without_credentials.status_code == 400 # Error: Bad Request
    assert_json_equal(login_fail__without_credentials.content,
        {
          "username": [
            #  "Este campo é obrigatório."
            "This field is required."
          ],
          "password": [
            "This field is required."
          ]
        }
    )

@pytest.fixture
def login_successful(client, user):
    return client.post(reverse('login'), {'username': user.username, 'password': user.plain_text_password}, format='json')

def test__login_successful_response(login_successful, user):
    assert login_successful.status_code == 200
    assert_json_equal(login_successful.content,
        {
          "username": user.username,
          "email": user.email,
        }
    )

@pytest.fixture
def authenticated_user_tries_to_login(client_with_logged_user):
    return client_with_logged_user.post(reverse('login'), {'username': 'some_username', 'password': 'somepassword123'}, format='json')

def test__authenticated_user_tries_to_login__response(authenticated_user_tries_to_login):
    assert authenticated_user_tries_to_login.status_code == 200
    assert_iqual(authenticated_user_tries_to_login.content,
        b'"User is already authenticated"'
    )

#--------------------------------------/ check_authenticated

@pytest.fixture
def check_authenticated(client_with_logged_user):
    return client_with_logged_user.get(reverse('check_authenticated'))

def test__check_authenticated(check_authenticated):
    assert check_authenticated.status_code == 200
    assert_json_equal(check_authenticated.content,
        {
          "username": "test_user",
          "email": "test@user.anything",
        }
    )

@pytest.fixture
def check_authenticated_fail(client):
    return client.get(reverse('check_authenticated'))

def test__check_authenticated_fail__without_credentials(check_authenticated_fail):
    assert check_authenticated_fail.status_code == 403 # Error: Forbidden
    assert_json_equal(check_authenticated_fail.content,
        {
          "detail": "Authentication credentials were not provided."
        }
    )

#--------------------------------------/ Logout

@pytest.fixture
def logout_successful(client_with_logged_user):
    return client_with_logged_user.post(reverse('logout'))

def test__logout_successful(logout_successful):
    assert logout_successful.status_code == 200
    assert_iqual(logout_successful.content, b'"Logged out"')

@pytest.fixture
def logout_fail__credentials_were_not_provided(client):
    return client.post(reverse('logout'))

def test__logout_fail__credentials_were_not_provided(logout_fail__credentials_were_not_provided):
    assert logout_fail__credentials_were_not_provided.status_code == 403 #Forbidden
    assert_json_equal(logout_fail__credentials_were_not_provided.content,
        {
          "detail": "Authentication credentials were not provided."
        }
    )

#--------------------------------------/ update_own_password

@pytest.fixture
def update_own_password_successful(client_with_logged_user):
    return client_with_logged_user.put(reverse('update_own_password'),
        data={
          'password': 'another_safe_password_123',
          'current_password': 'safe_password_123'
        }, format='json'

    )

def test__update_own_password_successful(update_own_password_successful):
    assert update_own_password_successful.status_code == 200
    assert_iqual(update_own_password_successful.content,
        b'"Password updated"'
    )


@pytest.fixture
def update_own_password_fail__passwords_dont_match(client_with_logged_user):
    return client_with_logged_user.put(reverse('update_own_password'),
        {
          "password": "wrong_password",
          "current_password": "wrong_current_password"
        }, format="json"
    )

def test__update_own_password_fail(update_own_password_fail__passwords_dont_match):
    assert update_own_password_fail__passwords_dont_match.status_code == 400 #Bad request
    assert_json_equal(update_own_password_fail__passwords_dont_match.content,
        {
          "error": [
            "passwords don't match"
          ]
        }
    )

@pytest.fixture
def update_own_password_fail__authentication_error(client):
    return client.put(reverse('update_own_password'))

def test__update_own_password_fail__authentication_error(update_own_password_fail__authentication_error):
    assert update_own_password_fail__authentication_error.status_code == 403 #Forbidden
    assert_json_equal(update_own_password_fail__authentication_error.content,
        {
          "detail": "Authentication credentials were not provided."
        }
    )
