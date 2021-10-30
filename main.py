from flask import Flask, render_template, request, redirect
import operator

app = Flask(__name__, static_folder='static', static_url_path='')

movies = []

# navigates to the index page
@app.get('/')
def index():
  return render_template('index.html', 
    movies=movies)

# navigates to the add movie page
@app.get('/add-movie')
def add_movie_page():
  return render_template('add-movie.html')

# sorts the wachlist by selected genre from the dropdown menu
@app.post('/select-genre')
def select_genre():
  genre = request.form
  movies_sorted = []
  for movie in movies:
    if genre["genre"] in movie["Genre"]:
      movies_sorted.append(movie)

  return render_template("sort-by-genre.html", movies_sorted=movies_sorted)

# adds the selected movie to the watchlist if it is currently not in the list and converts runtime to an int for sorting purposes
@app.post('/add-movie-to-list')
def add_movie():
  data = dict(request.form)
  does_contain = False
  for movie in movies:
    if movie["imdbID"] == data["imdbID"]:
      does_contain = True
      break
    else:
      does_contain = False

  if does_contain == False:
    time_int = data['Runtime'].split()
    time_int = int(time_int[0])
    data['Runtime'] = time_int
    movies.append(data)

  return redirect('/')

# sorts the watchlist by runtime
@app.get('/sort')
def sort_movies():
  movies.sort(key=operator.itemgetter('Runtime'))
  return redirect('/')

# removes a movie from the watchlist when remove button is clicked
@app.get('/remove/<id>')
def remove_movie(id):
  del movies[int(id)]
  return redirect('/') 

# moves a movie up in the watchlist unless it is already at the top
@app.get('/move-up/<id>')
def move_up_movie(id):
  if int(id) != 0:
    copy = movies[int(id)]
    del movies[int(id)]
    movies.insert(int(id) - 1, copy)

  return redirect('/') 

# moves a movie down in the watchlist unless it is already at the bottom
@app.get('/move-down/<id>')
def move_down_movie(id):
  if int(id) != len(movies) - 1:
    copy = movies[int(id)]
    del movies[int(id)]
    movies.insert(int(id) + 1, copy)

  return redirect('/') 

# starts the flask app
if __name__ == '__main__':
  app.run(debug=True)
