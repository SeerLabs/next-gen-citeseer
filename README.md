# next-gen-citeseer
This is the FastAPI-Vue-Elasticsearch new version of CiteSeer!

## local development environment

```
Source the virtual environment [pipenv shell]
Install the dependencies [pipenv install]
Navigate into the backend directory [cd server]
install necessary python requirements [pip install -r requirements.txt]
Start the backend server [uvicorn app.main:app --port=8000]
```
For frontend setup, read client/README.md

client development server: http://localhost:3000/

Core Api: http://localhost:8000/api/v1/

## TODO
### Frontend
Store - state management

Unit Tests
### Backend API
Set up proper architecture as needed - service layer, repository layer, etc. 

Persist data from Elasticsearch and other db, remove the sqlite db if not needed

Unit Tests
