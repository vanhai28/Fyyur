#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from sqlalchemy.orm import relationship
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort, jsonify
jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys
from sqlalchemy.orm import Session

from utils.helpers import convertRowToObject

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
class Genres(db.Model):
    __tablename__ = 'Genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    artistItem = db.relationship('Artist', backref='genresItem',lazy=True)
    showItem = db.relationship('Show', backref='genresItem',lazy=True)

    def __repr__(self):
      f'<Genres {self.id} {self.name}'

class State(db.Model):
    __tablename__ = 'State'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    artistItem = db.relationship('Artist', backref='stateItem',lazy=True)
    venueItem = db.relationship('Venue', backref='stateItem',lazy=True)
  
    def __repr__(self):
      f'<State {self.id} {self.name}'

class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    genres_id = db.Column(db.Integer, ForeignKey('Genres.id'))
    venue_id = db.Column(db.Integer, ForeignKey('Venue.id'))
    artist_id = db.Column(db.Integer, ForeignKey('Artist.id'))
    start_time = db.Column(db.Date)
      
    def __repr__(self):
      return f'<Show {self.id} {self.genres_id} {self.venue_id} {self.artist_id} {self.start_time}'

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state_id = db.Column(db.Integer, ForeignKey('State.id'))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_description = db.Column(db.String(120))
    seeking_talent = db.Column(db.String(2))
    show = db.relationship('Show', backref='venueItem',lazy=True)

    def __repr__(self):
      return f'<Venue {self.name} {self.city} {self.state_id} {self.address} \
        {self.phone} {self.image_link} {self.facebook_link}\
            {self.website_link} {self.seeking_talent} {self.seeking_description}'
    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state_id = db.Column(db.Integer, ForeignKey('State.id'))
    phone = db.Column(db.String(120))
    genres_id = db.Column(db.Integer, ForeignKey('Genres.id'))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_description = db.Column(db.String(120))
    seeking_venue = db.Column(db.String(2))
    Show = db.relationship('Show', backref='artistItem',lazy=True)

    def __repr__(self): 
        return f'<Artist {self.id}  {self.name} {self.city} {self.state_id} \
          {self.phone} {self.genres_id} {self.image_link} {self.facebook_link} \
            {self.website_link} {self.seeking_venue} {self.seeking_description}'
    # TODO: implement any missing fields, as a database migration using Flask-Migrate


