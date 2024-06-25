## About Project

This project implements a RESTful API for a system where users can post Ads and comment on other people's Ads using
FastAPI. Below you will find the business and technical specifications along with instructions for setting up and
running the project.

## Business Specifications

1. User Authentication: Users must be authenticated to add Ads and comments.
2. User Registration: Users can register with a unique email as a username and a password.
3. Commenting Restrictions: Each user can comment on an Ad only once.
4. Public Access: Ads and their related comments can be viewed without logging in.
5. Ad Management: Users can delete and edit their own Ads.

## Technical Specifications

* Framework: The API is built using FastAPI.
* Database: PostgreSQL is used as the database.

## Setup

1. Clone the repository:

`https://github.com/shahinAbolqasemi/advertisement-system-X2FJ.git`

2. Make config file

`cp .env.sample .env`

3. Open .env file and fill required fields
4. Install pipenv

`pip install pipenv`

5. Install required packages and libraries

`pipenv shell && pipenv install`

6. Run project

`python manage.py runserver`
