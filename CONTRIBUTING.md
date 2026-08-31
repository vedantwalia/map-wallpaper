# Contributing to MapToPoster

Thank you for your interest in contributing to MapToPoster! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Welcome new contributors

## Getting Started

### 1. Fork the Repository

```bash
git clone https://github.com/yourusername/maptoposter.git
cd maptoposter
```

### 2. Set Up Development Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

### 3. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

## Development Workflow

### Code Style

We follow PEP 8 with the following tools:

```bash
# Format code
black maptoposter/

# Sort imports
isort maptoposter/

# Check style
flake8 maptoposter/

# Type checking
mypy maptoposter/
```

### Writing Tests

- Add tests in `tests/` directory
- Use pytest conventions
- Aim for >80% coverage
- Test both happy path and edge cases

Run tests:

```bash
pytest
pytest --cov=maptoposter
```

### Type Hints

- Use type hints in all function signatures
- Use docstrings with type information
- Run mypy to catch type errors

```python
def create_poster(
    self,
    city: str,
    country: str,
    theme_name: str = "terracotta",
) -> Path:
    """Create a map poster."""
    ...
```

### Documentation

- Update README.md for user-facing changes
- Add docstrings to all public methods
- Include examples in docstrings
- Update CHANGELOG.md

### Commit Messages

Follow conventional commits:

```
feat: add new feature
fix: fix a bug
docs: update documentation
style: format code
test: add tests
chore: update dependencies
refactor: refactor code
```

Example:

```
feat(theme): add support for custom color palettes

- Add Theme.from_palette() method
- Support Coolors and Adobe Color APIs
- Add tests for palette loading
```

## Pull Request Process

1. **Before you start**: Check if an issue exists or create one
2. **Code**: Make your changes following the guidelines above
3. **Test**: Ensure all tests pass
4. **Documentation**: Update relevant docs
5. **Push**: Push to your fork
6. **PR**: Create a descriptive pull request

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation

## Related Issues
Closes #123

## Testing
- [ ] Unit tests added
- [ ] Manual testing done
- [ ] All tests pass

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Type hints added
- [ ] No new warnings
```

## Architecture Overview

### Core Classes

**MapPoster** - Main orchestrator
- Coordinates all components
- Manages poster generation workflow

**Theme** - Theme management
- Loads and manages color schemes
- Validates theme properties

**Geocoder** - Location services
- Converts city/country to coordinates
- Caches results for performance

**Renderer** - Map visualization
- Creates matplotlib figures
- Renders streets, water, parks
- Adds text overlays

### Module Dependencies

```
cli.py
  ↓
poster.py (MapPoster)
  ├─ geocoder.py (Geocoder)
  ├─ theme.py (Theme)
  └─ renderer.py (Renderer)
```

### Adding a New Feature

Example: Adding support for custom layers (e.g., railways)

1. **Modify Renderer**:
   ```python
   def _plot_railways(self, ax, point, theme):
       """Plot railways on map."""
       railways = ox.features_from_point(
           point,
           tags={'railway': 'rail'},
           dist=self.config.distance,
       )
       # ... render railways
   ```

2. **Update Theme**:
   ```python
   # Add to DEFAULT_PROPERTIES
   "railway": "#FF0000",
   ```

3. **Add tests**:
   ```python
   def test_render_railways(self):
       """Test railway rendering."""
       # Test implementation
   ```

4. **Update docs**:
   - Add to README
   - Update CHANGELOG

## Common Tasks

### Adding a New Built-in Theme

1. Add to `MapPoster._get_builtin_theme()`:

```python
"my_theme": {
    "name": "my_theme",
    "description": "Theme description",
    "bg": "#FFFFFF",
    # ... other properties
}
```

2. Test it:

```python
def test_load_my_theme(self):
    poster = MapPoster()
    theme = poster.load_theme("my_theme")
    assert theme.name == "my_theme"
```

### Adding a CLI Argument

1. Update `cli.py`:

```python
parser.add_argument(
    "--new-option",
    help="Description of option",
)
```

2. Handle in `main()`:

```python
if args.new_option:
    # Handle option
```

3. Pass to `create_poster()`:

```python
poster.create_poster(
    # ... existing args
    new_param=args.new_option,
)
```

### Adding a New Dependency

1. Update `pyproject.toml`:

```toml
dependencies = [
    # ... existing
    "new-package>=1.0.0",
]
```

2. Update `requirements.txt`:

```
new-package>=1.0.0
```

3. Update README dependencies section

## Issues and Bugs

### Reporting Issues

- Use clear, descriptive titles
- Include steps to reproduce
- Provide example output/error
- Mention your environment (OS, Python version)

### Fixing Bugs

- Create an issue if one doesn't exist
- Reference the issue in your PR
- Add a test that reproduces the bug
- Ensure fix passes the test

## Performance Considerations

- Cache expensive operations (geocoding)
- Test with large distances
- Monitor memory usage
- Profile with profiler for big changes

## Questions or Need Help?

- Open an issue with "question" label
- Check existing issues/discussions
- Review architecture documentation

## Review Process

Your PR will be reviewed by maintainers. We look for:

- ✅ Code quality and style
- ✅ Tests and coverage
- ✅ Documentation
- ✅ No breaking changes
- ✅ Clear commit messages

Thank you for contributing! 🙏
