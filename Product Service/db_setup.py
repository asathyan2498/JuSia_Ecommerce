def init_db(app):
    with app.app_context():
        from models import db
        db.init_app(app)
        db.create_all()
