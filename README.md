# BajaGhar — Traditional Nepali Instruments

An interactive web platform showcasing traditional Nepali musical instruments with interactive 3D models, expert profiles, and educational resources.

## Live Demo

- Website: https://bajanepal.com
- API: https://bajanepal.com/api

## Quick Overview

- Frontend: React + Vite, React Three Fiber for 3D
- Backend: Django + Django REST Framework, SQLite (development)
- Auth: Simple JWT for API authentication
- Hosting: Passenger WSGI (production)

## Fast Start (Development)

1. Clone the repo and install dependencies:

```bash
git clone https://github.com/Nabintimsina/BajaGhar_Nepal.git
cd "BajaGhar_Nepal"
npm install
```

2. Backend (Windows example):

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

3. Frontend (root folder):

```bash
npm run dev
```

4. Open the app:

- Frontend: http://localhost:5173
- API: http://localhost:8000/api
- Admin: http://localhost:8000/admin

## Project Layout

See the repository root for a full layout. Key folders:

- `backend/` — Django project and `catalog` app (models, serializers, views)
- `src/` — React frontend (components, pages, api client)
- `public/` — Static assets (images, models)

## Features

- Browse instruments with descriptions and media
- Interactive 3D model viewer for instruments
- Expert profiles with photos and contact info
- Contact form to submit inquiries
- Admin panel for managing instruments, experts, and submissions



## API (selected endpoints)

| Endpoint | Method | Purpose |
|---|---:|---|
| `/api/instruments/` | GET | List instruments |
| `/api/instruments/:id/` | GET | Instrument details |
| `/api/experts/` | GET | List experts |
| `/api/experts/:id/` | GET | Expert details |
| `/api/contact/` | POST | Submit contact form |

## Contributing

Contributions are welcome. Suggested workflow:

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/your-feature`)
3. Implement and test locally
4. Submit a pull request with a clear description

Please run backend migrations and frontend build checks before opening a PR.

## Support

Report bugs or request help via the repository Issues.

## Author

Nabin Timsina — https://github.com/Nabintimsina

---

Made with ❤️ to preserve and promote Nepali musical heritage
