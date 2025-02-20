# Network

This repository is a social network platform built using Django. Users can create posts, follow other users, and interact with posts by liking them. The platform includes a feed that displays posts from followed users.

## Live Demo: 
[https://youtu.be/I8pOWEyZsHc](https://youtu.be/DVc1pswlyQg)


## Features
- User authentication (login, logout, register).
- Create and edit posts.
- Follow/unfollow other users.
- Like/unlike posts.
- Feed displaying posts from followed users.

## Technologies Used
- Python
- Django (Backend Framework)
- SQLite (Database)
- HTML/CSS (Frontend)
- JavaScript (Dynamic Interactions)

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/MilkyLane/Network.git
   cd Network
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

3. Run migrations to set up the database:
   ```bash
   python manage.py migrate

4. Run the Django development server:
   ```bash
   python manage.py runserver

5. Open your browser and navigate to http://127.0.0.1:8000/ to access the encyclopedia.

   ## Usage
- Register or log in to your account.
- Create posts and interact with posts from other users.
- Follow/unfollow users to customize your feed.
- Like/unlike posts to show appreciation.

## Note
- This is a basic social network platform and is intended for educational purposes. For production use, additional features like notifications and enhanced security are recommended.
