# Project Tasker

An automated project management integration tool that breaks down software features into manageable tasks across various platforms.

## Features

- Natural Language Processing (NLP) based feature analysis
- Automated task breakdown and organization
- Multi-platform integration (GitHub, GitLab, Jira, Trello, etc.)
- RESTful API with FastAPI
- CLI tool for project management
- Docker support for easy deployment

## Quick Start

### Prerequisites

- Python 3.10 or higher
- PostgreSQL
- Redis
- Docker (optional)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/project-tasker.git
   cd project-tasker
   ```

2. Run the setup script:
   ```bash
   ./setup-dev.sh
   ```

3. Start the development server:
   ```bash
   poetry run uvicorn project_tasker.main:app --reload
   ```

4. Visit the API documentation at `http://localhost:8000/api/v1/docs`

### Docker Setup

1. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

2. The API will be available at `http://localhost:8000`

## Development

### Project Structure

```
project_tasker/
├── api/            # API endpoints and routes
├── core/           # Core functionality and configurations
├── integrations/   # Platform integration implementations
├── nlp/            # Natural Language Processing modules
└── utils/          # Utility functions and helpers
```

### Running Tests

```bash
poetry run pytest
```

### Making Changes

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and add tests

3. Run tests and linting:
   ```bash
   make test
   make lint
   ```

4. Submit a pull request

## API Documentation

The API documentation is available at `/api/v1/docs` when running the server. It includes:

- Authentication endpoints
- Project management
- Task operations
- Platform integrations
- Feature analysis

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Submit a pull request

Please make sure to update tests as appropriate and follow the existing coding style.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FastAPI for the web framework
- spaCy for NLP processing
- SQLAlchemy for database operations
- Various platform APIs for integration support
