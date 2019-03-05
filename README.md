# Kit

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

Migrations
```sh
manage.py makemigrations
manage.py migrate
```

Creating user
```python
from application.models import User

u = User.objects.create_user(
    username='Your username',
    password='Your password',
    email='Your email'
)
u.save()
```

### Run Server

To run server write

```sh
source venv/bin/activate
manage.py runserver 127.0.0.1:8000
```