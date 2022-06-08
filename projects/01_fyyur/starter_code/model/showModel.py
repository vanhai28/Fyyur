class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    venue = db.column(db.Integer, not null)
    artist = db.column(db.Integer, not null)
    start_time = db.column(db.DateTime)
