# Pyenv installation

**Pyenv** is a tool that allows you to install and manage multiple Python versions on your system easily. It lets you switch between different Python versions depending on the project you're working on, without version conflicts.

# Activate virtual environment
 - pipenv shell

## Prerequisites Installation for macOS

### 1. Install Python Version Manager (pyenv)
```sh
# Install pyenv to manage multiple Python versions
brew install pyenv

# Add pyenv to your shell profile (add to ~/.zshrc or ~/.bash_profile)
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc
```

### 2. Install and Configure Python
```sh
# (Recommended) Update Homebrew and pyenv to get the latest Python versions
brew update && brew upgrade pyenv

# List available Python versions
pyenv install --list

# Install recommended Python version for Playwright
pyenv install 3.13.7

# Set as global default (optional)
pyenv global 3.13.7

# Verify installation
python --version
```

### 3. Setup Virtual Environment Management
```sh
# Upgrade pip to latest version
python -m pip install --upgrade pip

# Install pipenv for virtual environment management
pip install pipenv
```

### 4. Install Playwright and Pytest
After activar tu entorno virtual con pipenv, instala Playwright y pytest:
```sh
# Activa tu shell de pipenv (si no está activa)
pipenv shell

# Instala Playwright y pytest
pipenv install pytest-playwright

# Instala Allure para reportes consolidados
pipenv install allure-pytest

# (Opcional) Instala los navegadores de Playwright
pipenv run playwright install
```

### 5. Install Allure CLI for HTML Reports
Para generar reportes HTML con Allure, necesitas instalar el CLI de Allure:
```sh
# Install Allure CLI on macOS
brew install allure

# Verify installation
allure --version
```
## Usage Commands
```sh
# Activate virtual environment
pipenv shell

# Install new dependencies
pipenv install <package-name>

# Run Python scripts
python your_script.py

# Run Playwright tests
python -m pytest

# Run tests with Allure reporting
python -m pytest --alluredir=allure-results

# Generate Allure HTML report
allure generate allure-results --clean -o allure-report

# Open Allure report in browser
allure open allure-report
```

## Test Runner Usage
El proyecto incluye un runner personalizado con múltiples opciones:

```sh
# Run on single browser
python scripts/runner.py --browser chromium

# Run on single device
python scripts/runner.py --device "iPhone 12 Pro"

# Run on all browsers with Allure reporting
python scripts/runner.py --all-browsers --allure

# Run on all mobile devices with Allure reporting
python scripts/runner.py --all-mobile --allure

# Run in headed mode (see browser)
python scripts/runner.py --all-browsers-headed --allure
```

# Playwright tips

## Pipenv tip

**Tip:** You should commit the `Pipfile` to your repository, as it defines your project's dependencies and environment. The `Pipfile.lock` is usually added to `.gitignore` to avoid conflicts between different environments, but `Pipfile` is essential for sharing your setup.

## Pytest: Running all tests in a folder

To make pytest automatically discover and run all your test files inside a custom folder (for example, `tests` or `test-specs`), add a `pytest.ini` file to your project root with the following content:

```ini
# pytest.ini
[pytest]
testpaths = tests specs
python_files = test_*.py *_test.py
```

By convention, pytest will only recognize files and folders that start with `test` (e.g., `tests/`, `test_example.py`).

Now you can simply run:

```sh
pytest
```