import data
import sender_state_request


def get_user_body(first_name):
    """Return a copy of the default user body with updated firstName."""
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body


def positive_assert(first_name: str):
    """Check that a valid user is created successfully."""
    user_body = get_user_body(first_name)
    response = sender_state_request.post_new_user(user_body)

    assert response.status_code == 201
    assert response.json(), "Response JSON should not be empty"

    users_table = sender_state_request.get_users_table()
    expected_user = (
        f'{user_body["firstName"]},{user_body["phone"]},'
        f'{user_body["address"]},,,{response.json()["authToken"]}'
    )

    assert (
        users_table.text.count(expected_user) == 1
    ), "User should appear exactly once in users table"


def negative_assert(first_name: str):
    """Check that an invalid firstName returns an error."""
    user_body = get_user_body(first_name)
    response = sender_state_request.post_new_user(user_body)

    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert (
        response.json()["message"]
        == "Имя пользователя введено некорректно. Имя может содержать только "
        "русские или латинские буквы, длина должна быть не менее 2 и не более 15 символов"
    )


def negative_assert_no_first_name(user_body: dict):
    """Check that missing firstName returns an error."""
    response = sender_state_request.post_new_user(user_body)

    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "Не все необходимые параметры были переданы"


# --- Tests ---

def test_create_user_with_2_letters():
    """User created successfully: firstName has 2 letters."""
    positive_assert("Фф")


def test_create_user_with_15_letters():
    """User created successfully: firstName has 15 letters."""
    positive_assert("Ффффффффффффффф")


def test_create_user_with_1_letter():
    """User not created: firstName has only 1 letter."""
    negative_assert("Ф")


def test_create_user_with_16_letters():
    """User not created: firstName has 16 letters."""
    negative_assert("Фффффффффффффффф")


def test_create_user_with_english_letters():
    """User created successfully: firstName contains English letters."""
    positive_assert("Qwerty")


def test_create_user_with_russian_letters():
    """User created successfully: firstName contains Russian letters."""
    positive_assert("Саша")


def test_create_user_with_space():
    """User not created: firstName contains a space."""
    negative_assert("Са ша")


def test_create_user_with_special_symbols():
    """User not created: firstName contains special symbols."""
    negative_assert("%#@№")


def test_create_user_with_numbers():
    """User not created: firstName contains digits."""
    negative_assert("12345")


def test_create_user_without_first_name():
    """User not created: firstName is missing."""
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    negative_assert_no_first_name(user_body)


def test_create_user_with_empty_first_name():
    """User not created: firstName is empty."""
    user_body = get_user_body("")
    negative_assert_no_first_name(user_body)


def test_create_user_with_number_type_first_name():
    """User not created: firstName is not a string (int instead)."""
    user_body = get_user_body(13)
    response = sender_state_request.post_new_user(user_body)

    assert response.status_code == 400
