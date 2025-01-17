Create a file named 'app/static/js/utils.js' with the following description:                 
                Utility functions for the frontend.
                Contents:
                - Helper functions for common tasks
                - Date formatting
                - Input validation
            

For python files include famework such as unittest


Here's the overall application plan which you should follow while writing the file:
<?xml version="1.0" encoding="UTF-8"?>
<application_plan>
    <components>        
        - Flask web application (backend)
        - Flask web application (frontend)
        - Asynchronous capabilities using asyncio
        - AI interaction through the Anthropic API
        - Comprehensive error handling and recovery
        - Interactive user feedback processing
        - Automated unit test generation and execution
        - Modular design for scalability and maintainability
        - WebSocket support for real-time communications
        - SQLAlchemy ORM for database interactions
        - User authentication and management
        - Encryption service for secure data handling
        - File handling and backup services
        - Push notification service
        - Web browsing and research agent
        - State monitoring and project tracking system
        - Version control system integration
        - Dependency management system
        - Code review interface
        - Deployment automation
        - Documentation generator
        - Performance monitoring and analysis tools
        - User feedback collection mechanism
        - Feedback analysis service
        - Priority assessment for feature requests and bug reports
        - Agile sprint planning integration
    </components>
    <files>
        <file>
            <description>                
                Analyzes code complexity using various metrics.
                
                import ast
                from radon.complexity import cc_visit
                from radon.metrics import mi_visit
                Classes:
                - CodeComplexityAnalyzer:
                Methods:
                - calculate_cyclomatic_complexity(self, code: str) -&gt; int
                - calculate_cognitive_complexity(self, code: str) -&gt; int
                - generate_complexity_report(self, project_path: str) -&gt; Dict[str, Any]
            </description>
            <name>app/utils/code_complexity_analyzer.py</name>
        </file>
        <file>
            <description>                
                Analyzes project structure and provides insights.
                
                import os
                import ast
                Classes:
                - ProjectAnalyzer:
                Methods:
                - analyze_project_structure(self, project_path: str) -&gt; Dict[str, Any]
                - identify_code_smells(self, project_path: str) -&gt; List[Dict[str, str]]
                - suggest_refactoring(self, project_path: str) -&gt; List[Dict[str, str]]
            </description>
            <name>app/utils/project_analyzer.py</name>
        </file>
        <file>
            <name>app/utils/feature_flags.py</name>
            <description>                
                Implements feature flag functionality for the application.
                from typing import Dict, Any
                Classes:
                - FeatureFlags:
                Methods:
                - __init__(self, config: Dict[str, Any])
                - is_enabled(self, feature_name: str) -&gt; bool: Checks if a feature is enabled
                - enable_feature(self, feature_name: str) -&gt; None: Enables a feature
                - disable_feature(self, feature_name: str) -&gt; None: Disables a feature
                - get_all_flags(self) -&gt; Dict[str, bool]: Returns the status of all feature flags
            </description>
        </file>
        <file>
            <description>                
                Base HTML layout template for the web UI.
                Contents:
                - HTML structure with placeholders for dynamic content
                - Links to CSS and JavaScript files
                - Meta tags and other common HTML elements
            </description>
            <name>app/templates/layout.html</name>
        </file>
        <file>
            <description>CSS file for project-specific styles</description>
            <name>app/static/css/project.css</name>
        </file>
        <file>
            <description>CSS file for task-specific styles</description>
            <name>app/static/css/task.css</name>
        </file>
        <file>
            <description>CSS file for user profile styles</description>
            <name>app/static/css/user_profile.css</name>
        </file>
        <file>
            <description>                
                CSS for layout and responsive design.
                Contents:
                - Grid system
                - Responsive breakpoints
                - Layout utilities
            </description>
            <name>app/static/css/layout.css</name>
        </file>
        <file>
            <description>                
                CSS for reusable UI components.
                Contents:
                - Styles for buttons, forms, modals, etc.
            </description>
            <name>app/static/css/components.css</name>
        </file>
        <file>
            <description>                
                Centralizes API calls to the backend.
                Contents:
                - Functions for making AJAX requests to various API endpoints
                - Error handling for API calls
            </description>
            <name>app/static/js/api.js</name>
        </file>
        <file>
            <name>app/utils/input_validator.py</name>
            <description>                
                Centralizes input validation and sanitization for the application.
                
                import re
                from email_validator import validate_email, EmailNotValidError
                Classes:
                - InputValidator:
                Methods:
                - validate_string(self, input: str, min_length: int, max_length: int) -&gt; bool:
                Validates string input
                - validate_email(self, email: str) -&gt; bool: Validates email addresses
                - validate_integer(self, input: str, min_value: int, max_value: int) -&gt; bool:
                Validates integer input
                - sanitize_input(self, input: str) -&gt; str: Sanitizes input to prevent XSS attacks
                This new file provides a centralized location for input validation and sanitization,
                improving security and reducing code duplication across the application.
            </description>
        </file>
        <file>
            <name>app/utils/error_handler.py</name>
            <description>                
                Implements a global exception handler and centralizes error handling logic.
                from flask import jsonify
                from werkzeug.exceptions import HTTPException
                Functions:
                - handle_error(error: Exception) -&gt; Tuple[str, int]: Handles and logs errors
                - log_error(error: Exception, context: Dict[str, Any]) -&gt; None: Logs detailed error
                information
                
                Classes:
                - GlobalExceptionHandler:
                Methods:
                - __init__(self, app: Flask)
                - handle_exception(self, error: Exception) -&gt; Response: Handles uncaught exceptions
                globally
                
                This updated file includes a global exception handler to catch and properly handle
                any uncaught exceptions in the application, improving overall error management and
                logging.
            </description>
        </file>
        <file>
            <description>                
                Checks for code similarity to detect potential plagiarism or code
                duplication.
                
                from difflib import SequenceMatcher
                Classes:
                - CodeSimilarityChecker:
                Methods:
                - check_similarity(self, code1: str, code2: str) -&gt; float
                - find_similar_code_blocks(self, project_id: int) -&gt; List[Dict[str, Any]]
            </description>
            <name>app/utils/code_similarity_checker.py</name>
        </file>
        <file>
            <description>                
                Configuration file for Alembic (database migration tool).
                Contents:
                - Alembic settings
                - Migration script locations
            </description>
            <name>migrations/alembic.ini</name>
        </file>
        <file>
            <description>                
                Configuration settings for the application.
                Imports: os
                Classes:
                - Config:
                Attributes:
                - SECRET_KEY: str
                - SQLALCHEMY_DATABASE_URI: str
                - ANTHROPIC_API_KEY: str
                - MAX_TOKENS: int
                - TEMPERATURE: float
                - DevelopmentConfig(Config):
                Additional development-specific settings
                - ProductionConfig(Config):
                Additional production-specific settings
                Functions:
                - get_config() -&gt; Config: Returns the appropriate configuration based on the
                environment
            </description>
            <name>config.py</name>
        </file>
        <file>
            <description>                
                Contains integration tests for the application.
                Contents:
                - End-to-end test cases
                - API integration tests
                - Database integration tests
            </description>
            <name>tests/test_integration.py</name>
        </file>
        <file>
            <description>                
                Contains tests for the application routes.
                import pytest
                from flask import url_for
                from app.models import User, Project, Task
                Contents:
                - Test cases for different HTTP endpoints
                - Authentication tests
                - Response validation tests
            </description>
            <name>tests/test_routes.py</name>
        </file>
        <file>
            <description>                
                Contains unit tests for database models.
                import pytest
                from app.models import User, Project, Task
                Contents:
                - Test cases for User, Project, Task, and File models
                - Relationship tests
                - Model method tests
            </description>
            <name>tests/test_models.py</name>
        </file>
        <file>
            <description>                
                Contains unit tests for the AI model service.
                Contents:
                - Test cases for model loading
                - Test cases for response generation
                - Test cases for model fine-tuning
            </description>
            <name>tests/test_ai_model_service.py</name>
        </file>
        <file>
            <description>                
                Contains unit tests for the AI service.
                Contents:
                - Test cases for various AI service methods
                - Mock API responses
                - Edge case handling tests
            </description>
            <name>tests/test_ai_service.py</name>
        </file>
        <file>
            <description>                
                Contains unit tests for the caching service.
                Contents:
                - Test cases for caching operations
                - Cache expiration tests
                - Edge case handling
            </description>
            <name>tests/test_caching_service.py</name>
        </file>
        <file>
            <description>                
                Contains unit tests for the code generation service.
                Contents:
                - Test cases for code generation
                - Test cases for code refactoring
            </description>
            <name>tests/test_code_generation_service.py</name>
        </file>
        <file>
            <description>                
                Contains unit tests for the data persistence service.
                Contents:
                - Test cases for saving and loading project states
                - Test cases for project backup functionality
            </description>
            <name>tests/test_data_persistence_service.py</name>
        </file>
        <file>
            <description>                
                Contains unit tests for the project planning service.
                Contents:
                - Test cases for project plan generation
                - Test cases for plan updates
            </description>
            <name>tests/test_project_planning_service.py</name>
        </file>
        <file>
            <description>                
                Contains unit tests for the user management service.
                Contents:
                - Test cases for user creation, update, and deletion
                - Test cases for retrieving user projects
            </description>
            <name>tests/test_user_management_service.py</name>
        </file>
        <file>
            <description>                
                Defines custom exceptions for the application.
                Classes:
                - AIServiceException(Exception)
                - DatabaseConnectionError(Exception)
                - InvalidInputError(Exception)
                - AuthenticationError(Exception)
            </description>
            <name>app/utils/custom_exceptions.py</name>
        </file>
        <file>
            <description>                
                Defines fixtures and configuration for pytest.
                import pytest
                from app import create_app, db
                from app.models import User, Project, Task
                Contents:
                - Test database setup
                - Application context creation
                - Mock object definitions
            </description>
            <name>tests/conftest.py</name>
        </file>
        <file>
            <description>                
                Defines various Flask routes for the application.
                from flask import Blueprint, render_template, request, jsonify
                from flask_login import login_required, current_user
                from app.models import User, Project, Task
                from app.services import (
                AIService, ProjectManager, TaskManager, FileManager,
                WebBrowsingService, StateMonitoringService
                )
                Functions:
                - index() -&gt; str: Home page route
                - user_profile(user_id: int) -&gt; str: User profile page
                - create_project() -&gt; str: Creates a new project
                - update_task(task_id: int, status: str) -&gt; str: Updates task status
                - browse_web(query: str) -&gt; str: Initiates web browsing for research
            </description>
            <name>app/routes/__init__.py</name>
        </file>
        <file>
            <description>                
                Detects the programming language of a given code snippet.
                
                from pygments.lexers import guess_lexer
                Classes:
                - LanguageDetector:
                Methods:
                - detect_language(self, code: str) -&gt; str
            </description>
            <name>app/utils/language_detector.py</name>
        </file>
        <file>
            <description>                
                Email template for password reset.
                Contents:
                - HTML structure for password reset email
                - Reset link placeholder
            </description>
            <name>app/templates/email/reset_password.html</name>
        </file>
        <file>
            <description>                
                Enforces coding style guidelines for different programming languages.
                import pylint.lint
                from pylint.reporters.text import TextReporter
                Classes:
                - CodeStyleEnforcer:
                Methods:
                - enforce_style(self, code: str, language: str, style_guide: str) -&gt; str
                - check_style_violations(self, code: str, language: str, style_guide: str) -&gt;
                List[Dict[str, Any]]
            </description>
            <name>app/utils/code_style_enforcer.py</name>
        </file>
        <file>
            <description>                
                Entry point for the application. Orchestrates the entire process from
                planning to feedback incorporation.
                import asyncio
                from flask import Flask
                from config import Config
                from app import create_app
                from app.services import AIService, ProjectManager, TaskManager, FileManager
                Functions:
                - main() -&gt; None: Initializes and runs the application.
                Classes:
                - AISoftwareFactory:
                Methods:
                - __init__(self, config: Config) -&gt; None
                - run(self) -&gt; None
                - plan_project(self, requirements: str) -&gt; Dict[str, Any]
                - generate_code(self, plan: Dict[str, Any]) -&gt; List[File]
                - fix_errors(self, files: List[File]) -&gt; List[File]
                - incorporate_feedback(self, feedback: str, files: List[File]) -&gt; List[File]
                - create_tests(self, files: List[File]) -&gt; List[File]
            </description>
            <name>main.py</name>
        </file>
        <file>
            <description>                
                Example environment variable file.
                Contents:
                - Placeholder values for configuration settings
                - Instructions for setting up the actual .env file
            </description>
            <name>.env.example</name>
        </file>
        <file>
            <description>Favicon for the application.</description>
            <name>app/static/img/favicon.ico</name>
        </file>
        <file>
            <description>                
                Formats code according to specified style guidelines.
                
                import black
                import isort
                Classes:
                - CodeFormatter:
                Methods:
                - format_code(self, code: str, language: str, style_guide: str) -&gt; str
                - detect_style_violations(self, code: str, language: str, style_guide: str) -&gt;
                List[Dict[str, Any]]
            </description>
            <name>app/utils/code_formatter.py</name>
        </file>
        <file>
            <description>                
                Generates AI prompts for various tasks.
                Classes:
                - AIPromptGenerator:
                Methods:
                - generate_code_prompt(self, task: str) -&gt; str
                - generate_test_prompt(self, code: str) -&gt; str
                - generate_refactor_prompt(self, code: str, issue: str) -&gt; str
            </description>
            <name>app/utils/ai_prompt_generator.py</name>
        </file>
        <file>
            <description>                
                Generates API documentation for the project.
                from typing import List, Dict
                Classes:
                - APIDocumentationService:
                Methods:
                - generate_api_docs(self, project_id: int) -&gt; str
                - update_api_docs(self, project_id: int, changes: List[Dict[str, Any]]) -&gt; bool
            </description>
            <name>app/services/api_documentation_service.py</name>
        </file>
        <file>
            <description>                
                Generates visualizations for project data and metrics.
                from typing import Dict, Any
                import matplotlib.pyplot as plt
                import io
                Classes:
                - DataVisualizationService:
                Methods:
                - generate_project_progress_chart(self, project_id: int) -&gt; bytes
                - generate_code_quality_heatmap(self, project_id: int) -&gt; bytes
                - generate_performance_trend_graph(self, project_id: int) -&gt; bytes
            </description>
            <name>app/services/data_visualization_service.py</name>
        </file>
        <file>
            <description>                
                Handles AI-driven code generation tasks.
                from typing import Dict, Any, List, Tuple
                from app.utils.api_utils import AsyncAnthropic
                import os
                Classes:
                - CodeGenerationService:
                Methods:
                - generate_code(self, specifications: Dict[str, Any]) -&gt; List[Tuple[str,
                str]]
                - refactor_code(self, code: str, refactor_instructions: str) -&gt; str
            </description>
            <name>app/services/code_generation_service.py</name>
        </file>
        <file>
            <description>                
                Handles AI-driven project planning tasks.
                from typing import Dict, Any
                from app.utils.api_utils import AsyncAnthropic
                import os
                Classes:
                - ProjectPlanningService:
                Methods:
                - generate_project_plan(self, requirements: str) -&gt; Dict[str, Any]
                - update_project_plan(self, current_plan: Dict[str, Any], new_requirements: str)
                -&gt; Dict[str, Any]
            </description>
            <name>app/services/project_planning_service.py</name>
        </file>
        <file>
            <description>                
                Handles AI-driven test generation and execution.
                from typing import Dict, Any
                import unittest
                import io
                import sys
                Classes:
                - TestingService:
                Methods:
                - generate_tests(self, code: str) -&gt; str
                - run_tests(self, code: str, tests: str) -&gt; Dict[str, Any]
            </description>
            <name>app/services/testing_service.py</name>
        </file>
        <file>
            <name>app/utils/feature_flags.py</name>
            <description>                
                Implements feature flag functionality for the application.
                from typing import Dict, Any
                Classes:
                - FeatureFlags:
                Methods:
                - __init__(self, config: Dict[str, Any])
                - is_enabled(self, feature_name: str) -&gt; bool: Checks if a feature is enabled
                - enable_feature(self, feature_name: str) -&gt; None: Enables a feature
                - disable_feature(self, feature_name: str) -&gt; None: Disables a feature
                - get_all_flags(self) -&gt; Dict[str, bool]: Returns the status of all feature flags
                This new file provides a centralized way to manage feature flags, allowing for easy
                enabling/disabling of features across the application.
            </description>
        </file>
        <file>
            <name>app/static/js/websocket.js</name>
            <description>                
                Handles WebSocket connections with enhanced authentication and message
                validation.
                Functions:
                - initWebSocket(token: string) -&gt; WebSocket: Initializes a new WebSocket connection
                with authentication
                - sendMessage(socket: WebSocket, message: object) -&gt; void: Sends a validated message
                through the WebSocket
                - handleMessage(event: MessageEvent) -&gt; void: Handles incoming messages with proper
                validation
                - authenticate(socket: WebSocket, token: string) -&gt; void: Authenticates the
                WebSocket connection
                
                This updated file includes proper authentication mechanisms for WebSocket
                connections and implements message validation to ensure data integrity and security.
            </description>
        </file>
        <file>
            <description>                
                Handles application state monitoring and project progress tracking.
                from typing import Dict, Any
                from app.models import Project
                Classes:
                - StateMonitoringService:
                Methods:
                - get_current_state(self, project_id: int) -&gt; Dict[str, Any]
                - update_state(self, project_id: int, new_state: Dict[str, Any]) -&gt; bool
                - track_progress(self, project_id: int) -&gt; float
            </description>
            <name>app/services/state_monitoring_service.py</name>
        </file>
        <file>
            <description>                
                Handles code generation tasks.
                Classes:
                - CodeGenerationService:
                Methods:
                - generate_code(self, specifications: Dict[str, Any]) -&gt; List[Tuple[str,
                str]]
                - refactor_code(self, code: str, refactor_instructions: str) -&gt; str
            </description>
            <name>app/services/code_generation_service.py</name>
        </file>
        <file>
            <description>                
                Handles code migration between different programming languages.
                
                from typing import Dict, Any
                from app.utils.api_utils import AsyncAnthropic
                import os
                Classes:
                - CodeMigrationService:
                Methods:
                - migrate_code(self, code: str, source_language: str, target_language: str) -&gt;
                str
                - analyze_migration_feasibility(self, code: str, source_language: str,
                target_language: str) -&gt; Dict[str, Any]
            </description>
            <name>app/services/code_migration_service.py</name>
        </file>
        <file>
            <description>                
                Handles code optimization tasks.
                from typing import Dict, Any, List
                from app.utils.api_utils import AsyncAnthropic
                import os
                Classes:
                - CodeOptimizationService:
                Methods:
                - optimize_code(self, code: str, language: str) -&gt; str
                - profile_code(self, code: str, language: str) -&gt; Dict[str, Any]
                - suggest_optimizations(self, profiling_result: Dict[str, Any]) -&gt; List[str]
            </description>
            <name>app/services/code_optimization_service.py</name>
        </file>
        <file>
            <description>                
                Handles code quality checks and improvements.
                from typing import Dict, Any, List
                from app.utils.code_analyzer import CodeAnalyzer
                Classes:
                - CodeQualityService:
                Methods:
                - analyze_code_quality(self, code: str, language: str) -&gt; Dict[str, Any]
                - suggest_improvements(self, analysis_result: Dict[str, Any]) -&gt; List[str]
                - apply_improvements(self, code: str, improvements: List[str]) -&gt; str
            </description>
            <name>app/services/code_quality_service.py</name>
        </file>
        <file>
            <description>                
                Handles code review processes.
                from typing import Dict, Any, List
                from app.utils.api_utils import AsyncAnthropic
                import os
                Classes:
                - CodeReviewService:
                Methods:
                - review_code(self, code: str, language: str) -&gt; List[Dict[str, Any]]
                - apply_suggestion(self, code: str, suggestion: Dict[str, Any]) -&gt; str
            </description>
            <name>app/services/code_review_service.py</name>
        </file>
        <file>
            <description>                
                Handles collaboration features for team projects.
                from typing import Dict, Any, List
                from app.models import User, Project, Task
                Classes:
                - CollaborationService:
                Methods:
                - invite_user(self, project_id: int, user_email: str) -&gt; bool
                - assign_task(self, task_id: int, user_id: int) -&gt; bool
                - get_project_activity(self, project_id: int) -&gt; List[Dict[str, Any]]
            </description>
            <name>app/services/collaboration_service.py</name>
        </file>
        <file>
            <description>                
                Handles continuous integration tasks.
                from typing import Dict, Any, List
                Classes:
                - ContinuousIntegrationService:
                Methods:
                - run_ci_pipeline(self, project_id: int) -&gt; Dict[str, Any]
                - analyze_ci_results(self, ci_results: Dict[str, Any]) -&gt; List[str]
            </description>
            <name>app/services/continuous_integration_service.py</name>
        </file>
        <file>
            <description>                
                Handles data persistence operations.
                from typing import Dict, Any
                from app.models import Project
                Classes:
                - DataPersistenceService:
                Methods:
                - save_project_state(self, project_id: int, state: Dict[str, Any]) -&gt; bool
                - load_project_state(self, project_id: int) -&gt; Dict[str, Any]
                - backup_project(self, project_id: int) -&gt; str
            </description>
            <name>app/services/data_persistence_service.py</name>
        </file>
        <file>
            <description>                
                Handles data preprocessing for AI models.
                from typing import List
                Classes:
                - DataPreprocessingService:
                Methods:
                - clean_text(self, text: str) -&gt; str
                - tokenize(self, text: str) -&gt; List[str]
                - encode_data(self, data: List[str]) -&gt; List[List[int]]
            </description>
            <name>app/services/data_preprocessing_service.py</name>
        </file>
        <file>
            <description>                
                Handles dependency management tasks.
                from typing import Dict, List
                Classes:
                - DependencyManagementService:
                Methods:
                - analyze_dependencies(self, project_path: str) -&gt; Dict[str, str]
                - update_dependencies(self, project_path: str) -&gt; Dict[str, str]
                - resolve_conflicts(self, project_path: str, conflicts: List[str]) -&gt; bool
            </description>
            <name>app/services/dependency_management_service.py</name>
        </file>
        <file>
            <description>                
                Handles deployment tasks.
                from typing import Dict, Any
                Classes:
                - DeploymentService:
                Methods:
                - deploy_to_environment(self, project_path: str, environment: str) -&gt; bool
                - rollback_deployment(self, project_path: str, environment: str, version: str) -&gt;
                bool
            </description>
            <name>app/services/deployment_service.py</name>
        </file>
        <file>
            <description>                
                Handles documentation generation tasks.
                from typing import List
                Classes:
                - DocumentationService:
                Methods:
                - generate_documentation(self, project_path: str) -&gt; str
                - update_readme(self, project_path: str, changes: List[str]) -&gt; bool
            </description>
            <name>app/services/documentation_service.py</name>
        </file>
        <file>
            <description>                
                Handles error detection and fixing.
                from typing import List
                from app.utils.api_utils import AsyncAnthropic
                import os
                Classes:
                - ErrorFixingService:
                Methods:
                - analyze_and_fix_errors(self, code: str, error_message: str) -&gt; str
                - suggest_fixes(self, code: str, error_type: str) -&gt; List[str]
            </description>
            <name>app/services/error_fixing_service.py</name>
        </file>
        <file>
            <description>                
                Handles fine-tuning and training of AI models.
                
                from typing import List, Dict
                from app.utils.api_utils import AsyncAnthropic
                import os
                Classes:
                - AITrainingService:
                Methods:
                - prepare_training_data(self, data: List[Dict[str, str]]) -&gt; List[Dict[str,
                str]]
                - fine_tune_model(self, model_name: str, training_data: List[Dict[str, str]]) -&gt;
                str
                - evaluate_model_performance(self, model_name: str, test_data: List[Dict[str, str]])
                -&gt; Dict[str, float]
            </description>
            <name>app/services/ai_training_service.py</name>
        </file>
        <file>
            <description>                
                Handles interactions with AI models.
                from app.utils.api_utils import AsyncAnthropic
                Classes:
                - AIModelService:
                Methods:
                - load_model(self, model_name: str) -&gt; Any
                - generate_response(self, prompt: str, model: Any) -&gt; str
                - fine_tune_model(self, model: Any, training_data: List[Dict[str, str]]) -&gt; Any
            </description>
            <name>app/services/ai_model_service.py</name>
        </file>
        <file>
            <description>                
                Handles natural language processing tasks.
                from typing import List, Dict
                from app.utils.api_utils import AsyncAnthropic
                import os
                Classes:
                - NLPService:
                Methods:
                - extract_keywords(self, text: str) -&gt; List[str]
                - sentiment_analysis(self, text: str) -&gt; Dict[str, float]
                - summarize_text(self, text: str, max_length: int) -&gt; str
            </description>
            <name>app/services/natural_language_processing.py</name>
        </file>
        <file>
            <description>                
                Handles performance monitoring and optimization tasks.
                from typing import Dict, Any, List
                Classes:
                - PerformanceMonitoringService:
                Methods:
                - analyze_performance(self, project_path: str) -&gt; Dict[str, Any]
                - suggest_optimizations(self, performance_data: Dict[str, Any]) -&gt; List[str]
            </description>
            <name>app/services/performance_monitoring_service.py</name>
        </file>
        <file>
            <description>                
                Handles project export and import functionality.
                from typing import Dict, Any
                import json
                from app.models import Project
                Classes:
                - ProjectExportService:
                Methods:
                - export_project(self, project_id: int) -&gt; bytes
                - import_project(self, project_data: bytes) -&gt; int
            </description>
            <name>app/services/project_export_service.py</name>
        </file>
        <file>
            <description>                
                Handles test generation tasks.
                from app.utils.api_utils import AsyncAnthropic
                import os
                Classes:
                - TestGenerationService:
                Methods:
                - generate_unit_tests(self, code: str, function_name: str) -&gt; str
                - generate_integration_tests(self, project_structure: Dict[str, Any]) -&gt; str
            </description>
            <name>app/services/test_generation_service.py</name>
        </file>
        <file>
            <description>                
                Handles user feedback processing and incorporation.
                from typing import Dict, Any
                from app.utils.api_utils import AsyncAnthropic
                import os
                Classes:
                - FeedbackService:
                Methods:
                - process_feedback(self, feedback: str, project_id: int) -&gt; Dict[str, Any]
                - incorporate_feedback(self, processed_feedback: Dict[str, Any], project_id: int)
                -&gt; bool
            </description>
            <name>app/services/feedback_service.py</name>
        </file>
        <file>
            <description>                
                Handles user-related operations.
                from typing import List
                from app.models import User, Project
                Classes:
                - UserManagementService:
                Methods:
                - create_user(self, username: str, email: str, password: str) -&gt; User
                - update_user(self, user_id: int, **kwargs) -&gt; User
                - delete_user(self, user_id: int) -&gt; bool
                - get_user_projects(self, user_id: int) -&gt; List[Project]
            </description>
            <name>app/services/user_management_service.py</name>
        </file>
        <file>
            <description>                
                Handles version control operations.
                from typing import Dict, Any
                import git
                Classes:
                - VersionControlService:
                Methods:
                - init_repository(self, project_path: str) -&gt; bool
                - commit_changes(self, project_path: str, commit_message: str) -&gt; bool
                - create_branch(self, project_path: str, branch_name: str) -&gt; bool
            </description>
            <name>app/services/version_control_service.py</name>
        </file>
        <file>
            <description>                
                Home page template for the web UI.
                Contents:
                - Extends layout.html
                - Contains the root element for the application
                - Includes any server-side rendered content
            </description>
            <name>app/templates/index.html</name>
        </file>
        <file>
            <name>app/services/ai_service.py</name>
            <description>                
                Provides AI-related services without direct database interactions.
                from typing import Dict, Any, List
                from app.utils.api_utils import AsyncAnthropic
                import os
                Classes:
                - AIService:
                Methods:
                - generate_text(self, prompt: str, max_tokens: int) -&gt; str: Generates text based on
                a prompt
                - analyze_code(self, code: str) -&gt; Dict[str, Any]: Analyzes code and returns
                insights
                - generate_unit_tests(self, code: str) -&gt; List[str]: Generates unit tests for given
                code
                - optimize_code(self, code: str) -&gt; str: Suggests optimizations for given code
                
                This refactored file removes direct database interactions, focusing solely on
                AI-related functionalities. Database operations are now handled by separate data
                access objects or services, improving separation of concerns and maintainability.
            </description>
        </file>
        <file>
            <description>                
                Implements API rate limiting functionality.
                Classes:
                - APIRateLimiter:
                Methods:
                - limit(self, func: Callable) -&gt; Callable
            </description>
            <name>app/utils/api_rate_limiter.py</name>
        </file>
        <file>
            <description>                
                Implements authentication-related functionality.
                from flask import Blueprint, render_template, redirect, url_for, flash, request
                from flask_login import login_user, logout_user, login_required
                from app.models import User
                from app import db
                from werkzeug.security import generate_password_hash, check_password_hash
                Contents:
                - Login and logout routes
                - User registration
                - Password reset functionality
            </description>
            <name>app/auth/__init__.py</name>
        </file>
        <file>
            <description>                
                Implements caching mechanisms for improved performance.
                from typing import Any
                Classes:
                - CachingService:
                Methods:
                - get(self, key: str) -&gt; Any
                - set(self, key: str, value: Any, expiration: int) -&gt; None
                - delete(self, key: str) -&gt; None
            </description>
            <name>app/services/caching_service.py</name>
        </file>
        <file>
            <description>                
                Implements centralized logging for the application.
                import logging
                Classes:
                - LoggingService:
                Methods:
                - log_info(self, message: str) -&gt; None
                - log_error(self, message: str, exception: Exception) -&gt; None
                - log_debug(self, message: str) -&gt; None
            </description>
            <name>app/services/logging_service.py</name>
        </file>
        <file>
            <description>                
                Implements code difference analysis functionality.
                Classes:
                - CodeDiff:
                Methods:
                - generate_diff(self, old_code: str, new_code: str) -&gt; str
                - apply_patch(self, original_code: str, patch: str) -&gt; str
            </description>
            <name>app/utils/code_diff.py</name>
        </file>
        <file>
            <description>                
                Implements code linting functionality.
                import pylint.lint
                from pylint.reporters.text import TextReporter
                Classes:
                - CodeLinter:
                Methods:
                - lint_code(self, code: str, language: str) -&gt; List[Dict[str, Any]]
                - apply_auto_fixes(self, code: str, lint_results: List[Dict[str, Any]]) -&gt; str
            </description>
            <name>app/utils/code_linter.py</name>
        </file>
        <file>
            <description>                
                Implements code obfuscation functionality for security purposes.
                
                import ast
                import random
                import string
                Classes:
                - CodeObfuscator:
                Methods:
                - obfuscate_code(self, code: str, language: str) -&gt; str
                - deobfuscate_code(self, obfuscated_code: str, language: str) -&gt; str
            </description>
            <name>app/utils/code_obfuscator.py</name>
        </file>
        <file>
            <description>                
                Implements code parsing functionality.
                import ast
                Classes:
                - CodeParser:
                Methods:
                - parse_code(self, code: str, language: str) -&gt; Dict[str, Any]
            </description>
            <name>app/utils/code_parser.py</name>
        </file>
        <file>
            <description>                
                Implements code quality metrics calculation.
                
                import radon.metrics
                from radon.visitors import ComplexityVisitor
                Classes:
                - CodeMetrics:
                Methods:
                - calculate_metrics(self, code: str, language: str) -&gt; Dict[str, Any]
            </description>
            <name>app/utils/code_metrics.py</name>
        </file>
        <file>
            <description>                
                Implements code translation between programming languages.
                Classes:
                - LanguageTranslator:
                Methods:
                - translate_code(self, code: str, from_language: str, to_language: str) -&gt;
                str
                - detect_language(self, code: str) -&gt; str
            </description>
            <name>app/utils/language_translator.py</name>
        </file>
        <file>
            <description>                
                Implements custom Flask CLI commands.
                import click
                from flask.cli import with_appcontext
                from app import db
                from app.models import User, Project, Task
                Contents:
                - Database initialization command
                - Test data population command
                - Other utility commands
            </description>
            <name>app/cli.py</name>
        </file>
        <file>
            <description>                
                Implements dependency graph functionality.
                
                import networkx as nx
                Classes:
                - DependencyGraph:
                Methods:
                - generate_graph(self, project_id: int) -&gt; networkx.Graph
            </description>
            <name>app/utils/dependency_graph.py</name>
        </file>
        <file>
            <description>                
                Implements security scanning functionality.
                
                import bandit
                from bandit.core import manager
                Classes:
                - SecurityScanner:
                Methods:
                - scan_code(self, code: str, language: str) -&gt; List[Dict[str, Any]]
            </description>
            <name>app/utils/security_scanner.py</name>
        </file>
        <file>
            <description>                
                Implements system thinking processes for AI decision-making.
                from typing import List
                from app.utils.api_utils import AsyncAnthropic
                import os
                Classes:
                - SystemThinkingService:
                Methods:
                - system_1_thinking(self, context: str) -&gt; str
                - system_2_thinking(self, context: str, options: List[str]) -&gt; str
                - system_3_thinking(self, context: str, options: List[str], constraints: List[str])
                -&gt; str
            </description>
            <name>app/services/system_thinking_service.py</name>
        </file>
        <file>
            <description>                
                Implements test coverage analysis functionality.
                
                import coverage
                Classes:
                - TestCoverageAnalyzer:
                Methods:
                - analyze_coverage(self, project_id: int) -&gt; Dict[str, Any]
            </description>
            <name>app/utils/test_coverage_analyzer.py</name>
        </file>
        <file>
            <description>                
                Implements web browsing functionality for research.
                from typing import List, Dict
                import requests
                from bs4 import BeautifulSoup
                from app.utils.api_utils import AsyncAnthropic
                import os
                Classes:
                - WebBrowsingService:
                Methods:
                - search(self, query: str) -&gt; List[Dict[str, str]]
                - extract_content(self, url: str) -&gt; str
                - summarize(self, content: str) -&gt; str
            </description>
            <name>app/services/web_browsing_service.py</name>
        </file>
        <file>
            <name>app/errors/__init__.py</name>
            <description>                
                Initializes the Flask application with lazy imports and distributed
                initialization logic.
                Imports: flask, flask_sqlalchemy, flask_migrate, flask_login, flask_socketio
                Functions:
                - create_app(config_class=Config) -&gt; Flask: Creates and configures the Flask
                application
                - init_extensions(app: Flask) -&gt; None: Initializes Flask extensions
                - register_blueprints(app: Flask) -&gt; None: Registers application blueprints
                - configure_logging(app: Flask) -&gt; None: Sets up application logging
                
                This file now uses lazy loading techniques to improve startup time and reduce memory
                usage. The initialization logic is distributed across multiple functions for better
                organization and maintainability.
            </description>
        </file>
        <file>
            <description>                
                Initializes the models for the application.
                
                from flask_sqlalchemy import SQLAlchemy
                from flask_login import UserMixin
                from werkzeug.security import generate_password_hash, check_password_hash
                from app import db
                Classes:
                - User(db.Model, UserMixin):
                Attributes: id, username, email, password_hash
                Methods:
                - set_password(self, password: str) -&gt; None
                - check_password(self, password: str) -&gt; bool
                - to_dict(self) -&gt; Dict[str, Any]
                - Project(db.Model):
                Attributes: id, name, description, user_id
                Methods:
                - to_dict(self) -&gt; Dict[str, Any]
                - Task(db.Model):
                Attributes: id, title, description, status, project_id
                Methods:
                - to_dict(self) -&gt; Dict[str, Any]
                - File(db.Model):
                Attributes: id, name, content, project_id
                Methods:
                - to_dict(self) -&gt; Dict[str, Any]
            </description>
            <name>app/models/__init__.py</name>
        </file>
        <file>
            <description>                
                Initializes the services for the application.
                Imports: anthropic, app.utils.api_utils
                Classes:
                - AIService:
                Methods:
                - generate_text(self, prompt: str, max_tokens: int) -&gt; str
                - analyze_code(self, code: str) -&gt; Dict[str, Any]
                - ProjectManager:
                Methods:
                - create_project(self, name: str, description: str, user_id: int) -&gt; Project
                - update_project(self, project_id: int, **kwargs) -&gt; Project
                - TaskManager:
                Methods:
                - create_task(self, title: str, description: str, project_id: int) -&gt; Task
                - update_task(self, task_id: int, **kwargs) -&gt; Task
                - FileManager:
                Methods:
                - create_file(self, name: str, content: str, project_id: int) -&gt; File
                - update_file(self, file_id: int, content: str) -&gt; File
            </description>
            <name>app/services/__init__.py</name>
        </file>
        <file>
            <description>JavaScript file for project-specific functionality</description>
            <name>app/static/js/project.js</name>
        </file>
        <file>
            <description>JavaScript file for task-specific functionality</description>
            <name>app/static/js/task.js</name>
        </file>
        <file>
            <description>JavaScript file for user profile functionality</description>
            <name>app/static/js/user_profile.js</name>
        </file>
        <file>
            <name>app/static/js/error_handling.js</name>
            <description>                
                Provides enhanced error handling and user feedback mechanisms for the
                frontend.
                Functions:
                - handleError(error: Error) -&gt; void: Handles and logs JavaScript errors
                - displayErrorToUser(message: string) -&gt; void: Displays user-friendly error messages
                - reportErrorToServer(error: Error) -&gt; void: Reports errors to the server for
                logging
                
                This updated file improves error handling on the frontend, providing better user
                feedback and error reporting capabilities.
            </description>
        </file>
        <file>
            <description>                
                JavaScript for generating charts and graphs.
                Contents:
                - Functions to create various types of charts (line, bar, pie, etc.)
                - Data processing for chart inputs
                - Chart update and animation functions
            </description>
            <name>app/static/js/charts.js</name>
        </file>
        <file>
            <description>                
                JavaScript for the AI chat functionality.
                Contents:
                - WebSocket connection for real-time chat
                - Functions to send and receive messages
                - UI updates for chat interface
            </description>
            <name>app/static/js/ai_chat.js</name>
        </file>
        <file>
            <description>                
                JavaScript for the code editor functionality.
                Contents:
                - Code editor initialization
                - Syntax highlighting
                - Auto-completion features
            </description>
            <name>app/static/js/code_editor.js</name>
        </file>
        <file>
            <description>Logo image file for the application.</description>
            <name>app/static/img/logo.svg</name>
        </file>
        <file>
            <description>                
                Main CSS file for styling the frontend.
                Contents:
                - Global styles
                - Component-specific styles
                - Responsive design rules
            </description>
            <name>app/static/css/style.css</name>
        </file>
        <file>
            <description>                
                Main JavaScript file for the frontend.
                Contents:
                - Flask components for the UI
                - WebSocket connection setup
                - API calls to the backend
                - State management
            </description>
            <name>app/static/js/main.js</name>
        </file>
        <file>
            <name>app/services/ai_model_manager.py</name>
            <description>                
                Manages AI models with versioning and rollback capabilities.
                Classes:
                - AIModelManager:
                Methods:
                - load_model(self, model_name: str, version: str = 'latest') -&gt; Any: Loads a
                specific version of an AI model
                - update_model(self, model_name: str, new_version: str) -&gt; bool: Updates a model to
                a new version
                - rollback_model(self, model_name: str, target_version: str) -&gt; bool: Rolls back a
                model to a previous version
                - list_model_versions(self, model_name: str) -&gt; List[str]: Lists all available
                versions of a model
                - get_model_metadata(self, model_name: str, version: str) -&gt; Dict[str, Any]:
                Retrieves metadata for a specific model version
                
                This updated file includes versioning support for AI models, allowing for better
                management and the ability to rollback to previous versions if needed.
            </description>
        </file>
        <file>
            <description>                
                Manages different AI models used in the application.
                from typing import Any, List
                Classes:
                - AIModelRegistry:
                Methods:
                - register_model(self, model_name: str, model_path: str) -&gt; bool
                - get_model(self, model_name: str) -&gt; Any
                - list_models(self) -&gt; List[str]
            </description>
            <name>app/services/ai_model_registry.py</name>
        </file>
        <file>
            <description>                
                Manages integrations with external APIs.
                Classes:
                - APIIntegrationService:
                Methods:
                - add_api_integration(self, project_id: int, api_name: str, api_key: str) -&gt;
                bool
                - remove_api_integration(self, project_id: int, api_name: str) -&gt; bool
                - list_project_integrations(self, project_id: int) -&gt; List[Dict[str, str]]
            </description>
            <name>app/services/api_integration_service.py</name>
        </file>
        <file>
            <description>                
                Manages user notifications and alerts.
                from typing import List, Dict, Any
                from app.models import User
                Classes:
                - NotificationService:
                Methods:
                - send_notification(self, user_id: int, message: str) -&gt; bool
                - get_user_notifications(self, user_id: int) -&gt; List[Dict[str, Any]]
            </description>
            <name>app/services/notification_service.py</name>
        </file>
        <file>
            <description>NPM package configuration for frontend dependencies</description>
            <name>package.json</name>
        </file>
        <file>
            <description>                
                Plain text email template for password reset.
                Contents:
                - Text version of password reset email
                - Reset link placeholder
            </description>
            <name>app/templates/email/reset_password.txt</name>
        </file>
        <file>
            <description>                
                Contains unit tests for various service classes.
                import pytest
                from app.services import (
                AIService, ProjectManager, TaskManager, FileManager,
                WebBrowsingService, StateMonitoringService
                )
            </description>
            <name>tests/test_services.py</name>
        </file>
        <file>
            <description>                
                Contains unit tests for various utility classes.
                
                import pytest
                from app.utils import (
                CodeAnalyzer, CodeComplexityAnalyzer, CodeDiff,
                CodeFormatter, CodeGenerator, CodeLinter
                )
            </description>
            <name>tests/test_utils.py</name>
        </file>
        <file>
            <description>                
                Processes natural language requirements and converts them into structured
                project tasks.
                from typing import List, Dict, Any
                from app.utils.api_utils import AsyncAnthropic
                import os
                Classes:
                - NaturalLanguageRequirementsService:
                Methods:
                - process_requirements(self, requirements_text: str) -&gt; List[Dict[str, Any]]
                - generate_user_stories(self, requirements_text: str) -&gt; List[str]
            </description>
            <name>app/services/natural_language_requirements_service.py</name>
        </file>
        <file>
            <description>                
                Project documentation and setup instructions.
                Contents:
                - Project overview
                - Installation instructions
                - Usage guide
                - Contributing guidelines
            </description>
            <name>README.md</name>
        </file>
        <file>
            <description>                
                Provides AI-generated explanations for code and concepts.
                from app.utils.api_utils import AsyncAnthropic
                Classes:
                - AIExplanationService:
                Methods:
                - explain_code(self, code: str, language: str) -&gt; str
                - explain_concept(self, concept: str, context: str) -&gt; str
                - generate_code_comments(self, code: str, language: str) -&gt; str
            </description>
            <name>app/services/ai_explanation_service.py</name>
        </file>
        <file>
            <description>                
                Provides analytics and insights for projects.
                from typing import Dict, Any
                from datetime import datetime
                Classes:
                - ProjectAnalyticsService:
                Methods:
                - calculate_project_metrics(self, project_id: int) -&gt; Dict[str, Any]
                - generate_project_report(self, project_id: int) -&gt; str
                - predict_project_completion(self, project_id: int) -&gt; datetime
            </description>
            <name>app/services/project_analytics_service.py</name>
        </file>
        <file>
            <description>                
                Provides code analysis utilities.
                
                import ast
                import radon.metrics
                from radon.visitors import ComplexityVisitor
                Classes:
                - CodeAnalyzer:
                Methods:
                - analyze_complexity(self, code: str) -&gt; Dict[str, Any]
                - detect_code_smells(self, code: str) -&gt; List[Dict[str, Any]]
                - suggest_improvements(self, analysis_result: Dict[str, Any]) -&gt; List[str]
            </description>
            <name>app/utils/code_analyzer.py</name>
        </file>
        <file>
            <description>                
                Provides data validation utilities.
                
                import re
                from marshmallow import Schema, fields, validate
                Classes:
                - DataValidator:
                Methods:
                - validate_user_input(self, data: Dict[str, Any], schema: Dict[str, Any]) -&gt;
                Tuple[bool, List[str]]
                - sanitize_input(self, input_string: str) -&gt; str
            </description>
            <name>app/utils/data_validator.py</name>
        </file>
        <file>
            <description>                
                Provides encryption and decryption utilities for sensitive data.
                from cryptography.fernet import Fernet
                Classes:
                - EncryptionService:
                Methods:
                - encrypt(self, data: str) -&gt; str
                - decrypt(self, encrypted_data: str) -&gt; str
            </description>
            <name>app/utils/encryption_service.py</name>
        </file>
        <file>
            <description>                
                Provides explanations for complex code snippets.
                from app.utils.api_utils import AsyncAnthropic
                import os
                Classes:
                - CodeExplanationService:
                Methods:
                - explain_code(self, code: str, language: str) -&gt; str
                - generate_code_summary(self, code: str, language: str) -&gt; str
            </description>
            <name>app/services/code_explanation_service.py</name>
        </file>
        <file>
            <description>                
                Provides project estimation features based on project requirements and
                historical data.
                from typing import List, Dict, Any
                from app.utils.api_utils import AsyncAnthropic
                import os
                Classes:
                - ProjectEstimationService:
                Methods:
                - estimate_project_duration(self, project_requirements: List[Dict[str, Any]]) -&gt;
                int
                - estimate_project_cost(self, project_requirements: List[Dict[str, Any]]) -&gt;
                float
                - analyze_risk_factors(self, project_requirements: List[Dict[str, Any]]) -&gt;
                List[Dict[str, Any]]
            </description>
            <name>app/services/project_estimation_service.py</name>
        </file>
        <file>
            <description>                
                Reusable component for AI chat interface.
                Contents:
                - HTML structure for AI chat interface
                - Placeholders for chat messages and input
            </description>
            <name>app/templates/components/ai_chat.html</name>
        </file>
        <file>
            <description>                
                Reusable component for displaying a list of tasks.
                Contents:
                - HTML structure for task list
                - Placeholders for task details and actions
            </description>
            <name>app/templates/components/task_list.html</name>
        </file>
        <file>
            <description>                
                Reusable component for displaying project dashboard.
                Contents:
                - HTML structure for project overview
                - Task summary and progress indicators
                - Recent activity feed
            </description>
            <name>app/templates/components/project_dashboard.html</name>
        </file>
        <file>
            <description>                
                Reusable component for displaying project information.
                Contents:
                - HTML structure for project card
                - Placeholders for project details and actions
            </description>
            <name>app/templates/components/project_card.html</name>
        </file>
        <file>
            <description>                
                Reusable component for in-browser code editing.
                Contents:
                - HTML structure for code editor
                - Integration with a JavaScript-based code editor library
            </description>
            <name>app/templates/components/code_editor.html</name>
        </file>
        <file>
            <description>                
                Reusable component for selecting AI models.
                Contents:
                - HTML structure for model selection dropdown
                - JavaScript for dynamic model loading
            </description>
            <name>app/templates/components/ai_model_selector.html</name>
        </file>
        <file>
            <description>                
                Reusable footer component.
                Contents:
                - HTML structure for the footer
                - Copyright information, links, etc.
            </description>
            <name>app/templates/components/footer.html</name>
        </file>
        <file>
            <description>                
                Reusable navigation bar component.
                Contents:
                - HTML structure for the navigation bar
                - Links to main sections of the application
            </description>
            <name>app/templates/components/navbar.html</name>
        </file>
        <file>
            <description>                
                Script to initialize the database with default data.
                Contents:
                - Database connection setup
                - Default data insertion queries
                - Error handling and logging
            </description>
            <name>scripts/db_init.py</name>
        </file>
        <file>
            <description>                
                Shell script for setting up the development environment.
                Contents:
                - Virtual environment creation
                - Dependency installation
                - Initial database setup
            </description>
            <name>scripts/setup.sh</name>
        </file>
        <file>
            <description>                
                Shell script to run all tests for the application.
                Contents:
                - Commands to set up test environment
                - Execution of unit and integration tests
                - Test result reporting
            </description>
            <name>scripts/run_tests.sh</name>
        </file>
        <file>
            <description>                
                Stores and manages templates for AI prompts.
                Classes:
                - AIPromptTemplates:
                Methods:
                - get_code_generation_prompt(self, task_description: str) -&gt; str
                - get_code_review_prompt(self, code: str) -&gt; str
                - get_error_fixing_prompt(self, error_message: str, code_snippet: str) -&gt; str
            </description>
            <name>app/utils/ai_prompt_templates.py</name>
        </file>
        <file>
            <description>                
                Stores templates for AI prompts used across the application.
                Classes:
                - AIPromptTemplates:
                Methods:
                - get_code_generation_prompt(self, task_description: str) -&gt; str
                - get_code_review_prompt(self, code: str) -&gt; str
                - get_error_fixing_prompt(self, error_message: str, code_snippet: str) -&gt; str
            </description>
            <name>app/utils/ai_prompt_templates.py</name>
        </file>
        <file>
            <description>                
                Template for 403 Forbidden error page.
                Contents:
                - Custom 403 error message and layout
            </description>
            <name>app/templates/errors/403.html</name>
        </file>
        <file>
            <description>                
                Template for 404 Not Found error page.
                Contents:
                - Custom 404 error message and layout
            </description>
            <name>app/templates/errors/404.html</name>
        </file>
        <file>
            <description>                
                Template for 500 Internal Server Error page.
                Contents:
                - Custom 500 error message and layout
            </description>
            <name>app/templates/errors/500.html</name>
        </file>
        <file>
            <description>Template for displaying and managing individual projects</description>
            <name>app/templates/project.html</name>
        </file>
        <file>
            <description>Template for displaying and managing individual tasks</description>
            <name>app/templates/task.html</name>
        </file>
        <file>
            <description>Template for user login page</description>
            <name>app/templates/login.html</name>
        </file>
        <file>
            <description>Template for user profile page</description>
            <name>app/templates/user_profile.html</name>
        </file>
        <file>
            <description>Template for user registration page</description>
            <name>app/templates/register.html</name>
        </file>
        <file>
            <description>                
                Utility for generating code snippets and boilerplate.
                import jinja2
                Classes:
                - CodeGenerator:
                Methods:
                - generate_class_template(self, class_name: str, attributes: List[str], methods:
                List[str]) -&gt; str
                - generate_function_template(self, func_name: str, params: List[str], return_type:
                str) -&gt; str
            </description>
            <name>app/utils/code_generator.py</name>
        </file>
        <file>
            <description>                
                Utility functions for API interactions.
                
                import time
                import asyncio
                from collections import deque
                from anthropic import AsyncAnthropic, RateLimitError, APIError
                Functions:
                - rate_limited_request(func: Callable, *args, **kwargs) -&gt; Any:
                Decorator for rate-limiting API requests
                Classes:
                - APIRateLimiter:
                Methods:
                - __init__(self, rate_limit: int, time_window: int)
                - wait(self) -&gt; None
            </description>
            <name>app/utils/api_utils.py</name>
        </file>
        <file>
            <description>                
                Utility functions for the frontend.
                Contents:
                - Helper functions for common tasks
                - Date formatting
                - Input validation
            </description>
            <name>app/static/js/utils.js</name>
        </file>
        <file>
            <name>webpack.config.js</name>
            <description>Webpack configuration for bundling frontend assets</description>
        </file>
        <file>
            <description>                
                Webpack configuration for bundling frontend assets
                
                from flask import Flask
                from flask_sqlalchemy import SQLAlchemy
                from flask_migrate import Migrate
                from flask_login import LoginManager
                from flask_socketio import SocketIO
                from config import Config
            </description>
            <name>app/__init__.py</name>
        </file>
    </files>
    <logicsteps>        
        1. Initialize the application environment and load the configuration.
        2. Set up the Flask application with all necessary extensions.
        3. Initialize the database and create tables if they don't exist.
        4. Start the WebSocket server for real-time communications.
        5. Load the initial application plan or create a new one if not exists.
        6. Use AI to generate a detailed project plan based on user input or existing plan.
        7. Generate initial code files according to the project plan.
        8. Create and run unit tests to ensure functionality.
        9. Detect and fix errors in the generated code using AI assistance.
        10. Run tests again and validate fixes.
        11. Start the web server and render the frontend.
        12. Handle user interactions through the web interface.
        13. Manage tasks and update the to-do list with AI completions.
        14. Implement the web browsing agent for research when requested.
        15. Continuously monitor the state of the application and track project progress.
        16. Gather user feedback and update the application accordingly.
        17. Repeat the feedback loop for continuous improvement.
        18. Manage file operations including reading, writing, and backups.
        19. Handle API rate limiting to ensure compliance with request quotas.
        20. Provide real-time updates to users through WebSocket connections.
        21. Implement system 1, 2, and 3 thinking for AI decision-making processes.
        22. Regularly update the project state and persist changes to the database.
        23. Handle user authentication and authorization for secure access.
        24. Provide mechanisms for exporting and importing projects.
        25. Offer documentation and help features within the application.
        26. Integrate version control operations for code management.
        27. Analyze and manage project dependencies.
        28. Facilitate code review processes with AI assistance.
        29. Automate deployment to various environments.
        30. Generate and update project documentation.
        31. Monitor application performance and suggest optimizations.
        32. Conduct security scans on generated code.
        33. Calculate and report code quality metrics.
        34. Analyze test coverage and suggest improvements.
        35. Parse and analyze code structure for various programming languages.
        36. Implement and maintain a feature flagging system for gradual rollout and A/B testing.
        37. Regularly collect and analyze user feedback to inform development priorities.
        38. Conduct sprint planning and review meetings to adapt to changing requirements.
        39. Continuously monitor system performance and user behavior to identify areas for improvement.
        40. Regularly update and reprioritize the product backlog based on new insights and feedback.
    </logicsteps>
    <mechanics>        
        - AI-assisted project planning and structuring
        - Automated code generation and modification
        - Error detection and automatic fixing
        - User feedback loop for continuous improvement
        - Unit testing and test-driven development
        - Comprehensive file management and backup
        - API rate limiting to manage request quotas
        - Interactive web UI for task management and user interaction
        - Web browsing agent for research
        - Editable to-do list with AI completions
        - State monitoring for tracking project progress
        - System 1, 2, and 3 thinking implementation for AI decision-making
        - Version control integration
        - Dependency management
        - Code review process
        - Automated deployment
        - Documentation generation
        - Performance monitoring and optimization
        - Feature flagging system for controlled feature rollout
        - User feedback collection and analysis
        - Agile sprint planning and backlog management
        - Continuous performance monitoring and analytics
        - A/B testing capabilities for data-driven decision making
    </mechanics>
    <overview>        
        The AI Software Factory is an advanced, Flask-based web application that leverages AI
        to assist in the entire software development lifecycle. It includes project planning, code
        generation, error fixing, testing, and continuous improvement based on user feedback. The
        system supports web browsing for research, task management with AI completions, and
        implements system 1, 2, and 3 thinking for decision-making processes. Additionally, it
        incorporates version control, dependency management, code review, deployment, documentation
        generation, and performance monitoring.
    </overview>
    <sql>        
        -- Create Users table
        CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(64) UNIQUE NOT NULL,
        email VARCHAR(120) UNIQUE NOT NULL,
        password_hash VARCHAR(128) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Create Projects table
        CREATE TABLE projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(64) NOT NULL,
        description TEXT,
        user_id INTEGER NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
        );
        
        -- Create Tasks table
        CREATE TABLE tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(128) NOT NULL,
        description TEXT,
        status VARCHAR(20) DEFAULT 'pending',
        project_id INTEGER NOT NULL,
        assigned_to INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projects (id),
        FOREIGN KEY (assigned_to) REFERENCES users (id)
        );
        
        -- Create Files table
        CREATE TABLE files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(128) NOT NULL,
        content TEXT,
        project_id INTEGER NOT NULL,
        version INTEGER DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projects (id)
        );
        
        -- Create CodeReviews table
        CREATE TABLE code_reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_id INTEGER NOT NULL,
        reviewer_id INTEGER NOT NULL,
        comments TEXT,
        status VARCHAR(20) DEFAULT 'pending',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (file_id) REFERENCES files (id),
        FOREIGN KEY (reviewer_id) REFERENCES users (id)
        );
        
        -- Create Deployments table
        CREATE TABLE deployments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        environment VARCHAR(20) NOT NULL,
        version VARCHAR(40) NOT NULL,
        status VARCHAR(20) DEFAULT 'pending',
        deployed_by INTEGER NOT NULL,
        deployed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projects (id),
        FOREIGN KEY (deployed_by) REFERENCES users (id)
        );
        
        -- Create Dependencies table
        CREATE TABLE dependencies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        name VARCHAR(64) NOT NULL,
        version VARCHAR(20) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projects (id)
        );
        
        -- Create PerformanceMetrics table
        CREATE TABLE performance_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        metric_name VARCHAR(64) NOT NULL,
        metric_value FLOAT NOT NULL,
        recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projects (id)
        );
        
        -- Create AIAssistance table
        CREATE TABLE ai_assistance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        project_id INTEGER NOT NULL,
        query TEXT NOT NULL,
        response TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (project_id) REFERENCES projects (id)
        );
        
        -- Create WebBrowsingHistory table
        CREATE TABLE web_browsing_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        project_id INTEGER NOT NULL,
        query TEXT NOT NULL,
        url VARCHAR(255) NOT NULL,
        summary TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (project_id) REFERENCES projects (id)
        );
        
        -- Create SystemThinking table
        CREATE TABLE system_thinking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        thinking_type VARCHAR(20) NOT NULL,
        context TEXT NOT NULL,
        decision TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projects (id)
        );
    </sql>
</application_plan>

Remember, the application should start with a main module in the main.py file(main shouldn't take any arguments). Always return the full contents of the file
    