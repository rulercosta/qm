# QM

## Setup Instructions

### Prerequisites

- [pyenv](https://github.com/pyenv/pyenv) for managing Python versions
- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) for managing virtual environments
- [Redis](https://redis.io/) for session storage
- [Flask-Admin](https://flask-admin.readthedocs.io/) for creating administrative interfaces

### Installation

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

2. **Clone the Repository**:
    ```sh
    git clone https://github.com/neuronnerd/qm.git
    cd qm
    ```

3. **Recreate the [.gitignore](http://_vscodecontentref_/1) File**:
    If the [.gitignore](http://_vscodecontentref_/2) file is missing, recreate it with the following content:
    ```sh
    echo ".env" > .gitignore
    echo "flask_session/" >> .gitignore
    echo "__pycache__/" >> .gitignore
    echo ".gitignore" >> .gitignore
    ```

4. **Install Python Version**:
    Ensure you have the correct Python version specified in the [.python-version](http://_vscodecontentref_/3) file:
    ```sh
    pyenv install $(cat .python-version)
    pyenv local $(cat .python-version)
    pyenv virtualenv $(cat .python-version) qm-env
    pyenv activate qm-env
    ```

5. **Install Requirements**:
    ```sh
    pip install -r requirements.txt
    ```

6. **Set Up Environment Variables**:
    Create a [.env](http://_vscodecontentref_/4) file in the project root directory and add your environment variables. For example:
    ```env
    FLASK_ENV=development
    SECRET_KEY=your_secret_key
    SESSION_TYPE=redis
    REDIS_HOST=localhost
    REDIS_PORT=6379
    ```

7. **Run the Application**:
    ```sh
    flask run
    ```

### Using a WSGI Server

If you are deploying the application using a WSGI server like Gunicorn, use the following command:
```sh
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

## License

This project is licensed under a Proprietary License. See the [LICENSE.md](LICENSE.md) file for details.