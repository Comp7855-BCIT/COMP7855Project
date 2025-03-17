# ----------------------------------------------
# Title: main.py
# Description: Run flask with job status filtering
# Author(s): Jasmine
# Date created: Feb 28, 2025
# Date modified: Mar 10, 2025
# ----------------------------------------------
from flask import Flask, render_template, redirect, url_for, session, request, flash
from controllers.userController import UserController
from controllers.jobController import JobController
from controllers.experienceController import ExperienceController
from initDb import initDb

app = Flask(__name__)
app.secret_key = "your_secret_key"

######### Main page ######### 
@app.route('/')
def index():
    if 'userId' not in session:
        return redirect(url_for('login'))
    userId = session['userId']

    # Read the 'status' from query params
    status_filter = request.args.get('status', '')

    # If user selected a specific status
    if status_filter:
        jobs = JobController.viewJobsByStatus(userId, status_filter)
    else:
        # Otherwise, show all jobs
        jobs = JobController.viewJobs(userId)

    username = UserController.getCurrentUsername()
    return render_template('index.html', jobs=jobs, username=username)

######### User page ######### 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        userId = UserController.validateLogin(username, password)
        if userId:
            session['userId'] = userId
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password.")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        return UserController.updateProfile()
    return UserController.viewProfile()

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        full_name = request.form.get('full-name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        username = request.form.get('user-name')
        password = request.form.get('password')

        return UserController.signUp(full_name, email, phone, username, password)

    return render_template('signUp.html')

@app.route('/signout')
def signout():
    return UserController.signout()

######### Job page ######### 
@app.route('/newJob', methods=['GET', 'POST'])
@app.route('/newJob/<int:jobId>', methods=['GET', 'POST'])
def newJob(jobId=None):
    if 'userId' not in session:
        return redirect(url_for('login'))
    userId = session['userId']  
    return JobController.newJob(jobId, userId)

@app.route('/deleteJob/<int:jobId>', methods=['GET'])
def deleteJob(jobId):
    if 'userId' not in session:
        return redirect(url_for('login'))
    return JobController.deleteJob(jobId)

@app.route('/archiveJob', methods=['GET', 'POST'])
def archiveJob():
    print("Job archive page")
    return render_template('archiveJob.html')

######### Expirence page ######### 
@app.route('/newExperience', methods=['GET', 'POST'])
def newExperience():
    return render_template('newExperience.html')

@app.route('/newWork', methods=['GET', 'POST'])
def newWork():
    print("Work page")
    return render_template('newWork.html') 

@app.route('/newVolunteer', methods=['GET', 'POST'])
def newVolunteer():
    print("Volunteer page")
    return render_template('newVolunteer.html')

@app.route('/newProject', methods=['GET', 'POST'])
def newProject():
    print("Project page")
    return render_template('newProject.html')

@app.route('/newAward', methods=['GET', 'POST'])
def newAward():
    print("Award page")
    return render_template('newAward.html')

@app.route('/newCertification', methods=['GET', 'POST'])
def newCertification():
    print("Certification page")
    return render_template('newCertification.html')

@app.route('/newEducation', methods=['GET', 'POST'])
def newEducation():
    print("Education page")
    return render_template('newEducation.html')

######### Documents page ######### 
@app.route('/resume', methods=['GET', 'POST'])
def resume():
    print("Resume page")
    return render_template('resume.html')

@app.route('/coverLetter', methods=['GET', 'POST'])
def coverLetter():
    print("Cover letter page")
    return render_template('coverLetter.html')

if __name__ == '__main__':
    initDb()
    app.run(debug=True)
