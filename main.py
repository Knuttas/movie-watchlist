from flask import Flask, render_template, request, redirect
import operator

app = Flask(__name__, static_folder='static', static_url_path='')

movies = []

@app.get('/')
def index():
  return render_template('index.html', 
    movies=movies)

@app.get('/add-movie')
def add_movie_page():
  # render_template looks for a file in templates folder
  # matching the name
  return render_template('add-movie.html')

# with Flask 1.0
#@app.route('/add-kitten', methods=['POST'])

@app.post('/select-genre')
def select_genre():
  genre = request.form
  movies_sorted = []
  for movie in movies:
    if genre["genre"] in movie["Genre"]:
      movies_sorted.append(movie)

  return render_template("sort-by-genre.html", movies_sorted=movies_sorted)

@app.post('/add-movie-to-list')
def add_movie():
  data = request.form

  
  # add dict to list
  does_contain = False
  for movie in movies:
    if movie["imdbID"] == data["imdbID"]:
      does_contain = True
      break
    else:
      does_contain = False

  if does_contain == False:
    movies.append(data)

  # keep user on the same page
  return redirect('/')

@app.get('/sort')
def sort_movies():
  movies.sort(key=operator.itemgetter('Runtime'))
  return redirect('/')

# get a dynamic parameter (always a string)
@app.get('/remove/<id>')
def remove_movie(id):
  del movies[int(id)]

  return redirect('/') 

@app.get('/move-up/<id>')
def move_up_movie(id):
  if int(id) != 0:
    copy = movies[int(id)]
    del movies[int(id)]
    movies.insert(int(id) - 1, copy)

  return redirect('/') 

@app.get('/move-down/<id>')
def move_down_movie(id):
  if int(id) != len(movies) - 1:
    copy = movies[int(id)]
    del movies[int(id)]
    movies.insert(int(id) + 1, copy)

  return redirect('/') 

# only start server when executing this python script
if __name__ == '__main__':
  app.run(debug=True)
