📰 News Site — Full Stack News Platform
A full-stack news platform with subscriptions, comments, and Stripe payments.
Live Demo:

🌐 Frontend: app-news-2-74rz.onrender.com
🔧 Backend API: app-news-1-kpkv.onrender.com


🛠 Tech Stack
Backend

Python 3.10 + Django 5.2 + Django REST Framework
PostgreSQL — primary database
Cloudinary — media file storage (avatars, post images)
Stripe — subscription payments
JWT (SimpleJWT) — authentication
Celery + Redis — background tasks
Gunicorn + Docker — production deployment

Frontend

Vue.js 3 + Vite
Pinia — state management
Axios — HTTP client
Tailwind CSS — styling
Vue Router — client-side routing

Infrastructure

Render — cloud deployment (backend + frontend)
Docker — containerization


✨ Features

📝 Create, edit, delete posts with images
💬 Comments and nested replies
👤 User profiles with avatars
🔐 JWT authentication (register, login, refresh tokens)
💳 Stripe subscription payments (Premium Monthly)
📌 Pin posts (premium feature)
🔍 Search and filter posts by category
📊 Post views and comments count
🔔 Subscription status tracking
📱 Fully responsive design


🚀 Getting Started
Prerequisites

Python 3.10+
Node.js 20+
PostgreSQL
Redis (for Celery)

Backend Setup
bashcd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Fill in your environment variables

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
Frontend Setup
bashcd frontend

# Install dependencies
npm install

# Create .env file
VITE_API_URL=http://localhost:8000

# Run development server
npm run dev

⚙️ Environment Variables
Backend .env
envSECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Cloudinary
CLOUD_NAME=your_cloud_name
API_KEY=your_api_key
API_SECRET=your_api_secret

# Stripe
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Email
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=your_password

# Frontend URL
FRONTEND_URL=http://localhost:5173

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

🐳 Docker Deployment
bash# Backend
cd backend
docker build -t news-backend .
docker run -p 8000:8000 --env-file .env news-backend

📁 Project Structure
app-news/
├── backend/
│   ├── apps/
│   │   ├── accounts/      # User auth & profiles
│   │   ├── main/          # Posts & categories
│   │   ├── comments/      # Comments system
│   │   ├── subscribe/     # Subscription plans
│   │   └── payment/       # Stripe payments
│   ├── config/
│   │   ├── settings.py
│   │   └── urls.py
│   ├── Dockerfile
│   ├── start.sh
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── components/    # Vue components
    │   ├── views/         # Page views
    │   ├── stores/        # Pinia stores
    │   ├── services/      # API services
    │   └── router/        # Vue Router
    ├── public/
    └── vite.config.js

🔑 API Endpoints
Auth
MethodEndpointDescriptionPOST/api/v1/auth/register/RegisterPOST/api/v1/auth/login/LoginPOST/api/v1/auth/logout/LogoutGET/PUT/api/v1/auth/profile/Get/Update profilePOST/api/v1/auth/token/refresh/Refresh token
Posts
MethodEndpointDescriptionGET/api/v1/posts/List postsPOST/api/v1/posts/Create postGET/api/v1/posts/{slug}/Get postPUT/api/v1/posts/{slug}/Update postDELETE/api/v1/posts/{slug}/Delete post
Subscriptions
MethodEndpointDescriptionGET/api/v1/subscribe/plans/Get plansGET/api/v1/subscribe/status/Subscription statusPOST/api/v1/payment/create-checkout-session/Create Stripe session

📝 License
MIT License — feel free to use this project for learning purposes.

👤 Author
Made with ❤️ by AAAArtteem21