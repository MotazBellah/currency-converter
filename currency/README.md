# Currency Converter

Application to convert the currency
App URL on Heroku https://converter-currency.herokuapp.com/

## Code style

- This project is written in python 3.
- Flask framework.
- Bootstrap in front-end

## Database Installation on Heroku

1. Create App on Heroku.

2. On app’s “Overview” page, click the “Configure Add-ons” button.

3. In the “Add-ons” section of the page, type in and select “Heroku Postgres.

4. Choose the “Hobby Dev - Free” plan, which will give you access to a free PostgreSQL database that will support up to 10,000 rows of data. Click “Provision..

5. Click the “Heroku Postgres :: Database” link.

6. Click on “Settings”, and then “View Credentials.”. This information to hock my App to the DB

7. Run `heroku run python create.py` in order to convert the SQLAlchemy class to DB table and load the data to that table.

## Project Files

- models.py: Contain the class representation for DB table.

- create.py: File to build to DB tables and scrap the xml file to get the data and load it to DB

- app.py: application file

- wtform_fields: Contain wtforms class for the form and validator

- Procfile: (For Heroku) To  declare the process type, in this app the type is "web" and Identify thread operation

- Dockerfile: contains all the commands a user could call on the command line to assemble an docker image

- convert_test.py: contain tests

- requirements.txt: Contain a list of items to be installed, use the command to install all of items `pip install -r requirements.txt`

## Run

### Dockerize the App

- To build the image from Dockerfile run on project directory run `$ docker build -t currency-converter:latest . `

- To Run the container run `$ docker run -d -p 7000:7000 currency-converter`

### Create DB

- run `python create.py`

- run `python app.py`

- go to localhost:7000

### Run the tests

- run `python convert_test.py`
