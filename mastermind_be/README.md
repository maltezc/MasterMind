# MasterMind-BE


# how to run: 
1) Clone repo
2) Create psql database: `mastermind_be`
3) Set up virtualenv inside mastermind_be folder
4) Set Env variables: 
   - SECRET_KEY=anything_you_want
   - DATABASE_URL=postgresql:///mastermind_be
   - FLASK_APP=mastermind_be
   
5) Install requirements.txt with `pip3 install -r requirements.txt `
6) Run `flask --app mastermind_be run` in outer mastermind_be


### Bug Journal
- Working with new BluePrint version and setting up.
- Leading 0s issue: example - DB number_to_guess showing 373 instead of 0372. This happened because the DB type was set to int instead of a string value.
- Always install CORS and include CORS(app) in your `__init__.py`
- Always check the network tab in chrome when a request fails.
- 

### Refresh / New Topics
- Static methods vs class methods
- New Blueprint Version

### TODO
- write tests