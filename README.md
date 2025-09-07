# API Tests for User Creation

This repository contains automated Tests for validating the `firstName` parameter when creating a user in Yandex.Prilavok using the Yandex.Prilavok API. 

## Features

- Positive tests for valid user creation (length, Russian/English letters).  
- Negative tests for invalid inputs (too short/long, spaces, special symbols, digits, missing parameter).  
- Clear separation of reusable assert functions.  
- Easy to extend with new test cases.  

## Project Structure

- data.py                    Test data (default user body)
- sender_state_request.py    API request functions
- test_create_user.py        Test cases (this file)
- requirements.txt           Dependencies

## Running Tests

Run all tests with:
```bash
pytest -v
```

Run a specific test with:
```bash
pytest -v -k "test_create_user_with_english_letters"
```

## Notes

- The API endpoints are defined in `sender_state_request.py`.  
- Test data (like default `user_body`) is stored in `data.py`.  
- Make sure the API server is running before executing the tests.
