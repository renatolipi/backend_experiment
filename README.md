# Backend Experiment

This is temporary project

{Description goes here}

---

## How to install

##### Conventions:
Considering you're going to insall it in your home folder, I'm going to represent your home folder as `/home/user`.

#### Pre requisites:
```
$ sudo apt-get install python-dev python-virtualenv git curl
```

#### Create a virtual environment
Let's call your virtual environment *VENV*. Create it in your home folder:
```
$ virtualenv VENV
```
Now, activate your virtual environment:
```
source VENV/bin/activate
```
From now on, I'm considering your always using your terminal with activated virtualenv.

#### Getting this project:
In your home folder, clone this project:
```
$ git clone git@github.com:renatolipi/backend_experiment.git
```

#### Install Python packages requirements:
Get into `backend_experiment`'s folder and install requirements:
```
$ cd /home/user/backend_experiment
$ pip install -r requirements.txt
```

#### "Hello World" test:
To check if it's all working, start your test server:
```
$ python company_project/manage.py runserver
```
Go to another terminal (this new one doesn't need to have virtualenv activated):
```
$ curl -i -X GET -H "Content-Type: application/json" -H "Authorization: 00123456789ABCDEF"  http://localhost:8000/api/v1/health
```
If the response was `{"content":"ok"}` (status code 200), then your installation is done.

---

## How to setup

#### Database initialization
This project is cofigured to use SQLite3. Considering you are in `/home/user/backend_experiment/company_project`, the command below will initiate your database:
```
$ python manage.py migrate
```

#### Create a admin user
Then you should create a user with administrative privileges:
```
$ python manage.py createsuperuser
```
Fill in with some user name, e-mail and choose a password as it goes through your terminal. Thus, you are able to access the application admin area. But first, remember to turn on your test server:
```
$ python manage.py runserver
```
Now, hit `http://localhost:8000/admin` on your web browser. Login with username and password you typed above.

---

## Runing tests
 Once you are in `/home/user/backend_experiment/company_project`, type:
 ```
 $ python manage.py tests
 ```

 ---

 ## API Docs

  There is a specific document called API.md at `backend_experiment/docs/` where you can find all instructions to use the API. We included calls using `curl`, as example.

  You can also paste the content of the file `backend_experiment/docs/api.swagger` into Swagger's online editor: `http://editor.swagger.io`, to read it pretty well formatted. **Remember:** although Swagger's online editor can generate the API client code, this `api.swagger` file was created intended to format API docs. I do not encourage you to use any auto generated code.

