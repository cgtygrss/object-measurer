# 📐 Object Measurer

**Measure real-world objects using your phone camera.**

A mobile app that lets you measure objects by pointing your camera at them. Uses a hybrid processing model:
- **Real-Time Mode** — On-device OpenCV for quick estimates (~30fps)
- **Photo Mode** — Server-side full pipeline for precise measurements (±2mm)

---

## Architecture

```
┌───────────────────────────┐
│   📱 Mobile App            │
│   React Native + Expo      │
│   Vision Camera + OpenCV   │
│                             │
│   Real-Time → On-Device    │
│   Photo     → Server API   │
└────────────┬───────────────┘
             │
             ▼
┌───────────────────────────┐
│   🖥️ Backend API           │
│   FastAPI + Python          │
│   OpenCV + rembg            │
│   JWT Auth                  │
└────────────┬───────────────┘
             │
             ▼
┌───────────────────────────┐
│   🗄️ PostgreSQL            │
│   Users, Sessions,          │
│   Measurements              │
└───────────────────────────┘
```

---

## Project Structure

```
object-measurer/
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── auth/             # Authentication (JWT)
│   │   ├── measurement/      # Measurement pipeline + API
│   │   ├── main.py           # App entry point
│   │   ├── config.py         # Settings
│   │   └── database.py       # Async SQLAlchemy
│   ├── Dockerfile
│   └── requirements.txt
│
├── mobile/                   # React Native (Expo)
│   ├── app/
│   │   ├── (tabs)/
│   │   │   ├── index.tsx     # Camera tab
│   │   │   ├── history.tsx   # Measurement history
│   │   │   └── profile.tsx   # Settings & calibration
│   │   └── _layout.tsx       # Root layout
│   ├── services/api.ts       # API client
│   ├── store/index.ts        # Zustand state
│   └── constants/theme.ts    # Design tokens
│
├── Logic/                    # Original university project
└── Images/                   # Sample test images
```

---

## Getting Started

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# Start the API server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# API docs available at http://localhost:8000/docs
```

### Mobile

```bash
cd mobile
npm install

# Start the development server
npx expo start

# For development build (required for camera):
npx expo run:ios    # or
npx expo run:android
```

> **Note:** Camera features require a development build — they won't work in Expo Go.
> Update the API URL in `mobile/services/api.ts` to match your local network IP.

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/auth/register` | Create account |
| `POST` | `/api/v1/auth/login` | Login |
| `GET` | `/api/v1/auth/me` | Get profile |
| `PATCH` | `/api/v1/auth/me` | Update profile |
| `POST` | `/api/v1/measure/sessions` | Create calibration session |
| `POST` | `/api/v1/measure/upload` | Upload photo → get measurements |
| `GET` | `/api/v1/measure/history` | Measurement history |
| `GET` | `/api/v1/measure/{id}` | Measurement detail |
| `DELETE` | `/api/v1/measure/{id}` | Delete measurement |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Mobile | React Native, Expo, Vision Camera |
| Backend | Python, FastAPI, OpenCV, rembg |
| Database | PostgreSQL, SQLAlchemy |
| Auth | JWT, bcrypt |
| State | Zustand |

---

## Original Project

This project started as a university assignment for measuring objects from 2D images using OpenCV in Python. The original pipeline:
1. Capture photo via webcam
2. Remove background (rembg)
3. Edge detection (threshold + contours)
4. Pixel ratio calculation from reference object
5. Grid intersection measurement
6. Annotated image output

The server-side "Photo Mode" is a direct port of this pipeline.
