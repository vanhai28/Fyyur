class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state_id = db.Column(db.Integer, ForeignKey('state.id'))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    def __repr__(self):
      return f'<Venue {self.name} {self.city} {self.state_id} {self.address} {self.phone} {self.image_link} {self.facebook_link}'
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

