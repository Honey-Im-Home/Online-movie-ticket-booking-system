
from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import AddMovie, AddShow, BookMovieShow
from .import db
from flask_login import login_required,current_user

views = Blueprint('views', __name__)
is_admin=False

@views.route('/')
@login_required
def home():
    all_data = AddMovie.query.all()
    return render_template("home.html",user =current_user,movies = all_data)

@views.route('/unsign',methods=['GET','POST'])
def unsign():
    global is_admin
    is_admin=True
    return redirect(url_for('views.sign'))

@views.route('/sign',methods=['GET','POST'])
def sign():
    global is_admin
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if password=='pass' and username=='root':
            flash('Logged in successfully!', category='success')
            #print(3)
            is_admin=True
            return redirect(url_for('views.movies'))
        else:
            flash('Incorrect password, try again.', category='error')

    return (render_template("sign.html"))

@views.route('/movies',methods = ['GET','POST'])
def movies():
    global is_admin
    all_data = AddMovie.query.all()
    if request.method == 'GET':
        #print(0)
        if is_admin:
            #print(1)
            return render_template("movies.html",movies = all_data,is_admin=is_admin)
        else:
            #print(2)
            return (redirect(url_for('views.sign')))
    if request.method == 'POST':
        movies_name = request.form.get('movies_name')
        movies_director = request.form.get('movies_director')
        genre = request.form.get('genre')
        
        movie_data = AddMovie(movies_name = movies_name , movies_director = movies_director , genre = genre)
        db.session.add(movie_data)
        db.session.commit()
        flash("Movie added Successfully!")

        return redirect(url_for('views.movies'))

    return render_template("movies.html",movies = all_data,user=current_user)

@views.route('/shows',methods = ['GET','POST'])
def shows():
    global is_admin
    all_data = AddShow.query.all()
    all_movies = AddMovie.query.all()
    if request.method == 'GET':
        #print(0)
        if is_admin:
            #print(1)
            return render_template("shows.html",shows = all_data,movies=all_movies,is_admin=is_admin)
        else:
            #print(2)
            return (redirect(url_for('views.sign')))
    if request.method == 'POST':
        movies_name = request.form.get('movies_name')
        show_date = request.form.get('show_date')
        show_time = request.form.get('show_time')
        seats = request.form.get('seats')

        show_data = AddShow(movies_name = movies_name , show_date = show_date , show_time = show_time, seats =seats)
        db.session.add(show_data)
        db.session.commit()
        flash("Show added Successfully!")

        return redirect(url_for('views.shows'))
    return render_template("shows.html",shows = all_data, movies=all_movies,user=current_user)


@views.route('/movie_show',methods = ['GET','POST'])
@login_required
def movie_show():
    all_data = AddShow.query.all()
    return render_template("movie_show.html",shows = all_data,user=current_user)


@views.route('/history',methods=['GET'])
@login_required
def history():
    all_data = BookMovieShow.query.filter(BookMovieShow.user_id==current_user.id)
    return render_template("history.html",books = all_data,user=current_user)


@views.route('/bookings',methods=['GET'])
def bookings():
    global is_admin
    all_data = BookMovieShow.query.all()
    if request.method == 'GET':
        #print(0)
        if is_admin:
            #print(1)
            return render_template("bookings.html",books = all_data,is_admin=is_admin)
        else:
            #print(2)
            return (redirect(url_for('views.sign')))
    return render_template("bookings.html",books = all_data,user=current_user)


@views.route('/update',methods =['POST'])
def update():
    
    if request.method == 'POST':
        movie_data = AddMovie.query.get(request.form.get('id'))
        movie_data.movies_name = request.form.get('movies_name')
        movie_data.movies_director = request.form.get('movies_director')
        movie_data.genre = request.form.get('genre')

        db.session.commit()
        flash("Movie Successfully Updated!")
        return redirect(url_for('views.movies'))
    return render_template("movies.html")

@views.route('/book/<id>',methods = ['GET','POST'])
def book(id):
    if request.method == 'POST':
        show_data = AddShow.query.get(id)
        movies_name = show_data.movies_name
        show_date = show_data.show_date
        show_time = show_data.show_time
        tickets = int(request.form.get('tickets'))
        if tickets > show_data.seats :
            flash("Requested number of tickets unavailable for lack of seats")
        else:
            show_data.seats -= tickets
            user_id = current_user.id
            price = 350 * int(tickets)
            book_data = BookMovieShow(movies_name = movies_name , show_date = show_date , show_time = show_time, tickets=tickets, price=price,user_id=user_id)
            db.session.add(book_data)
            db.session.commit()
            
            flash("Movie Show Successfully Booked!")
        return redirect(url_for('views.movie_show'))
    return render_template("movie_show.html")

@views.route('/delete/<id>',methods = ['GET','POST'])
def delete(id):
    movie_data = AddMovie.query.get(id)
    db.session.delete(movie_data)
    db.session.commit()
    flash("Movie Successfully Deleted!")
    return redirect(url_for('views.movies'))





    



