"""The app to use the knight trip"""

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


import knight
import numpy as np
import string

#chars to display on the horizontal grid of the board
all_chars = list(string.ascii_lowercase)

#create the game class with initial position [0,0] (equals: a1)
game_ij = knight.Chess_game([0,0])

app = Flask(__name__)
#put your connect to the database.
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:flask@localhost/sergey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moves.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

#The database table to store all the trips of the Knight
class Trips(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    init_cell = db.Column(db.String(20), nullable=False)
    optim = db.Column(db.String(100), nullable=False)
    moves = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime)

    def __init__(self, init_pos, optim, moves, date_created):
        self.init_cell = all_chars[init_pos[1]] + str(init_pos[0]+1)
        self.optim = optim
        self.moves = moves
        self.date_created = date_created

    def __repr__(self):
        return '<Trip %r>' % self.id 


@app.route('/results', methods=['POST','GET'])
def result():
    print("Enter to result worker") 
    trips = Trips.query.order_by(Trips.date_created).all() 
    #trips = Trips.query.paginate(per_page=10) 
    return render_template('results.html',trips=trips)


@app.route("/select/<int:row>/<int:col>")
def select(row,col): 
    try:
        knight.update_init(game_ij,[row-1,col-1])
        return redirect("/")
    except:
        return "there was a problem selecting that cell"


@app.route('/', methods=["POST","GET"])
def index():
    if request.method == 'POST':  
        try:
            if optim := request.form.getlist("opt"): 
                game_ij.move_count = knight.knight_trip(game_ij,knight.make_move_opt)
                optim = "on"
            else:
                game_ij.move_count = knight.knight_trip(game_ij,knight.make_move_reg)
                optim = "off"
            

            new_trip = Trips(game_ij.init_pos,optim,game_ij.move_count,datetime.now())
            db.session.add(new_trip)
            db.session.commit()
            knight.board_reset(game_ij)
            return redirect("/")
        except:
            return "there was an issue with the knight trip"

    else: 
        return render_template(
                        'index.html', 
                        b_size=knight.BOARD_SIZE, 
                        board_chars=all_chars[:knight.BOARD_SIZE], 
                        board=game_ij.board,
                        moves=game_ij.move_count)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)