# PLEASE READ THIS
I didn't use the exact commit messages as specified in the milestones while doing it
so to make sure everything is ok i've added all the exact commit messages, with no changes, at once at a later point
so it might seem as though most of the project was made and pushed in one day, 
i hope this clarifies things and won't be an issue, sorry for the informal language used in the commits, thank you.

# quiz-master-project
multi-user quiz app for exam preparation for multiple courses

## To run
1. clone the repository `git clone [repository url]`
2. import requirments, (preferrably in your own env (`python -m venv .\.env`))
```pip install -r requirements.txt```
3. run create_example_db.py (or create_db.py if you would like to start with no example data)
```python .\create_example_db.py```
4. run app.py, `python .\app.py`
this will start the application on localhost:5000, 
default admin details: 
username:admin
password:password

