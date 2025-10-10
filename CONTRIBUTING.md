# Contributing to Synology Download Station Integration

Thank you for considering contributing to this project! 🎉

## Development Setup

### Prerequisites

- Python 3.11+
- Docker Desktop (for macOS/Windows)
- Git

### Local Development Environment

#### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/votre-username/synology-download-station.git
cd synology-download-station

# Start Home Assistant in development mode
docker-compose -f docker-compose.dev.yml up

# Access Home Assistant
# Open http://localhost:8123
```

#### Option 2: Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Home Assistant
pip install homeassistant

# Create config directory
mkdir -p ~/.homeassistant/custom_components

# Link your integration
ln -s $(pwd) ~/.homeassistant/custom_components/synology_download_station

# Start Home Assistant
hass --debug
```

### Testing Your Changes

1. Make your changes to the code
2. Restart Home Assistant
3. Check the logs for any errors
4. Test the integration with a real Synology NAS

### Enable Debug Logging

Add to your Home Assistant `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.synology_download_station: debug
    homeassistant.helpers.update_coordinator: debug
```

## Code Style

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints where possible
- Maximum line length: 100 characters
- Use descriptive variable names

### Example

```python
async def _async_update_data(self) -> dict[str, Any]:
    """Update data via library."""
    try:
        downloads = await self._async_get_downloads()
        if downloads is None:
            raise UpdateFailed("Failed to fetch data")
        
        return {
            "tasks": downloads,
            "total_speed": self._calculate_total_speed(downloads),
        }
    except Exception as err:
        raise UpdateFailed(f"Error updating data: {err}") from err
```

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add support for pause/resume downloads
fix: handle timeout errors gracefully
docs: update installation instructions
refactor: improve session management
test: add tests for coordinator
```

### Examples

- `feat(sensors): add download ETA sensor`
- `fix(api): increase timeout to 60 seconds`
- `docs(readme): add troubleshooting section`

## Pull Request Process

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following the code style guide
3. **Test your changes** thoroughly
4. **Update documentation** if needed (README, CHANGELOG)
5. **Create a Pull Request** with a clear description

### PR Checklist

- [ ] Code follows the project's style guidelines
- [ ] Changes have been tested locally
- [ ] Documentation updated (if applicable)
- [ ] CHANGELOG.md updated
- [ ] No linter errors (`pylint`, `mypy`)
- [ ] PR description clearly explains the changes

## Reporting Bugs

### Before Submitting

- Check existing [Issues](https://github.com/votre-username/synology-download-station/issues)
- Enable debug logging and collect logs
- Test with the latest version

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**Environment:**
 - Home Assistant version: [e.g. 2024.10.1]
 - Integration version: [e.g. 1.0.0]
 - Synology DSM version: [e.g. 7.2]
 - Download Station version: [e.g. 3.8]

**Logs:**
```
[Paste relevant logs here]
```

**Additional context**
Any other information about the problem.
```

## Feature Requests

We welcome feature requests! Please:

1. Check if the feature already exists
2. Check if there's an open issue for it
3. Provide a clear use case
4. Describe the expected behavior

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
What you want to happen.

**Describe alternatives you've considered**
Other solutions or features you've considered.

**Additional context**
Any other context or screenshots.
```

## Questions?

- Open a [Discussion](https://github.com/votre-username/synology-download-station/discussions)
- Check the [Wiki](https://github.com/votre-username/synology-download-station/wiki)
- Read the [documentation](README.md)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Thank You! 🙏

Your contributions make this project better for everyone!

