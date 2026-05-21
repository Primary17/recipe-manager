# RecipeManager

Django-application for recipes and categories management.

## Features

- Main page (`/`) — last 5 created recipes.
- Categories list (`/categories/`) — all categories with number of recipes  in each.
- Admin-panel Django for data management/

## Run

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Load data

```bash
python manage.py loaddata initial_data.json
```

## Tests

```bash
python manage.py test recipe
```