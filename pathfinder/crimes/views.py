from flask import abort, render_template
from .forms import CrimeCategory
from ..model import Category
from . import crimes


@crimes.route('/admin/crime-category')
def crimeCategory():
    form = CrimeCategory()

    # categories = Category.query.all()
    return render_template('crimes/category_index.html', 
                            title="Crime Category",
                            form=form)