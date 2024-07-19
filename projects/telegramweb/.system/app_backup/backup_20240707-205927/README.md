# Secure Messaging Platform

A professional-grade web-based messaging platform inspired by Telegram, built with Flask. This application offers secure messaging, media sharing, voice and video functionality, and advanced features like powerful search, sticker support, and end-to-end encryption.

## Features

- Secure user authentication
- Real-time messaging
- Media file sharing
- End-to-end encryption for messages
- Powerful search functionality
- Responsive web design

## Prerequisites

- Python 3.7+
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/secure-messaging-platform.git
   cd secure-messaging-platform
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Copy the `config.py.example` file to `config.py`:
   ```
   cp config.py.example config.py
   ```

2. Edit `config.py` and set your desired configuration options, including the secret key and database URI.

## Running the Application

To start the application, run:

```
python main.py
```

The application will be available at `http://localhost:5000`.

## Project Structure

- `app/`: Main application package
  - `models/`: Database models
  - `routes/`: Route definitions
  - `services/`: Business logic
  - `static/`: Static files (CSS, JavaScript)
  - `templates/`: HTML templates
  - `utils/`: Utility functions
- `config.py`: Configuration file
- `main.py`: Application entry point

## Development

To run the application in debug mode, set the `DEBUG` variable in `config.py` to `True`.

## Testing

To run the tests, execute:

```
python -m unittest discover tests
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Flask team for the excellent web framework
- Telegram for inspiration