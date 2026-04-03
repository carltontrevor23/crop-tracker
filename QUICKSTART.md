# Quick Start Guide - CropTracker

## Get Started in 5 Minutes

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

### 3. Open in Browser
Visit: **http://localhost:5000**

### 4. Start Using
- Click "+ Add Crop" to add your first crop
- Fill in the crop details
- Click "Add Crop"
- Manage your crops with Edit and Delete buttons

---

## For Deployment to Render

1. Push to GitHub
2. Connect to Render
3. Set environment variables in Render dashboard:
   - `FLASK_ENV=production`
   - `SECRET_KEY=<generate-a-secure-random-string>`
   - `DATABASE_URL=sqlite:///croptracker.db`
4. Deploy!

See [README.md](README.md) for detailed deployment instructions.
