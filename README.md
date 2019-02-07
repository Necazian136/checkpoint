# Checkpoint

### Installation

Requires [Python](https://www.python.org/downloads/) v3+ to run.

Download project
```sh
git clone https://github.com/Necazian136/checkpoint
cd checkpoint
```

Create a virtual environment

```sh
python3 -m venv venv
source venv/bin/activate
```

Install packages

```sh
pip install django
pip install numpy
pip install Pillow
pip install opencv-python
```

### Run Server

To run server write

```sh
source venv/bin/activate
manage.py runserver 127.0.0.1:8000
```