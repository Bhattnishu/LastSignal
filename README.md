# LastSignal – Lost & Found Intelligence

LastSignal is an AI-powered Lost & Found platform that helps people report lost and found items, discover possible matches, and investigate where their missing belongings might be.

Instead of simply listing lost items, LastSignal combines intelligent matching with AI-generated investigation suggestions to make item recovery easier.

## Features

- **Lost & Found Reports:** Submit lost or found item reports with descriptions, images, categories, colors, brands, and locations.
- **Possible Match Detection:** Identify potentially matching lost and found reports.
- **AI Investigation:** Get relevant places to check and identify missing information using Google Gemini.
- **Recovery Requests:** Contact the person who found an item through a recovery request.
- **Notifications:** Receive updates about possible matches and recovery requests.
- **My Activity:** Track submitted reports and sent or received recovery requests.
- **Image Storage:** Store uploaded item images securely using Amazon S3.

## Technology Stack

| Area            | Technologies                          |
| --------------- | ------------------------------------- |
| Frontend        | React, JavaScript, Vite               |
| Backend         | Python, Django, Django REST Framework |
| Database        | PostgreSQL                            |
| Authentication  | JWT (Simple JWT)                      |
| AI              | Google Gemini API                     |
| Cloud Storage   | AWS S3                                |
| Version Control | Git & GitHub                          |

## Project Structure

```text
LastSignal/
├── backend/
│   ├── accounts/
│   ├── investigations/
│   ├── items/
│   ├── config/
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.13+
- Node.js and npm
- PostgreSQL
- AWS account and S3 bucket
- Google Gemini API key

### 1. Clone the Repository

```bash
git clone https://github.com/Bhattnishu/LastSignal.git
cd LastSignal
```

### 2. Backend Setup

From the project root:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
cd backend
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file inside the `backend/` directory.

Add the following variables with your own values:

```env
DEBUG=True

DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432

AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_STORAGE_BUCKET_NAME=your_s3_bucket_name
AWS_S3_REGION_NAME=ap-southeast-2

GEMINI_API_KEY=your_gemini_api_key
```

**Important:** Never commit your `.env` file, AWS credentials, or API keys to GitHub.

### 4. Database Setup

Create a PostgreSQL database and configure the database environment variables.

Run migrations:

```bash
python manage.py migrate
```

Create an administrator account:

```bash
python manage.py createsuperuser
```

### 5. Start the Backend

```bash
python manage.py runserver
```

The backend will run at:

`http://127.0.0.1:8000/`

### 6. Frontend Setup

Open another terminal from the project root:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL displayed by Vite in your browser.

## AI and AWS Integration

### Google Gemini

LastSignal uses the Google Gemini API to generate investigation summaries, suggest possible places to check, and identify useful missing information about lost items.

### Amazon S3

Uploaded item images are stored in Amazon S3 using Django Storages. The bucket is configured for private access, with signed URLs used to access stored images.

## Future Improvements

- More advanced item matching.
- Improved investigation recommendations.
- Additional recovery and communication features.
- Production deployment and performance improvements.

## Author

**Nishant Bhatt**

GitHub: [Bhattnishu](https://github.com/Bhattnishu)

---

Built as a solo project for **Hack-to-Ween 2026**.
