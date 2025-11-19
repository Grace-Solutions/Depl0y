# Contributing to Depl0y

Thank you for your interest in contributing to Depl0y! We welcome contributions from everyone.

## How Can I Contribute?

### Reporting Bugs

Before submitting a bug report:
- Check the [existing issues](https://github.com/yourusername/depl0y/issues) to avoid duplicates
- Gather information about the bug
- Try to reproduce it with the latest version

When submitting a bug report, include:
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Environment details (OS, Docker version, etc.)
- Relevant logs

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:
- Use a clear, descriptive title
- Provide detailed description of the proposed feature
- Explain why this enhancement would be useful
- List any alternative solutions you've considered

### Pull Requests

1. **Fork the repository**
2. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/my-feature
   ```
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with clear messages**:
   ```bash
   git commit -m "Add feature: description"
   ```
6. **Push to your fork**:
   ```bash
   git push origin feature/my-feature
   ```
7. **Open a Pull Request**

## Development Setup

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Database

```bash
docker-compose up -d db
```

## Code Style

### Python

- Follow PEP 8
- Use type hints
- Write docstrings for functions and classes
- Maximum line length: 100 characters

### JavaScript/Vue

- Use ES6+ features
- Follow Vue.js style guide
- Use meaningful variable names
- Add comments for complex logic

### Commits

- Use present tense ("Add feature" not "Added feature")
- Reference issues and PRs when applicable
- Keep commits focused and atomic

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm run test
```

## Documentation

- Update README.md if needed
- Add docstrings to new functions
- Update user guide for new features
- Include inline comments for complex code

## Community

- Be respectful and inclusive
- Help others learn and grow
- Follow the [Code of Conduct](CODE_OF_CONDUCT.md)

## Questions?

Feel free to open an issue or discussion if you have questions!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
