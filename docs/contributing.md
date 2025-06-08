# Contributing Guide

Thank you for your interest in contributing to the Hospital Management System! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

1. Be respectful and inclusive
2. Exercise consideration and empathy
3. Focus on what is best for the community
4. Use welcoming and inclusive language
5. Be collaborative

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/hospital-management.git
   cd hospital-management
   ```
3. Set up development environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   ```
4. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Process

### 1. Pick an Issue

- Check existing issues or create a new one
- Comment on the issue you want to work on
- Wait for assignment from maintainers

### 2. Development Guidelines

#### Code Style
- Follow PEP 8 for Python code
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use meaningful variable and function names
- Add docstrings to functions and classes

#### Django Best Practices
- Keep views focused and simple
- Use class-based views when appropriate
- Follow Django's model naming conventions
- Write reusable template tags
- Use Django's ORM effectively

#### Frontend Guidelines
- Follow BEM methodology for CSS
- Use semantic HTML
- Ensure dark theme compatibility
- Make interfaces responsive
- Follow accessibility guidelines

### 3. Testing

Before submitting a pull request:

1. Run tests:
   ```bash
   python manage.py test
   ```

2. Run linting:
   ```bash
   flake8
   black .
   isort .
   ```

3. Test your changes:
   - Test in both light and dark themes
   - Test on different screen sizes
   - Test with different user roles
   - Verify all CRUD operations

### 4. Commit Guidelines

Follow conventional commits:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Code restructuring
- test: Adding tests
- chore: Maintenance

Example:
```
feat(appointments): add email notifications

- Add email notification system
- Configure SMTP settings
- Add notification templates

Closes #123
```

### 5. Pull Request Process

1. Update your fork:
   ```bash
   git remote add upstream https://github.com/original/hospital-management.git
   git fetch upstream
   git rebase upstream/main
   ```

2. Push your changes:
   ```bash
   git push origin feature/your-feature-name
   ```

3. Create a pull request:
   - Use a clear title and description
   - Reference related issues
   - Include screenshots if UI changes
   - List testing steps

4. PR Review:
   - Address review comments
   - Make requested changes
   - Respond to feedback
   - Update tests if needed

### 6. Documentation

Update documentation when:
- Adding new features
- Changing existing functionality
- Fixing bugs that affect user interaction
- Adding or modifying API endpoints

Documentation locations:
- Code comments and docstrings
- README.md updates
- /docs directory updates
- API documentation
- User guides

## Project Structure

```
hospital-management/
├── hospital/              # Main application
│   ├── models/           # Database models
│   ├── views/            # View logic
│   ├── forms/            # Form definitions
│   └── tests/           # Test files
├── templates/            # HTML templates
├── static/              # Static assets
├── docs/                # Documentation
└── requirements/        # Dependencies
```

## Common Tasks

### Adding a New Feature

1. Create feature branch
2. Update models if needed
3. Create/update views
4. Add templates
5. Write tests
6. Update documentation
7. Submit pull request

### Fixing Bugs

1. Create bug fix branch
2. Reproduce the bug
3. Write failing test
4. Fix the bug
5. Verify tests pass
6. Update documentation
7. Submit pull request

### Adding Documentation

1. Identify documentation need
2. Create/update relevant files
3. Include code examples
4. Add screenshots if needed
5. Submit pull request

## Getting Help

- Check existing documentation
- Search closed issues
- Join our Discord server
- Contact maintainers

## Review Process

PRs are reviewed for:
- Code quality
- Test coverage
- Documentation
- Performance
- Security
- Accessibility
- Dark theme support

## Release Process

1. Version bump
2. Update changelog
3. Create release branch
4. Run final tests
5. Create release tag
6. Deploy to production

## Recognition

Contributors are recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

## Questions?

- Open a discussion
- Join our Discord
- Email maintainers
- Check FAQ in wiki 