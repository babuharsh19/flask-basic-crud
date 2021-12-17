from flask import Flask, redirect, render_template, session,flash,url_for, request
import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import StringField, SubmitField, RadioField, IntegerField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/letsupcrud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'MY SECRET KEY'

db = SQLAlchemy(app)

class Homeform(Form):
    choice = RadioField('Please Select Your choice : ',choices=[('1', 'Tutor'),('2', 'Candidate')] )
    submit = SubmitField('Submit')

class AddTutor(Form):
     name = StringField('Enter your name : ',validators = [DataRequired()])
     batches = IntegerField('Enter number of batches you are teaching : ',validators = [DataRequired()])
     experience = StringField('Enter your experience : ',validators = [DataRequired()])
     company = StringField('Enter your company : ',validators = [DataRequired()])
     submit = SubmitField('Submit')

class DelTutor(Form):
    id = IntegerField('Enter your id to delete record ',validators=[DataRequired()])
    submit = SubmitField('Submit')

class Edittutor(Form):
    id = IntegerField('Enter your id ')
    batches = IntegerField('Enter number of batches you are teaching : ',validators = [DataRequired()])
    experience = StringField('Enter your experience : ',validators = [DataRequired()])
    company = StringField('Enter your company : ',validators = [DataRequired()])
    submit = SubmitField('Submit')

class Candidates(db.Model):
    id = db.Column(db.Integer(),nullable=False,primary_key = True)
    name = db.Column(db.String(25),nullable=False)
    age = db.Column(db.Integer(),nullable=False)
    program = db.Column(db.String(40),nullable=False)
    work = db.Column(db.String(40),nullable=False)

class Tutors(db.Model):
    id = db.Column(db.Integer(),nullable=False,primary_key = True)
    name = db.Column(db.String(25),nullable=False)
    batches = db.Column(db.Integer(),nullable=False)
    experience= db.Column(db.String(40),nullable=False)
    company = db.Column(db.String(40),nullable=False)

#db.create_all()

@app.route('/',methods=['GET', 'POST'])
def index():
    homeform = Homeform()
    if homeform.validate():
        session['choice'] = homeform.choice.data
    return render_template('home.html',homeform=homeform)

@app.route('/view-tutor',methods=['GET', 'POST'])
def ViewTutor():
    tutors = Tutors.query.all()
    return render_template('view-tutor.html',tutors=tutors)

@app.route('/add-tutor',methods=['POST','GET'])
def addTutor():
    addtutor = AddTutor()
    if addtutor.validate():
        name = addtutor.name.data
        batches = addtutor.batches.data
        experience = addtutor.experience.data
        company = addtutor.company.data
        newtutor = Tutors(name=name,batches=batches,experience=experience,company=company)
        db.session.add(newtutor)
        db.session.commit()
        flash('Tutor added succesfully ')
        return redirect(url_for('view-tutor'))
    return render_template('add-tutor.html',addtutor=addtutor)

@app.route('/del-tutor',methods=['GET','POST'])
def delTutor():
    deltutor = DelTutor()
    if deltutor.validate():
        id = deltutor.id.data
        del_data = Tutors.query.get(id=id)
        db.session.delete(del_data)
        db.session.commit()
        return redirect(url_for('view-tutor'))
    return render_template('del-tutor.html',deltutor=deltutor)

@app.route('/edit-tutor',methods=['GET', 'POST'])
def EditTutor():
    edittutor = Edittutor()
    if edittutor.validate():
        id = edittutor.id.data
        batches = edittutor.batches.data
        experience = edittutor.experience.data
        company = edittutor.company.data
        update_data = Tutors.query.get(id=id)
        update_data.batches = batches
        update_data.experience = experience
        update_data.company = company
        db.session.commit()
        return redirect(url_for('view-tutor'))
    return render_template('edit-tutor',edittutor=edittutor)


app.run(debug=True)
