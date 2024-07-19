# Agent Application Dev

Agent Application Dev is an AI-assisted Python application development tool. It uses AI to help create, plan, and modify Python applications based on user input and feedback.

## Features

- AI-assisted application creation and planning
- Automated code generation
- Error detection and fixing
- Iterative development based on user feedback
- Automatic backup system
- Unit test generation and execution

## Requirements

- Python 3.7+
- Anthropic API key

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/agent-application-dev.git
   cd agent-application-dev
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your Anthropic API key:
   ```
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```

## Usage

To start creating a new application:
```
python agent_application_maker.py
```

To fix issues in an existing application:
```
python agent_application_maker.py --fix
```

To provide feedback and update an existing application:
```
python agent_application_maker.py --feedback
```

To plan an application without creating files:
```
python agent_application_maker.py --plan
```

## How it works

1. The tool prompts you to describe the Python application you want to create.
2. It uses AI to plan the application structure and generate initial code.
3. The application is then run, and any errors are automatically detected.
4. If errors are found, the AI attempts to fix them.
5. You can provide feedback to further improve the application.
6. The process continues iteratively until you're satisfied with the result.

## File Structure

- `agent_application_maker.py`: The main script that orchestrates the application development process.
- `devfolder/`: The directory where the generated application files are stored.
- `.system/`: Contains system files including backups and logs.
- `projects/`: Archived versions of previous projects.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Disclaimer

This tool automatically executes code on your machine. Use it at your own risk and always review generated code before running it.