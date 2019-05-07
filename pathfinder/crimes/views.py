from flask import flash, request, abort, render_template
from flask_login import login_manager,login_required, current_user
from .forms import CrimeCategory

from ..model import Category, Police,CrimeScene
from .. import db
from . import crimes


@crimes.route('/admin/crime-category', methods=['POST','GET'])
@login_required
def crimeCategory():
    if not current_user.is_admin:
        abort(403)
    form = CrimeCategory()
    if form.validate_on_submit():
        category = Category(violet_type = form.violet_type.data)
        db.session.add(category)
        db.session.commit()
        flash('You have successfully added a crime category!')
    categories = Category.query.all()
    return render_template('crimes/category_index.html', 
                            title="Crime Category",
                            categories=categories,
                            form=form)

@crimes.route('/admin/add-crime', methods=['POST', 'GET'])
@login_required
def addCrime():
    if not current_user.is_admin:
        abort(403)
    if request.form:
        print(request.form)
        crime = CrimeScene(longitude = request.form.get("longitude"),
                            latitude = request.form.get('latitude'),
                            description = request.form.get('description'),
                            location = request.form.get('location'),
                            category_id = request.form.get('category'),
                            user_id = current_user.id,
                            police_id = request.form.get('police')
                            )
        db.session.add(crime)
        db.session.commit()
        flash('You have successively registered a Crime')
    categories = Category.query.all()
    police_stations = Police.query.all()
    return render_template('crimes/add_crime.html',
                            categories=categories,
                            police_stations=police_stations,
                            title="Add Crime")