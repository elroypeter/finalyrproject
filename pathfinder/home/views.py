from flask import flash, abort, render_template
from flask_login import current_user, login_required
from .forms import LoginForm, AddPoliceStationForm,RegistrationForm
from ..model import Police
from .. import db
from . import home

@home.route('/')
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


@home.route('/admin/register_user')
def register_user():
    form = RegistrationForm()
    return render_template('home/register.html', title="Register User",
                             form=form)
                             