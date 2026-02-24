# 📏 Object Measurer

> Measure real-world objects from photos — available as a mobile app for **iOS** and **Android**.

Take a photo of any object, provide a known reference measurement, and get accurate dimensions automatically. Export results as PDF or share with others.

---

## 📱 Features

- **Camera Capture** — Take photos directly with alignment grid and flash control
- **Gallery Import** — Pick images from your photo library
- **Background Removal** — AI-powered background removal for clean edge detection
- **Auto Measurement** — Detects edges and calculates real-world dimensions
- **Multiple Units** — Supports mm, cm, m, in, ft
- **Measurement History** — Browse and manage all past measurements
- **PDF Export** — Generate professional measurement reports
- **Share Results** — Share annotated images directly from the app
- **AR Overlay** — SVG-based measurement line overlay on result images
- **Dark Theme** — Beautiful dark UI designed for comfortable use

---

## 🏗️ Architecture

```
object-measurer/
├── backend/              # Python FastAPI server
│   ├── app/
│   │   ├── main.py       # FastAPI app entry
│   │   ├── config.py     # Settings & environment config
│   │   ├── database/     # SQLAlchemy async setup
│   │   ├── models/       # DB models + Pydantic schemas
│   │   ├── routes/       # API endpoints
│   │   │   ├── measure.py    # POST /api/measure/
│   │   │   ├── history.py    # CRUD /api/history/
│   │   │   └── export.py     # PDF /api/export/
│   │   └── services/     # Image processing pipeline
│   │       ├── background_removal.py
│   │       ├── edge_detection.py
│   │       ├── intersection.py
│   │       ├── measurement.py
│   │       └── pixel_ratio.py
│   ├── Dockerfile
│   └── requirements.txt
├── mobile/               # React Native (Expo) app
│   ├── app/              # Expo Router screens
│   │   ├── (tabs)/       # Tab navigator
│   │   │   ├── index.tsx     # Home screen
│   │   │   ├── scan.tsx      # Camera/Gallery picker
│   │   │   ├── history.tsx   # Measurement history
│   │   │   └── settings.tsx  # App settings
│   │   ├── camera.tsx        # Full-screen camera
│   │   ├── measure.tsx       # Measurement form
│   │   └── result/[id].tsx   # Result detail + export
│   └── src/
│       ├── api/          # API client
│       ├── components/   # Reusable components
│       ├── config/       # App configuration
│       └── theme/        # Colors, spacing, typography
├── docker-compose.yml
└── Logic/                # Original Python scripts (legacy)
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+** (backend)
- **Node.js 18+** (mobile app)
- **Expo CLI** (`npm install -g expo-cli`)
- **Expo Go** app on your phone (for development)

### 1. Start the Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Copy env file and configure
cp .env.example .env

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`. Visit `http://localhost:8000/docs` for the interactive Swagger UI.

### 2. Start the Mobile App

```bash
cd mobile

# Install dependencies
npm install

# Start Expo dev server
npx expo start
```

Then scan the QR code with **Expo Go** (Android) or the Camera app (iOS).

> **Note**: If running on a physical device, update `API_BASE_URL` in `mobile/src/config/api.ts` with your machine's local IP address (e.g., `http://192.168.1.100:8000`).

### 3. Using Docker (Backend only)

```bash
docker-compose up -d
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/measure/` | Upload image and get measurements |
| `GET` | `/api/history/` | List all measurements (paginated) |
| `GET` | `/api/history/{id}` | Get measurement details |
| `PATCH` | `/api/history/{id}` | Update title/notes |
| `DELETE` | `/api/history/{id}` | Delete measurement |
| `GET` | `/api/export/{id}/pdf` | Download PDF report |
| `GET` | `/health` | Health check |

### Example: Measure an Object

```bash
curl -X POST http://localhost:8000/api/measure/ \
  -F "image=@photo.jpg" \
  -F "reference_height=15.5" \
  -F "unit=cm" \
  -F "title=My Object"
```

---

## 🔧 Processing Pipeline

1. **Background Removal** — Uses `rembg` (U²-Net) to isolate the object
2. **Edge Detection** — Gaussian blur + binary threshold + morphological cleanup + contour detection
3. **Grid Intersection** — Finds where object edges cross a measurement grid
4. **Pixel Ratio Calibration** — Uses known reference height to map pixels → real units
5. **Measurement** — Calculates distances between intersection points
6. **Annotation** — Draws measurement lines and labels on the image
7. **PDF Report** — Generates a formatted report with all measurements

---

## 📱 Building for Production

### iOS (App Store)

```bash
cd mobile

# Build for iOS
npx eas build --platform ios --profile production

# Submit to App Store
npx eas submit --platform ios
```

### Android (Google Play)

```bash
cd mobile

# Build for Android
npx eas build --platform android --profile production

# Submit to Google Play
npx eas submit --platform android
```

### EAS Configuration

Create `mobile/eas.json`:

```json
{
  "cli": { "version": ">= 5.0.0" },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal"
    },
    "preview": {
      "distribution": "internal"
    },
    "production": {}
  },
  "submit": {
    "production": {}
  }
}
```

---

## 🛡️ App Store Checklist

- [ ] App icons (1024×1024 for iOS, 512×512 for Google Play)
- [ ] Splash screen assets
- [ ] Screenshots for all device sizes
- [ ] Privacy policy URL
- [ ] Terms of service URL
- [ ] App description and keywords
- [ ] EAS build profiles configured
- [ ] Backend deployed to a cloud provider (AWS, GCP, Railway, etc.)
- [ ] Custom domain for API
- [ ] SSL/TLS certificate
- [ ] Rate limiting on API
- [ ] Error tracking (Sentry)
- [ ] Analytics (optional)

---

## 🧪 Tech Stack

| Layer | Technology |
|-------|-----------|
| Mobile | React Native + Expo (TypeScript) |
| Navigation | Expo Router (file-based) |
| Backend | Python + FastAPI |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Image Processing | OpenCV, rembg, Pillow |
| PDF Generation | ReportLab |
| Deployment | Docker, EAS Build |

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
