from flask import render_template, url_for, jsonify
from pathfinder.model import User, CaseFile, db, bcrypt
from flask import request, abort
from pathfinder import app
from flask_login import login_user, current_user, logout_user
# from pathfinder import PlotDataOnmap

#   final String url = "http://192.168.43.197:5000/web/PathFinder/v1.0/getcrime_api";
#   final String url2 = "http://192.168.43.197:5000/web/PathFinder/v1.0/postcrime_api";


# API end points for servicing web app
@app.route('/web/PathFinder/v1.0/getcrime_api', methods=['GET'])
def get_crime_data():
    result = []
    cases = CaseFile.query.all()

    for case in cases:
        result.append(case.serialize_to_json())

    return jsonify({'result':result})

@app.route('/web/PathFinder/v1.0/postcrime_api', methods=['POST'])
def post_crime_data():
    if not request.json:
        abort(400)
        
    case = CaseFile(
        longitude =request.json['longitude'],
        latitude  =request.json['latitude'],
        category  =request.json['category'],
        image_file=request.json['image'],
        decription=request.json['description'],
        user_id   =request.json['user_id']
    )

    db.session.add(case)
    db.session.commit()
    return jsonify({'case': case.serialize_to_json()}), 201
    

@app.route('/web/PathFinder/v1.0/loginuser', methods=['POST'])
def login_myuser():
    if current_user.is_authenticated:
        return jsonify({'response':'user logged in'})

    if not request.json:
        abort(400)

    user = User.query.filter_by(email = request.json['email']).first()
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        login_user(user)
        return jsonify({'response':'user logged in', 'name':user.username})
    else:
        return jsonify({'response':'wrong credentials'})


@app.route('/web/PathFinder/v1.0/registeruser', methods=['POST'])
def register_user():
    if current_user.is_authenticated:
        return jsonify({'response':'user logged in'})

    if not request.json:
        abort(400)
    
    # check if username and email exit
    user = User.query.filter_by(username = request.json['username']).first()
    if user:
        return jsonify({'response':'username exits'})

    useremail = User.query.filter_by(email = request.json['email']).first()
    if useremail:
        return jsonify({'response':'email exits'})
    
    # create new user
    hashed_password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
    user = User(
        username = request.json['username'],
        email    = request.json['email'],
        password = hashed_password
    )
    # save user to db
    db.session.add(user)
    db.session.commit()
    return jsonify({'response':'user created'})


@app.route('/web/PathFinder/v1.0/data/to-day')
def collect_data_today():
    datemask = '%m/%d/%Y'
    today = datetime.datetime.strftime(datetime.datetime.today(),datemask)
    today_cases = CaseFile.query.filter_by(date_posted = today)
    labels = ['thefty','Murder','kidnap','robbery']
    actual_data = [ 40,2,10,30]
    crimesdata = {
        'labels':labels,
        'data': actual_data
    }
    print('request made.............\n ')
    return jsonify({'crimesdata':crimesdata})

@app.route('/web/PathFinder/v1.0/data/')
def collect_data():
    casesData = {
        'thefty':CaseFile.query.filter_by(category = 'thefty').count(),
        'murder':CaseFile.query.filter_by(category = 'murder').count(),
        'kidnap':CaseFile.query.filter_by(category = 'kidnap').count(),
        'robbery':CaseFile.query.filter_by(category = 'robbery').count()
    }
    return jsonify({'casesData':casesData})



@app.route('/web/PathFinder/v1.0/logout')
def logout_myuser():
    logout_user()
