# ----------------------------------------------
# Title: main.py
# Description: Run flask with job status filtering
# Author(s): Jasmine
# Date created: Feb 28, 2025
# Date modified: Mar 10, 2025
# ----------------------------------------------
# main.py
from flask import Flask, render_template, redirect, url_for, session, request, flash
from controllers.userController import UserController
from controllers.jobController import JobController
from controllers.experienceController import ExperienceController
from initDb import initDb

# Add this line so Python knows what JobModel is
from models.jobModel import JobModel

app = Flask(__name__)
app.secret_key = "your_secret_key"

######### Main page ######### 
@app.route('/')
def index():
    if 'userId' not in session:
        return redirect(url_for('login'))
    userId = session['userId']

    # Retrieve user's jobs (the ones they personally created)
    status_filter = request.args.get('status', '')
    if status_filter:
        jobs = JobController.viewJobsByStatus(userId, status_filter)
    else:
        jobs = JobController.viewJobs(userId)

    username = UserController.getCurrentUsername()

    # Now fetch job suggestions from the jobSuggestions table
    rawSuggestions = JobModel.getJobSuggestions(userId)
    aiSuggestions = []
    for row in rawSuggestions:
        # (id, userId, jobTitle, company, link, matchScore)
        aiSuggestions.append({
            "jobTitle":   row[2],
            "company":    row[3],
            "link":       row[4],
            "matchScore": row[5]
        })

    return render_template(
        'index.html',
        jobs=jobs,
        username=username,
        aiSuggestions=aiSuggestions
    )



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
    if request.method == 'POST':
        # If your POST is just for a future plan, you can leave it blank or redirect.
        return render_template('newExperience.html')
    else:
        # Make sure user is logged in
        if 'userId' not in session:
            return redirect(url_for('login'))
        userId = session['userId']

        # Retrieve a dictionary of experiences from the model
        from models.experienceModel import ExperienceModel
        experiences = ExperienceModel.getAllExperiencesForUser(userId)
        
        # Pass these into newExperience.html
        return render_template('newExperience.html', experiences=experiences)

@app.route('/newWork', methods=['GET', 'POST'])
def newWork():
    if request.method == 'POST':
        return ExperienceController.addWork()
    else:
        print("Work page GET")
        return render_template('newWork.html')

@app.route('/newVolunteer', methods=['GET', 'POST'])
def newVolunteer():
    if request.method == 'POST':
        return ExperienceController.addVolunteer()
    return render_template('newVolunteer.html')

@app.route('/newProject', methods=['GET', 'POST'])
def newProject():
    if request.method == 'POST':
        return ExperienceController.addProject()
    return render_template('newProject.html')

@app.route('/newAward', methods=['GET', 'POST'])
def newAward():
    if request.method == 'POST':
        return ExperienceController.addAward()
    return render_template('newAward.html')

@app.route('/newCertification', methods=['GET', 'POST'])
def newCertification():
    if request.method == 'POST':
        return ExperienceController.addCertification()
    return render_template('newCertification.html')

@app.route('/newEducation', methods=['GET', 'POST'])
def newEducation():
    if request.method == 'POST':
        return ExperienceController.addEducation()
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

@app.route('/generateSuggestions')
def generateSuggestions():
    if 'userId' not in session:
        return redirect(url_for('login'))
    userId = session['userId']
    from controllers.apiController import apiController
    suggestions = apiController.suggestJobs(userId)
    # suggestions is a list of { jobTitle, company, link, matchScore } 
    # but also we saved them in DB

    # We can also store them in session if you want immediate display 
    # but it's simpler to re-fetch from DB on next load
    return redirect(url_for('index'))


if __name__ == '__main__':
    initDb()
    app.run(debug=True)
