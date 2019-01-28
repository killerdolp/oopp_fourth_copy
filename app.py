from flask import Flask,render_template,request,flash,redirect,url_for
from wtforms import Form,StringField,FileField,validators,TimeField
from wtforms.fields.html5 import DateField,IntegerField,TimeField
from flask_uploads import UploadSet,configure_uploads,IMAGES

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '627e176bc1c2124a87500343b2b016ed11232'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
#Base = declarative_base()


class Tournament(db.Model):
    __tablename__="tournament"

    id= Column('id',Integer,primary_key=True)
    tournamentName=Column('TournamentName',String)
    time1=Column('time1',String)
    time2=Column('time2',String)
    date=Column('date',String)
    place=Column('place',String)
    betting_amount=Column('betting_amount',String)
    filename=Column('filename',String)
    difficulty = Column('difficulty', Integer)

    def get_id(self):
        return self.id

    def get_tournamentName(self):
        return self.tournamentName

    def get_time1(self):
        return self.time1

    def get_time2(self):
        return self.time2

    def get_date(self):
        return self.date

    def get_place(self):
        return self.place

    def get_betting_amount(self):
        return self.betting_amount

    def get_filename(self):
        return self.filename

    def get_difficulty(self):
        return self.difficulty

    def set_newName(self,newname):
        self.tournamentName=newname

    def set_newTime1(self,time):
        self.time1=time

    def set_newtime2(self,time2):
        self.time2=time2

    def set_newdate(self,date):
        self.date=date

    def set_newPlace(self,place):
        self.place=place

    def set_newBettingamount(self,bettingamount):
        self.betting_amount=bettingamount

    def set_newfilename(self,filename):
        self.filename=filename

    def set_newdifficulty(self,difficulty):
        self.difficulty=difficulty
'''
    def __init__(self,tournamentName,time1,time2,date,place,betting_amount,filename,difficulty):
        self.tournamentName=tournamentName
        self.time1=time1
        self.time2=time2
        self.date=date
        self.place=place
        self.betting_amount=betting_amount
        self.filename=filename
        self.difficulty = difficulty
'''

'''  
#sql
engine = create_engine('sqlite:///tournament.db',echo=True)
Base.metadata.create_all(bind=engine)
Session1 = sessionmaker(bind=engine)
'''

list1=[]
list10=[]


def tournamentdb_retrieve():
    global list1
    list1.clear()
    #session1 = Session1()
    matches = Tournament.query.all()
    for tour in matches:
        list1.append(tour)
    #session1.close()
    return len(list1)


#app = Flask(__name__)

# for uploading of photos
photos=UploadSet('photos',IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static'
configure_uploads(app, photos)


@app.route('/')
@app.route('/<user>')
def user(user=None):
    return render_template("home.html" ,user=user)


class FilterList(Form):
    Fdifficulty = IntegerField("Difficulty", [validators.NumberRange(min=1, max=5)])
    Fentryamount = IntegerField("Entry amount")


class CreateTournament(Form):

    Tournament_Name = StringField("Tournament Name", [validators.Length(min=4,max=50)])
    Time1 = TimeField("Time")
    Time2 = TimeField("(24 hour format)")
    Date = DateField("Date")
    Place = StringField("Place", [validators.Length(min=1,max=50)])
    Betting_amount = IntegerField("Entry Amount($)")
    Difficulty=IntegerField("Difficulty", [validators.NumberRange(min=1, max=5)])


@app.route('/create',methods=["GET","POST"])
def create():
    form = CreateTournament(request.form)
    if request.method == "POST" and form.validate() and 'photo' in request.files:
        name = form.Tournament_Name.data
        Time1 = str(form.Time1.data)
        Time2 = str(form.Time2.data)
        Date = str(form.Date.data)
        Place = form.Place.data
        Betting_amount = str(form.Betting_amount.data)
        filename = photos.save(request.files['photo'])
        Difficulty = form.Difficulty.data

        # sql
        #session1 = Session1()
        tournament = Tournament(tournamentName=name,time1=Time1,time2=Time2,date=Date,place=Place,betting_amount=Betting_amount,filename=filename,difficulty=Difficulty)
        #db.session.add(Tournament(name, Time1, Time2, Date, Place, Betting_amount, filename, Difficulty))
        db.session.add(tournament)
        db.session.commit()
        #session1.close()

        flash("The tournament have been created! ", "success")
        return redirect(url_for('find'))
    return render_template('createtournament.html', form=form)


@app.route('/findtournament', methods=["GET", "POST"])
def find():
    global list1
    global list10
    listlen = tournamentdb_retrieve()
    form10 =FilterList(request.form)

    if request.method == "POST" and form10.validate():
        difficulty=form10.Fdifficulty.data
        byentryamount=form10.Fentryamount.data

        list10.clear()
        #session=Session1()
        tests=Tournament.session.query.filter_by(difficulty=difficulty,betting_amount=byentryamount ).all()

        for test in tests:
            list10.append(test.get_id())
            print(list10)
        if len(list10)==0:
            flash('No results :(')
            pass
        else:
            return redirect(url_for('filter'))

    return render_template('findtournament.html', list=list1, id=id, listlen=listlen, form2=form10)

@app.route('/filteredTournaments')
def filter():
    global list10
    global list1
    listlen=len(list10)
    return render_template('filteredtournament.html',list10=list10,listlen=listlen,list=list1)

@app.route('/JoinTournament=<int:id>')
def index(id):
    global list1
    listlen = tournamentdb_retrieve()
    return render_template("jointournament.html", id=id, listlen=listlen, list=list1)


@app.route('/UpdateTournament=<int:id>',methods=['GET', 'POST'])
def updateTournament(id):
    global list1
    form11= CreateTournament(request.form)
    if request.method=="POST" and form11.validate() and 'photo' in request.files:
        name = form11.Tournament_Name.data
        Time1 = str(form11.Time1.data)
        Time2 = str(form11.Time2.data)
        Date = str(form11.Date.data)
        Place = form11.Place.data
        Betting_amount = str(form11.Betting_amount.data)
        filename = photos.save(request.files['photo'])
        Difficulty = form11.Difficulty.data

        #session=Session1()
        update=Tournament.session.query.filter_by(id=(id+1)).first()
        update.set_newName(name)
        update.set_newTime1(Time1)
        update.set_newtime2(Time2)
        update.set_newdate(Date)
        update.set_newPlace(Place)
        update.set_newBettingamount(Betting_amount)
        update.set_newfilename(filename)
        update.set_newdifficulty(Difficulty)
        db.session.commit()
        #session.close()
        flash("The tournament have been created! ", "success")

        return redirect(url_for('find'))
    return render_template('updatetournament.html',form=form11,id=id,list1=list1)


if __name__=="__main__":
    app.run(debug=True)
