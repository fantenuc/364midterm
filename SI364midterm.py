## SI 364 Midterm Project ##
## Name: Frankie Antenucci

###############################
####### SETUP (OVERALL) #######
###############################

#######################
## Import statements ##
#######################
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError # Note that you may need to import more here! Check out examples that do what you want to figure out what.
from wtforms.validators import Required, Length # Here, too
from flask_sqlalchemy import SQLAlchemy
import newsapi_info
import requests
import json


################################
## Application Configurations ##
################################
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hard to guess string from si364'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/fantenuc364midterm"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



###################
#### App setup ####
###################
db = SQLAlchemy(app) # For database use


######################################
######## HELPER FXNS (If any) ########
######################################




##################
##### MODELS #####
##################

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(64))
    username = db.Column(db.String(64))

    def __repr__(self):
        return "{} (ID: {})".format(self.user, self.id)

class Terms(db.Model):
    __tablename__ = 'terms'
    id = db.Column(db.Integer, primary_key=True)
    search_term = db.Column(db.String(64))
    results = db.relationship('Headlines', backref='Terms')

    def __repr__(self):
        return "Topic Searched: {}".format(self.search_term)

class Headlines(db.Model):
    __tablename__ = 'headlines'
    id = db.Column(db.Integer, primary_key=True)
    headline = db.Column(db.String(1000))
    source = db.Column(db.String(100))
    description = db.Column(db.String(5000))
    published = db.Column(db.String(64))
    term_id = db.Column(db.Integer, db.ForeignKey('terms.id'))

    def __repr__(self):
        return "Headline: {} (Source: {}) Published: {}".format(self.headline, self.source, self.published)

class Sources(db.Model):
    __tablename__ = 'sources'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    source = db.Column(db.String(100))
    source_rating = db.Column(db.Integer)

    def __repr__(self):
        return "{} rated the source {} a rating of {}".format(self.username, self.source, self.source_rating)


###################
###### FORMS ######
###################

class UserForm(FlaskForm):
    user = StringField('Please enter your name: ', validators=[Required()])
    username = StringField('Please enter your username (no spaces): ', validators=[Required()])

    def validate_username(self, field):
        if len(field.data.split()) > 1:
            raise ValidationError('The username you entered is not valid -- do not include a "space" in your username!')

    search_term = StringField('Please enter a topic you would like to read about: ', validators=[Required()])
    submit = SubmitField('Submit')

class SourceForm(FlaskForm):
    username = StringField('Please enter your username: ', validators=[Required()])
    source = StringField('Enter the news source you would like to rate: ', validators=[Required()])
    source_rating = StringField('Rating of news source (1-10, 1 = terrible and 10 = outstanding): ', validators=[Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    username = StringField('Please enter your username: ', validators=[Required()])
    comment = StringField('Please comment on how useful this news source application was to you: ', validators=[Required(Length(1,250))])
    useful = StringField('Would you use this application again?: ', validators=[Required()])
    submit = SubmitField('Submit')


##################################
###### Error Handling Route ######
##################################
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


#######################
###### VIEW FXNS ######
#######################

@app.route('/', methods=['GET', 'POST'])
def home():
    form = UserForm() # User should be able to enter name after name and each one will be saved, even if it's a duplicate! Sends data with GET
    if form.validate_on_submit():
        # getting name, username, and topic entered from form
        user = form.user.data
        username = form.username.data
        search_term = form.search_term.data

        # adding name and username to users table
        newuser = Users.query.filter_by(user=user, username=username).first()
        if not newuser:
            newuser = Users(user=user, username=username)
            db.session.add(newuser)
            db.session.commit()

        # calling the news api to return headlines for specific search term
        newsapiKey = newsapi_info.api_key
        baseurl = 'https://newsapi.org/v2/everything?'
        params = {'q': search_term, 'apiKey': newsapiKey}
        news_request = requests.get(baseurl, params=params)
        news_results = json.loads(news_request.text)

        term = Terms.query.filter_by(search_term=search_term).first()
        if not term:
            term = Terms(search_term=search_term)
            db.session.add(term)
            db.session.commit()

        for item in news_results['articles']:
            title = item['title']
            source = item['source']['name']
            description = item['description']
            published = item['publishedAt']

            headline = Headlines.query.filter_by(headline=title).first()
            if not headline:
                headline = Headlines(headline=title, source=source, description=description, published=published, term_id=term.id)
                db.session.add(headline)
                db.session.commit()

        return redirect(url_for('home'))

    errors = [v for v in form.errors.values()] # Citation from HW3
    if len(errors) > 0:
        flash("!!!! ERRORS IN FORM SUBMISSION - " + str(errors))
    return render_template('base.html',form=form)

@app.route('/names')
def all_names():
    users = Users.query.all()
    return render_template('name_example.html',users=users)

@app.route('/headlines')
def all_headlines():
    headlines = Headlines.query.all()
    return render_template('all_headlines.html',headlines=headlines)

@app.route('/rate_sources', methods=['GET', 'POST'])
def rate_sources():
    form = SourceForm()

    if request.method == 'POST':
        username = form.username.data
        source = form.source.data
        source_rating = form.source_rating.data

        newsource = Sources(username=username, source=source, source_rating=source_rating)
        db.session.add(newsource)
        db.session.commit()

        all_sources = Sources.query.all()
        return render_template('rate_sources.html', form=form, all_sources=all_sources)

    return render_template('rate_sources.html',form=form)

@app.route('/comments')
def comments():
    form = CommentForm()
    return render_template('leave_comments.html', form=form)

@app.route('/view_comments', methods=['GET', 'POST'])
def view_comments():
    form = CommentForm()
    if request.args:
        username = request.args.get('username')
        comment = request.args.get('comment')
        useful = request.args.get('useful')

        return render_template('comments.html', username=username, comment=comment, useful=useful)
    return redirect(url_for('comments'))



## Code to run the application...

# Put the code to do so here!
# NOTE: Make sure you include the code you need to initialize the database structure when you run the application!

if __name__ == '__main__':
    db.create_all() # Will create any defined models when you run the application
    app.run(use_reloader=True,debug=True) # The usual
