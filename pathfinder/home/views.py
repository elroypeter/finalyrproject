from flask import flash, abort, render_template, jsonify
from flask_login import current_user, login_required
from .forms import LoginForm, AddPoliceStationForm,RegistrationForm
from ..model import Police, User, Category, CrimeScene
from .. import db
from . import home
from ..PlotData import showmap


@home.route('/',methods=['GET', 'POST'])
def homepage():
    """
    Render the home page on / route
    """
    form = LoginForm()

    # policestations = Police.query.all()
    return render_template('home/index.html', title="welcome",
                             form=form, methods=['GET', 'POST'])

#add admin dashboard view
@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    #prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)
    showmap()
    return render_template('home/admin_dashboard.html', title="dashboard")

@home.route('/admin/policestation', methods=['POST', 'GET'])
@login_required
def police_station_data():
    if not current_user.is_admin:
        abort(403)
    form = AddPoliceStationForm()
    if form.validate_on_submit():
        police_station = Police(StationName = form.StationName.data,
                                division = form.division.data)
        db.session.add(police_station)
        db.session.commit()
        flash("You have successfully added a Police Station.")
    police_stations = Police.query.all()
    return render_template('home/police_index.html',
                            title="PoliceStation",
                            police_stations=police_stations,
                            form=form)


@home.route('/admin/register_user', methods=['GET', 'POST'])
def register_user():
    """
    Handle requests for to the database through the registration form

    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
                    email = form.email.data,
                    full_names= form.full_names.data,
                    telephone =form.telephone.data,
                    password = form.password.data
                    )
        #add employee to the database
        db.session.add(user)
        db.session.commit()
        flash('You have successively registered! You may now login.')

    #redirect to the login page
    return render_template('home/register.html', title="Register User",
                             form=form)

@home.route('/web/PathFinder/v1.0/data/to-day')
def collect_data():
    # datemask = '%m/%d/%Y'
    # today = datetime.datetime.strftime(datetime.datetime.today(),datemask)
    # today_cases = CaseFile.query.filter_by(date_posted = today)

    labels,actual_data = category_crimes_data()
    crimesdata = {
        'labels':labels,
        'data': actual_data
    }
    print('request made.............\n ')
    return jsonify({'crimesdata':crimesdata})

@home.route('/web/PathFinder/v1.0/data/')
def collect_summary_data():
    casesData = {
        'thefty':len(Category.query.filter_by(violet_type = 'thefty').first().crimescene),
        'murder':len(Category.query.filter_by(violet_type = 'murder').first().crimescene),
        'kidnap':len(Category.query.filter_by(violet_type = 'kidnap').first().crimescene),
        'robbery':len(Category.query.filter_by(violet_type = 'robbery').first().crimescene)
    }
    return jsonify({'casesData':casesData})



    """
    returns the taple of categories list the count of crimes count
    list
    """

def category_crimes_data():
    crime_categories = []
    crime_categories_count = []
    for category in Category.query.all():
        crime_categories.append(category.violet_type)
        crime_categories_count.append(len(category.crimescene))
    return crime_categories, crime_categories_count
