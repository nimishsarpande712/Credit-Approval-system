# 💳 Credit Approval System 🏦

Welcome to the **Credit Approval System**, a backend-only Django 💼 + PostgreSQL 🐘 powered application for managing customer credit, loan eligibility, and loan management — with background tasks using Celery and Redis. Fully containerized using Docker for smooth setup and portability 🚀

---

## 🧠 Made With Love by: **Nimish Sarpande** 💡

---

## 🔧 Tech Stack

- 🐍 Python 3.10+
- 🌐 Django 4.x
- 🔄 Django REST Framework
- 🐘 PostgreSQL
- 🔁 Celery + Redis (for background task queues)
- 📊 Pandas (for Excel data handling)
- 🐳 Docker & Docker Compose (for containerization)

---

## 📁 Project Structure

```bash
credit-approval-system/
├── backend/
│   ├── customers/         # Customer model, APIs
│   ├── loans/             # Loan model, logic, APIs
│   ├── utils/             # Excel ingestion, helper logic
│   ├── settings.py        # Django settings
│   ├── celery.py          # Celery app init
│   └── urls.py            # URL Routing
├── data/
│   ├── customer_data.xlsx
│   └── loan_data.xlsx
├── docker/
│   ├── Dockerfile
│   └── celery_worker.sh
├── docker-compose.yml
└── README.md              # ← You are here!
🚀 How to Run the Project
The entire system runs with a single Docker command! 🐳

✅ Prerequisites:
Docker: Download Docker

Docker Compose

Git (to clone the repository)

🧪 Steps to Start:
bash
Copy
Edit
# 1️⃣ Clone the repo
git clone https://github.com/your-username/credit-approval-system.git
cd credit-approval-system

# 2️⃣ Run all services (Django + PostgreSQL + Redis + Celery) 🚀
docker-compose up --build
This will:

🐘 Start PostgreSQL database

🔄 Start Django API server at http://localhost:8000/

🧵 Run Celery background workers for Excel ingestion

📬 Launch Redis as broker

📊 Initial Data Ingestion
Place your data files in the data/ folder:

customer_data.xlsx

loan_data.xlsx

These are auto-ingested in the background via Celery after container boot. 💾
🧑‍💻 OPTION 2: Manual Developer Setup
For development, testing, or debugging without Docker.

✅ 1. Clone and Setup Virtual Environment
bash
Copy
Edit
git clone https://github.com/your-username/credit-approval-system.git
cd credit-approval-system

# Create virtual environment
python -m venv venv
source venv/bin/activate         # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
🗃️ 2. Setup PostgreSQL Locally
Create a PostgreSQL DB and update settings.py:

python
Copy
Edit
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'creditdb',
    'USER': 'credituser',
    'PASSWORD': 'yourpassword',
    'HOST': 'localhost',
    'PORT': '5432',
  }
}
🔁 3. Run Migrations
bash
Copy
Edit
python manage.py makemigrations
python manage.py migrate
🧙‍♂️ 4. Create Superuser (Optional for admin panel)
bash
Copy
Edit
python manage.py createsuperuser
🧵 5. Start Redis (for Celery)
Make sure Redis is installed and running:

bash
Copy
Edit
redis-server
🧠 6. Start Celery Worker (in a new terminal tab)
bash
Copy
Edit
celery -A backend worker --loglevel=info
This will auto-ingest:

data/customer_data.xlsx

data/loan_data.xlsx

into your database 🎯

🌐 7. Start Django Server
bash
Copy
Edit
python manage.py runserver
Your API is live at:

bash
Copy
Edit
http://127.0.0.1:8000/

📡 API Endpoints
All endpoints follow RESTful design and return JSON.

Method	Endpoint	Description
POST	/register	➕ Register a new customer
POST	/check-eligibility	✅ Check loan eligibility
POST	/create-loan	🏦 Apply for a loan
GET	/view-loan/<loan_id>	🔍 View loan and customer details
GET	/view-loans/<customer_id>	📜 View all loans for a customer

🧠 Business Logic Highlights
Approved Limit = 36 * monthly_salary (rounded to nearest lakh)

Uses compound interest to compute EMI 💸

Loan approval logic based on:

🔹 Past loans paid on time

🔹 No. of loans taken before

🔹 Loan activity in current year

🔹 Total approved loan volume

🔹 If current debt > limit → ❌ score = 0

Final decision based on credit score 🧾

🧪 Running Tests (Optional)
If unit tests are added, you can run them with:

bash
Copy
Edit
docker-compose exec web python manage.py test
🧼 Good Practices Followed
✅ Code separation & modular apps
✅ Dockerized setup
✅ Background ingestion via Celery
✅ Proper status codes & error handling
✅ Ready for scalability

👨‍💻 Author
Made with 💙 by Nimish Sarpande
📜 License
This project is open-source under the MIT License.

💬 Final Note
“Write clean code. Handle edge cases. Approve responsibly.” 💼💸

yaml
Copy
Edit

---

Let me know if you want:

- A sample `docker-compose.yml` or `Dockerfile`
- Dummy Excel data
- Postman collection for testing APIs

I’ll help you 100%. 💪
