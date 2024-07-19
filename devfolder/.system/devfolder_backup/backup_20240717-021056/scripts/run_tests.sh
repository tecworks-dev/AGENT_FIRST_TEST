
#!/bin/bash

# scripts/run_tests.sh
# Shell script to run all tests for the AI Software Factory application.

# Set up error handling
set -e

# Set up the test environment
echo "Setting up test environment..."
source venv/bin/activate
export FLASK_ENV=testing
export PYTHONPATH=.

# Run unit tests
echo "Running unit tests..."
python -m pytest tests/test_models.py tests/test_routes.py tests/test_services.py tests/test_utils.py

# Run integration tests
echo "Running integration tests..."
python -m pytest tests/test_integration.py

# Run AI model service tests
echo "Running AI model service tests..."
python -m pytest tests/test_ai_model_service.py

# Run AI service tests
echo "Running AI service tests..."
python -m pytest tests/test_ai_service.py

# Run caching service tests
echo "Running caching service tests..."
python -m pytest tests/test_caching_service.py

# Run code generation service tests
echo "Running code generation service tests..."
python -m pytest tests/test_code_generation_service.py

# Run data persistence service tests
echo "Running data persistence service tests..."
python -m pytest tests/test_data_persistence_service.py

# Run project planning service tests
echo "Running project planning service tests..."
python -m pytest tests/test_project_planning_service.py

# Run user management service tests
echo "Running user management service tests..."
python -m pytest tests/test_user_management_service.py

# Generate coverage report
echo "Generating coverage report..."
coverage run -m pytest
coverage report
coverage html

# Check for any failed tests
if [ $? -ne 0 ]; then
    echo "Some tests failed. Please check the output above for details."
    exit 1
fi

echo "All tests passed successfully!"

# Deactivate the virtual environment
deactivate

exit 0
