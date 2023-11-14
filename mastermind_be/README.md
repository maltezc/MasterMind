# MasterMind-BE


# how to run: 
1) Clone repo
2) Set up virtualenv inside mastermind_be folder
3) Set Env variables: 
   - SECRET_KEY
   - DATABASE_URL_TEST
   - DATABASE_URL
   - FLASK_APP
   - INT_GENERATOR_API_URL
     - https://www.random.org/integers/?num=4&min=0&max=9&col=4&base=10&format=plain&rnd=new
4) Install requirements.txt
5) Create psql database named: `mastermind`
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
- Control Depth to prevent circular Serializations
- 

### TODO
- write tests