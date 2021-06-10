# next-gen-citeseer
This is the Vue-FastAPI-Elasticsearch version of CiteSeer!

## **Setting up the local development environment**
Note: In order to run the backend API, you must have access to the port that your ElasticSearch index is running on.
### **Setting up through docker-compose**
If you wish to run the system using the docker-compose configuration, run `docker-compose build` to install the dependencies and `docker-compose up` to start-up the system. To build the frontend or backend separately (such as if changes are made and they need to be rebuilt), run `docker-compose build client` or `docker-compose build server` depending on which container needs to be rebuilt, then run `docker-compose up` as normal.

To deploy the system for a production environment, run `docker-compose -f docker-compose.yml -f production.yml up`. You must generate a Google ReCaptcha v3 key and set `RECAPTCHA_SITE_KEY` and `RECAPTCHA_SECRET_KEY` environmental variables. You can specify these variables in the `variables` directory, in which you'll need to specify them in the `development.env` and `production.env` files as such:

```
RECAPTCHA_SITE_KEY=Your site key here
RECAPTCHA_SECRET_KEY=Your secret key here
```

You can generate your site key and secret key pair at https://www.google.com/recaptcha/about/

### **Setting up manually through command line**
If you're not using the docker-compose configuration, you must manually specify the following environmental variables

```
DEBUG: A boolean that specifies if you're running in development or not.
RECAPTCHA_SITE_KEY: Google ReCaptcha v3 site key if running in production
RECAPTCHA_SECRET_KEY: Google ReCaptcha v3 secret key if running in
```

Source the virtual environment and the install necessary Python requirements `pip install -r requirements.txt`

#### **Frontend setup**
```Navigate into the client director [cd client]
# install dependencies
$ npm install

# serve with hot reload at localhost:3000
$ npm run dev

# build for production and launch server
$ npm run build
$ npm run start

# generate static project
$ npm run generate
```
`Client development server:` http://localhost:3000/

#### **Backend Setup**
```Navigate into the backend directory [cd server]
1. Install the project [python setup.py install --user]
2. Start the backend server by [python main.py] or running [uvicorn app.main:app --port=8000]
```

```Navigate into the backend directory [cd server]
Start the backend server by [python main.py]
or running [uvicorn app.main:app --port=8000]
```

`Backend Core Api:` http://localhost:8000/docs