# TODO Implement Show and Artist models, and complete all model relationship and properties, as a database migration.
db.create_all()

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  if isinstance(value, str):
    date = dateutil.parser.parse(value)
  else:
    date = value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  venueList = Venue.query.join(State, Venue.state_id == State.id)\
    .add_columns(State.name).all()
  
  returnData = []
  for row in venueList:
    row_as_dict = row._mapping
    venue = convertRowToObject(row_as_dict.Venue)
    print(venue["state_id"])

    if(len(returnData) == 0):
      returnData.append({
          "city": "",
          "state": row_as_dict.name,
          "state_id": venue["state_id"],
          "venues": [{
            "id": venue["id"],
            "name": venue["name"],
            "num_upcoming_shows": 0,
          }]
        })
    else:
      isChange = False
      for i, item in enumerate(returnData):
        print('--', item["state_id"])
        if(item["state_id"] == venue["state_id"]):
          returnData[i]["venues"].append({
            "id": venue["id"],
            "name": venue["name"],
            "num_upcoming_shows": 0,
          })
          isChange = True
          break
      if(isChange != True):
        returnData.append({
            "city": "",
            "state": row_as_dict.name,
            "state_id": venue["state_id"],
            "venues": [{
              "id": venue["id"],
              "name": venue["name"],
              "num_upcoming_shows": 0,
            }]
          })

  print(returnData)
    # customResult = {
    #   'artist': artist,
    #   'artist_id': artist["id"],
    #   'artist_name': artist["name"],
    #   "artist_image_link": artist["image_link"],
    #   "start_time": row_as_dict.start_time,
    # }
    # print(customResult)
    # returnData.append(customResult)
  
  data=[{
    "city": "San Francisco",
    "state": "CA",
    "venues": [{
      "id": 1,
      "name": "The Musical Hop",
      "num_upcoming_shows": 0,
    }, {
      "id": 3,
      "name": "Park Square Live Music & Coffee",
      "num_upcoming_shows": 1,
    }]
  }, {
    "city": "New York",
    "state": "NY",
    "venues": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }]
  return render_template('pages/venues.html', areas=returnData);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  key = request.form.get('search_term')
  result = Venue.query.filter(Venue.name.like('%' + key + '%')).all()
  data = []

  for venueRow in result:
    venueObject = convertRowToObject(venueRow)
    data.append(venueObject)

  response = {
    'count': len(result),
    'data': data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)
  return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False

  try:
    name = request.form.get('name')
    city = request.form.get('city')
    state_id = request.form.get('state')
    address = request.form.get('address')
    phone = request.form.get('phone')
    image_link = request.form.get('image_link')
    facebook_link = request.form.get('facebook_link')
    website_link = request.form.get('website_link')
    seeking_description = request.form.get('seeking_description')
    seeking_talent = request.form.get('seeking_talent')

    venue = Venue(name = name, city = city, state_id = state_id, address = address,\
      phone = phone, image_link = image_link, facebook_link = facebook_link, \
        website_link = website_link, seeking_description = seeking_description, seeking_talent = seeking_talent)
   
    db.session.add(venue)
    db.session.commit()

  except:
    error = True
    db.session.rollback()
    print('error: ',sys.exc_info())
  finally:
    db.session.close()
  if(error):
    flash('An error occurred. Venue ' + venue.name + ' could not be listed.')
    abort(400)

  flash('Venue ' + request.form['name'] + ' was successfully listed!')
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    print(venue_id)
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return jsonify({'success': True})

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data=Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term=request.form.get('search_term')
  listArtist = Artist.query.filter(Artist.name.like('%' + search_term + '%')).all()
  count = len(listArtist)
  data = []

  for artist in listArtist:
    artistObject = convertRowToObject(artist)
    data.append(artistObject)
  
  response={
    "count": count,
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  data  = convertRowToObject(artist)
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  print(artist)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  error = False

  try:
    artist = Artist.query.get(artist_id)
    
    artist.name = request.form.get('name')
    artist.city = request.form.get('city')
    artist.state_id = request.form.get('state')
    artist.genres_id = request.form.get('genres')
    artist.phone = request.form.get('phone')
    artist.image_link = request.form.get('image_link')
    artist.facebook_link = request.form.get('facebook_link')
    artist.website_link = request.form.get('website_link')
    artist.seeking_description = request.form.get('seeking_description')
    artist.seeking_venue = request.form.get('seeking_venue')

    db.session.commit()
  
  except:
    error = True
    db.session.rollback()
    print('error: ',sys.exc_info())
  finally:
    db.session.close()
  if(error):
    flash('An error occurred. artist ' + artist.name + ' could not be listed.')
    abort(400)
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  error = False

  try:
    venue = Venue.query.get(venue_id)
    
    venue.name = request.form.get('name')
    venue.city = request.form.get('city')
    venue.state_id = request.form.get('state')
    venue.address = request.form.get('address')
    venue.phone = request.form.get('phone')
    venue.image_link = request.form.get('image_link')
    venue.facebook_link = request.form.get('facebook_link')
    venue.website_link = request.form.get('website_link')
    venue.seeking_description = request.form.get('seeking_description')
    venue.seeking_talent = request.form.get('seeking_talent')

    db.session.commit()
  
  except:
    error = True
    db.session.rollback()
    print('error: ',sys.exc_info())
  finally:
    db.session.close()
  if(error):
    flash('An error occurred. Venue ' + venue.name + ' could not be listed.')
    abort(400)


  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False

  try:
    name = request.form.get('name')
    city = request.form.get('city')
    state_id = request.form.get('state')
    genres_id = request.form.get('genres')
    phone = request.form.get('phone')
    image_link = request.form.get('image_link')
    facebook_link = request.form.get('facebook_link')
    website_link = request.form.get('website_link')
    seeking_description = request.form.get('seeking_description')
    seeking_venue = request.form.get('seeking_venue')

    artist = Artist(name = name, city = city, state_id = state_id, genres_id = genres_id,\
      phone = phone, image_link = image_link, facebook_link = facebook_link,\
        website_link = website_link, seeking_description = seeking_description, seeking_venue = seeking_venue)
   
    db.session.add(artist)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print('error: ',sys.exc_info())
  finally:
    db.session.close()
  if(error):
    flash('An error occurred. Venue ' + artist.name + ' could not be listed.')
    abort(400)
  # print(body)
  # on successful db insert, flash success
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data = Artist.query.join(Show, Show.artist_id == Artist.id)\
    .join(Venue, Venue.id == Show.venue_id)\
      .add_columns(Show.start_time).all()
  returnData = []
  for row in data:
    row_as_dict = row._mapping
    artist = convertRowToObject(row_as_dict.Artist)

    customResult = {
      'artist': artist,
      'artist_id': artist["id"],
      'artist_name': artist["name"],
      "artist_image_link": artist["image_link"],
      "start_time": row_as_dict.start_time,
    }
    print(customResult)
    returnData.append(customResult)
  return render_template('pages/shows.html', shows=returnData)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False

  try:
    artist_id = request.form.get('artist_id')
    venue_id = request.form.get('venue_id')
    start_time = request.form.get('start_time')

    show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time,genres_id= None)
   
    db.session.add(show)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print('error: ',sys.exc_info())
  finally:
    db.session.close()
  if(error):
    flash('An error occurred. Show could not be listed.')
    abort(400)
  # on successful db insert, flash success
  flash('Show was successfully listed!')
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
