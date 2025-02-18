# Installation Guide

## Prerequisites

- [pyenv](https://github.com/pyenv/pyenv) for managing Python versions
- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) for managing virtual environments
- [Redis](https://redis.io/) for session storage
- [Flask-Admin](https://flask-admin.readthedocs.io/) for creating administrative interfaces

## Step-by-Step Installation

1. **Install pyenv and pyenv-virtualenv on Arch Linux**:
    ```sh
    # Install dependencies
    sudo pacman -S --needed base-devel openssl zlib

    # Install pyenv
    curl https://pyenv.run | bash

    # Add pyenv to bashrc
    echo -e '\n# Pyenv Configuration' >> ~/.bashrc
    echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
    source ~/.bashrc

    # Install pyenv-virtualenv
    git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
    ```

2. **Clone and Setup**:
    ```sh
    git clone https://github.com/neuronnerd/qm.git
    cd qm
    pyenv install $(cat .python-version)
    pyenv local $(cat .python-version)
    pyenv virtualenv $(cat .python-version) qm-env
    pyenv activate qm-env
    pip install -r requirements.txt
    ```

3. **Run the Application**:
    ```sh
    flask run
    ```

## Production Deployment

To use a WSGI server like Gunicorn:
```sh
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```
