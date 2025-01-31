# HackerNews Scraper Documentation

This repository contains a Python application designed to scrape the latest technology news from Hacker News. The scraper fetches top stories, job postings, and discussions, providing an organized collection of the most recent and popular content.

## Features
- **Periodic Scraping:** Automatically scrapes Hacker News at regular intervals (default: every 5 minutes) to keep the data up-to-date.
- **Search Functionality:** Allows users to search for specific news articles or topics.
- **Pagination:** Enables convenient navigation through lists of news items.
- **Filtering:** Provides options to filter news based on news type.
- **API Access:** Offers API endpoints to post, delete, and update news articles, facilitating easy integration with front-end frameworks.

## Live Demo
A live version of the application is available at: [HackerNews Scraper](https://hackernews-scraper.onrender.com/)

## Technology Stack
- **Backend Framework:** Django
- **API Framework:** Django Rest Framework (DRF)
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS (Bootstrap)

## Setting Up for Local Development

### Verify Python Installation
Ensure Python 3 is installed:
```bash
python --version
```

### Install Virtual Environment
```bash
pip install virtualenv
```

### Clone the Repository
```bash
git clone https://github.com/timmyades3/hackernews-scraper.git
cd hackernews-scraper
```

### Create and Activate Virtual Environment
```bash
virtualenv venv
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Set Up PostgreSQL Database
1. Install PostgreSQL locally.
2. Create a new database and user.
3. Update the `.env` file with your database credentials.

### Example `.env` File
Rename `.env_sample` to `.env` and update it with your credentials:
```
DATABASE_NAME=your_database_name
DATABASE_USER=your_database_user
DATABASE_PASSWORD=your_database_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
SECRET_KEY=your_secret_key
DEBUG=True 
```

### Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Start Redis Server
```bash
redis-server
```

### Start Celery Worker
```bash
celery -A core worker --loglevel=info
```

### Start Celery beat
```bash
celery -A core beat --loglevel=info 
```

### Run the Application
```bash
python manage.py runserver
```
Access the application at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Running Tests
### Run All Tests
```bash
python manage.py test
```

### Run Specific Test
```bash
python manage.py test api.tests.unit.testnewsscrape
```

### Run Tests in a Folder
```bash
python manage.py test <folder_name>
```

## API Endpoints
Detailed API documentation is available at the `/api/docs/` route.

Live API URL: [hackernews-scraper](https://hackernews-scraper.onrender.com/swagger/)

## License
This project is licensed under the MIT License.

## Acknowledgments
This project utilizes several open-source libraries and frameworks, including Django, Django Rest Framework, and Bootstrap.
