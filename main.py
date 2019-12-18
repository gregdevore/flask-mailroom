import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donor, Donation

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'POST': # POST request, process donation
        # Retrieve donor using name from form
        try:
            donor = Donor.select().where(Donor.name == request.form['donor']).get()
        except Donor.DoesNotExist:
            return render_template('create.jinja2',
                                    error='Error, donor \'{}\' not found in database.'.format(request.form['donor']),
                                    donors=Donor.select())
        # Add donation to database, credited to donor
        Donation(value=request.form['donation'], donor=donor).save()
        # Redirect to home page
        return redirect(url_for('all'))
    else: # GET request, display create template
        return render_template('create.jinja2')

@app.route('/singledonor')
def singledonor():
    donor_name = request.args.get('donor',None)
    # Check if donor has been submitted, otherwise user visiting for first time
    if not donor_name: # No donor name supplied, redirect to page
        return render_template('single.jinja2')
    else: # Donor name supplied, gather donations and inject to page
        try:
            donor = Donor.select().where(Donor.name == donor_name).get()
        except Donor.DoesNotExist:
            return render_template('single.jinja2',
                                    error='Error, donor \'{}\' not found in database.'.format(donor_name),
                                    donors=Donor.select())
        donations = Donation.select().where(Donation.donor == donor)
        return render_template('single.jinja2', donor=donor.name, donations=donations)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
