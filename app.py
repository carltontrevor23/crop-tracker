import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Crop
from config import config
from datetime import datetime

def create_app(config_name=None):
    """Application factory."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize database
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    # Routes
    @app.route('/')
    def index():
        """Display all crops."""
        crops = Crop.query.order_by(Crop.created_at.desc()).all()
        return render_template('index.html', crops=crops, now=datetime.now())
    
    @app.route('/add', methods=['GET', 'POST'])
    def add_crop():
        """Add a new crop."""
        if request.method == 'POST':
            try:
                name = request.form.get('name', '').strip()
                planting_date_str = request.form.get('planting_date', '')
                status = request.form.get('status', 'Planted')
                
                # Validation
                if not name:
                    flash('Crop name is required.', 'error')
                    return redirect(url_for('add_crop'))
                
                if not planting_date_str:
                    flash('Planting date is required.', 'error')
                    return redirect(url_for('add_crop'))
                
                if status not in Crop.STATUS_CHOICES:
                    flash('Invalid status.', 'error')
                    return redirect(url_for('add_crop'))
                
                planting_date = datetime.strptime(planting_date_str, '%Y-%m-%d').date()
                
                crop = Crop(name=name, planting_date=planting_date, status=status)
                db.session.add(crop)
                db.session.commit()
                
                flash(f'Crop "{name}" added successfully!', 'success')
                return redirect(url_for('index'))
                
            except ValueError:
                flash('Invalid date format. Please use YYYY-MM-DD.', 'error')
                return redirect(url_for('add_crop'))
            except Exception as e:
                db.session.rollback()
                flash(f'An error occurred: {str(e)}', 'error')
                return redirect(url_for('add_crop'))
        
        return render_template('add_crop.html', status_choices=Crop.STATUS_CHOICES)
    
    @app.route('/edit/<int:crop_id>', methods=['GET', 'POST'])
    def edit_crop(crop_id):
        """Edit an existing crop."""
        crop = Crop.query.get_or_404(crop_id)
        
        if request.method == 'POST':
            try:
                name = request.form.get('name', '').strip()
                planting_date_str = request.form.get('planting_date', '')
                status = request.form.get('status', crop.status)
                
                # Validation
                if not name:
                    flash('Crop name is required.', 'error')
                    return redirect(url_for('edit_crop', crop_id=crop_id))
                
                if not planting_date_str:
                    flash('Planting date is required.', 'error')
                    return redirect(url_for('edit_crop', crop_id=crop_id))
                
                if status not in Crop.STATUS_CHOICES:
                    flash('Invalid status.', 'error')
                    return redirect(url_for('edit_crop', crop_id=crop_id))
                
                planting_date = datetime.strptime(planting_date_str, '%Y-%m-%d').date()
                
                crop.name = name
                crop.planting_date = planting_date
                crop.status = status
                db.session.commit()
                
                flash(f'Crop "{name}" updated successfully!', 'success')
                return redirect(url_for('index'))
                
            except ValueError:
                flash('Invalid date format. Please use YYYY-MM-DD.', 'error')
                return redirect(url_for('edit_crop', crop_id=crop_id))
            except Exception as e:
                db.session.rollback()
                flash(f'An error occurred: {str(e)}', 'error')
                return redirect(url_for('edit_crop', crop_id=crop_id))
        
        return render_template('edit_crop.html', crop=crop, status_choices=Crop.STATUS_CHOICES)
    
    @app.route('/delete/<int:crop_id>', methods=['POST'])
    def delete_crop(crop_id):
        """Delete a crop."""
        crop = Crop.query.get_or_404(crop_id)
        try:
            crop_name = crop.name
            db.session.delete(crop)
            db.session.commit()
            flash(f'Crop "{crop_name}" deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'error')
        
        return redirect(url_for('index'))
    
    @app.errorhandler(404)
    def notfound(error):
        """Handle 404 errors."""
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def server_error(error):
        """Handle 500 errors."""
        return render_template('500.html'), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
