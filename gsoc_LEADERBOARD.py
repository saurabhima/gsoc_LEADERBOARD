from flask import Flask,request,redirect,url_for
from flask.templating import render_template
import pickle
import os
import datetime
app = Flask(__name__)
app.config['DEBUG']=True

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/donorleaderboard')
def donors():
    fh=open('donor_details.pickle','rb')
    pickle_obj=pickle.load(fh)
    print(pickle_obj)
    return render_template('donor_leaderboard.html',donor_list=pickle_obj)

@app.route('/add_donor_to_leaderboard')
def add_donors():
    return render_template('insert_donor_to_leaderboard.html')

@app.route('/process_donor_form',methods=['POST'])
def process_add_donors():
    title=request.form['donor_title']
    name = request.form['donor_name']
    org = request.form['donor_org']
    email=request.form['donor_email']
    donated_amount = request.form['donated_amount']
    donor_contact=request.form['donor_contact']
    contact_person=request.form['contact_person']
    contact_date=request.form['contact_date']
    donor_list=[]
    donor_pickle_filename = 'donor_details.pickle'

    if os.path.exists(donor_pickle_filename):
        with open(donor_pickle_filename, 'rb') as rfp:
            donor_list = pickle.load(rfp)




    donor={}
    donor['title'] = title
    donor['name']=name
    donor['org']=org
    donor['amount']=donated_amount
    donor['phone']=donor_contact
    donor['email'] = email
    donor['contact_person'] = contact_person
    donor['contact_date'] = contact_date
    donor['donation_date']=datetime.datetime.now().date().strftime ("%Y-%m-%d")
    donor_list.append(donor)

    with open(donor_pickle_filename, 'wb') as wfp:
        pickle.dump(donor_list, wfp)

    return redirect(url_for('donors'))
if __name__ == '__main__':
    app.run()
