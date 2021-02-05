# Weatherapp

Hello Bart!
I'm trying to write it in good English for you. 

Anyways, when you'll open the branch/tree/ whatever it may be, you'll find a couple folders, a database file and a manage.py file. 
To run the server/ website you'll need to download all of the files in the coresponding folder. 
When you've done that, you can start a new or a already existing virtual environment. 

When you don't have virtualenv installed you can do this by typing the following command in the terminal: python3 -m pip install --user virtualenv
After that, make a new virtual environment: python3 -m virtualenv environmentname
To activate the environment: source environmentname/bin/activate
To open the virtualenv-folder in the virtualenv: cd environmentname

Next, open the virtualenv-folder in the files directory and put the project you've just downloaded in it. 
After that open this folder in the virtualenv folder by typing: cd TERM3PROJECT

When this is done you can run the server, however if the essential packages/modules aren't installed in the virtualenv yet, you'll need to do that first. 
For example: python3 -m pip install django
Here's an overview of all the used packages/modules:
- Django
- Requests
- Numpy
- Time

Now the only thing left is running it! 
You can do that by typing the following command: python3 manage.py runserver

Well enjoy our website! 

If there are any questions or it doesn't run, please contact us.
