# 🌾 CropTracker

A simple and aesthetic web application for farmers to manage crops they are growing. Built with Flask and designed for easy deployment to Render.

## Features

- **Create** - Add new crops with planting date and status
- **Read** - View all crops in a beautiful card-based layout
- **Update** - Edit crop details (name, planting date, status)
- **Delete** - Remove crops from your collection
- **Track** - Automatically calculate days since planting

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLAlchemy with SQLite
- **Frontend**: HTML5, CSS3
- **Deployment**: Render (with Gunicorn)

## Project Structure

```
crop-tracker/
├── app.py              # Main Flask application
├── models.py           # Database models
├── config.py           # Configuration management
├── wsgi.py             # WSGI entry point for production
├── requirements.txt    # Python dependencies
├── Procfile            # Render deployment configuration
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore rules
├── README.md           # This file
└── templates/
    ├── base.html       # Base template with styling
    ├── index.html      # Home page (crop listing)
    ├── add_crop.html   # Add crop form
    ├── edit_crop.html  # Edit crop form
    ├── 404.html        # 404 error page
    └── 500.html        # 500 error page
```

## Local Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd crop-tracker
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create environment file**
   ```bash
   cp .env.example .env
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

The application will be available at `http://localhost:5000`

## Usage

### Adding a Crop
1. Click the "+ Add Crop" button in the navigation bar
2. Enter the crop name (e.g., Maize, Beans)
3. Select the planting date
4. Choose the initial status (Planted, Growing, or Harvested)
5. Click "Add Crop"

### Viewing Crops
- All crops are displayed on the home page in a card-based grid layout
- Each card shows the crop name, planting date, current status, and days since planting
- Cards are sorted by most recently added

### Editing a Crop
1. Click the "Edit" button on the crop card
2. Modify the crop details
3. Click "Update Crop"

### Deleting a Crop
1. Click the "Delete" button on the crop card
2. Confirm the deletion when prompted

## Database Schema

### Crops Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer (PK) | Unique identifier |
| name | String (100) | Crop name (e.g., Maize) |
| planting_date | Date | When the crop was planted |
| status | String (50) | Planted, Growing, or Harvested |
| created_at | DateTime | Record creation timestamp |
| updated_at | DateTime | Last update timestamp |

## Deployment to Render

### Prerequisites
- A Render account (free tier available at render.com)
- Your code pushed to a GitHub repository

### Step-by-Step Deployment

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit: CropTracker app"
   git push origin main
   ```

2. **Create a new Web Service on Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository and branch

3. **Configure the service**
   - **Name**: croptracker (or your preferred name)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn wsgi:app`
   - **Instance Type**: Free (or Standard if needed)

4. **Set Environment Variables**
   - Go to Environment tab
   - Add the following variables:
     ```
     FLASK_ENV=production
     SECRET_KEY=your-secret-key-here (generate a random string)
     DATABASE_URL=sqlite:///croptracker.db
     ```

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically deploy your app
   - You'll receive a URL like `https://croptracker.onrender.com`

### Important Notes for Render

- **Database**: SQLite works on Render but data will be reset if the service is restarted. For persistent data, consider upgrading to PostgreSQL.
- **Free Tier**: Services on the free tier will spin down after 15 minutes of inactivity
- **Custom Domain**: You can add a custom domain in Settings

## Environment Variables

Create a `.env` file in the root directory with:

```
FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///croptracker.db
```

For production (Render), update these values in the Render dashboard.

## Development

### Running Tests
```bash
# Add pytest to requirements.txt if desired
python -m pytest
```

### Database Migrations

Currently, the app uses SQLAlchemy to auto-create tables. For future migrations, consider using Flask-Migrate:

```bash
pip install Flask-Migrate
```

### Debugging

Enable debug mode in development:
```python
app.run(debug=True)
```

## Features for Future Enhancement

- User authentication and authorization
- Export crop data to CSV/PDF
- Harvest reminders and notifications
- Crop history and analytics
- Multi-user support with team management
- Photo uploads for crop progress tracking
- Weather integration for planting recommendations

## Troubleshooting

### Issue: ModuleNotFoundError when running app
**Solution**: Make sure your virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: Database lock errors
**Solution**: Delete the `croptracker.db` file and restart the app:
```bash
rm croptracker.db
python app.py
```

### Issue: Port 5000 already in use
**Solution**: Use a different port:
```bash
python -c "from app import create_app; app = create_app(); app.run(port=5001)"
```

### Issue: App won't start on Render
**Solution**: Check the logs in Render dashboard and ensure:
- All environment variables are set
- `Procfile` exists with correct command
- `requirements.txt` has all dependencies

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to fork this project and submit pull requests with improvements!

## Support

For issues or questions, please open an issue on GitHub or contact the development team.

---

**Happy Crop Tracking!** 🌱
