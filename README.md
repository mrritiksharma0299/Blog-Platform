# Blog Platform

A modern full-stack blogging platform built with Django, Wagtail CMS, Cloudinary, and PostgreSQL. Users can create blogs, join communities, interact through comments and likes, and participate in community discussions.

## Live Demo

https://blog-platform-nzzv.onrender.com

---

## Features

### Authentication
- User registration
- Secure login/logout
- Password change
- User profiles

### Blog System
- Create blog posts
- Edit and delete your own posts
- Rich text editor
- Upload featured images
- Categories and tags
- Search functionality
- Published posts only

### Community System
- Create communities
- Join and leave communities
- Community feed
- Community chat
- Community-specific blog posts
- Community image support

### User Interaction
- Like posts
- Comment on posts
- User profile pages
- Author information

### Homepage
- Dynamic homepage using Wagtail CMS
- Hero banner
- Featured content

### Media Management
- Cloudinary image hosting
- Automatic image uploads
- Responsive media support

### Deployment
- Deployed on Render
- PostgreSQL database
- WhiteNoise static file serving
- Production-ready Django configuration

---

## Tech Stack

### Backend
- Python 3
- Django
- Wagtail CMS

### Database
- PostgreSQL

### Frontend
- HTML5
- CSS3
- JavaScript

### Cloud
- Cloudinary
- Render

### Version Control
- Git
- GitHub

---

## Installation

Clone the repository:

```bash
git clone https://github.com/mrritiksharma0299/Blog-Platform.git
```

Move into the project:

```bash
cd Blog-Platform
```

Create a virtual environment:

```bash
python -m venv env
```

Activate it:

Windows

```bash
env\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

---

## Environment Variables

Create a `.env` file and configure:

```
SECRET_KEY=
DEBUG=
DATABASE_URL=
CLOUDINARY_URL=
ALLOWED_HOSTS=
```

---

## Screenshots

Add screenshots here after uploading images.

Example:

- Home Page
- Blog List
- Blog Detail
- Community Page
- Community Chat
- User Profile

---

## Project Structure

```
accounts/
blog/
community/
home/
notifications/
media/
static/
templates/
mysite/
```

---

## Future Improvements

- Real-time chat using WebSockets
- Notifications
- Bookmark posts
- Follow authors
- Email verification
- REST API
- Dark mode
- Mobile application

---

## Author

Ritik Sharma

GitHub:
https://github.com/mrritiksharma0299

---

## License

This project is developed for learning, portfolio, and demonstration purposes.