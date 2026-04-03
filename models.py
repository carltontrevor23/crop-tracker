from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Crop(db.Model):
    """Crop model for storing crop information."""
    __tablename__ = 'crops'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    planting_date = db.Column(db.Date, nullable=False)
    status = db.Column(
        db.String(50),
        nullable=False,
        default='Planted',
        index=True
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    STATUS_CHOICES = ['Planted', 'Growing', 'Harvested']
    
    def __repr__(self):
        return f'<Crop {self.name}>'
    
    def to_dict(self):
        """Convert crop to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'planting_date': self.planting_date.strftime('%Y-%m-%d'),
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
