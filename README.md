make your environment ready with below commands: \

git clone https://github.com/vimlesh-verma16/IMDB_MOVIES.git

Now go to vscode terminal and run below commands \

1.pip3 install -r requirements.txt \
2.python manage.py makemigrations movie_viewer \
3.python manage.py migrate \
4.python manage.py runserver

Run Integration test:
python manage.py test movie_viewer
