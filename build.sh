#!/bin/bash
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Initializing database..."
python -c "from app import create_app; app = create_app('production'); print('Database initialized!')"

echo "Build complete!"
