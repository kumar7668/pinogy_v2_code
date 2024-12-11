# Pinogy
## Developing setup
1. Create virtual environment for project.

    1.1 ```virtualenv -p python3.11.3 venv```

    1.2 ```source venv/bin/activate```

2. Install dependency.

    ```pip install -r requirements/local.txt```

3. Create .env file from .env.example

4. Update directory path of media_location & temp_dir in pos_api.models.photo.py

    4.1 Create data/media folders at project level

    4.2 Set full path for media_location & temp_dir in photo.py file to your local directory

5. Migrate database ( or restore db dump if available )

    `python manage.py migrate`

6. Run server

    `python manage.py runserver`
