# flash-cards-python-backend
This is a flash cards project written in Python

If you want to see how it works:

1) Install dependencies: 
You have to use pip (or pip3 if you are using a GNU Linux distribution) to install the requirements.txt file. You can also create a new virtual environment (venv, pipenv) to install the dependencies if you like.
So in a new terminal you have to put the following:
pip install -r requirements.txt

2) Create a new SQLite database (from terminal):
First of all, you have to check out there is no a __pycache__ folder into the directory (this can cache some old database parameters or configurations and raise an error). Then in a new terminal:

    a)  Yo have to start a python3 interactive session, so you have to type into the command line: python (or python3, if you are using a GNU Linux distribution).
    b)  Finally, within the python3 interactive session you have to type the following:
        from flashcards import db
        db.create_all()
        exit()

3) Run the project:
To do that you just have go to the src directory and then to type in a command line:
    python run.py (or python3 if you are using a GNU Linux distribution)


Once you have your localhost server on, you can test the different services through an API testing tool like Postman.

