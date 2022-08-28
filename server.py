# Reference : 
# - https://nominatim.openstreetmap.org/ui/search.html

from flask import Flask, render_template, request
from app.config.middleware import checkLogin
from app.controllers import misc, user
import os

app = Flask(__name__)

## ---------- START USERS ---------- ##
@app.route("/users")
@checkLogin
def user_index():
    return user.index() 

@app.route("/users/create")
@checkLogin
def user_create():
    return user.create() 

@app.route("/users/store", methods=['POST'])
@checkLogin
def user_store():
    return user.store(request)

@app.route("/users/<int:id>/update", methods=['POST'])
@checkLogin
def user_update(id):
    return user.update(request, id)

@app.route("/users/<int:id>/edit")
@checkLogin
def user_edit(id):
    return user.edit(id)

@app.route("/users/<int:id>/delete")
@checkLogin
def user_delete(id):
    return user.delete(id)

## ---------- END USERS ---------- ##

## ---------- START DATASETS ---------- ##
@app.route('/update-dataset')
def update_dataset():
    return misc.scrapingData()


@app.route('/update-dataset-ajax')
def update_dataset_ajax():
    return misc.scrapingData(is_redirect=False)

@app.route('/check-datasets')
def check_datasets():
    return misc.checkDataset()

@app.route('/renew-html')
def renew_html():
    return misc.renew_html()
## ---------- END DATASETS ---------- ##

##MISC
@app.route("/")
def index():
    return misc.index_front()

@app.route("/dashboard")
def index_admin():
    return misc.index()

##MISC

@app.route("/login")
def login():
    return misc.login()

@app.route("/doLogin", methods=['POST'])
def doLogin():
    return misc.doLogin(request.form)

@app.route("/logout")
def logout():
    return misc.logout()

app.secret_key = '3RDLwwtFttGSxkaDHyFTmvGytBJ2MxWT8ynWm2y79G8jm9ugYxFFDPdHcBBnHp6E'
app.config['SESSION_TYPE'] = 'filesystem'

@app.context_processor
def inject_stage_and_region():
    return dict(APP_NAME=os.environ.get("APP_NAME"),
        APP_AUTHOR=os.environ.get("APP_AUTHOR"),
        APP_TITLE=os.environ.get("APP_TITLE"),
        APP_LOGO=os.environ.get("APP_LOGO"))

if __name__ == "__main__":
    app.run()
    #app.run(host='0.0.0.0', port=5299)