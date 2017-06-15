## Backend Experiment

This is temporary project

Description goes here:


## Installation

##### Conventions:
Considering you're going to insall it in your home folder, I'm going to represent your home folder as `/home/user`.

## Pre requisites:
```sh
$ sudo apt-get install python-virtualenv git curl
```

### Create a virtual environment
Let's call your virtual environment *VENV*. Create it in your home folder:
```sh
$ virtualenv VENV
```
Now, activate your virtual environment:
```sh
source VENV/bin/activate
```
From now on, I'm considering your always using your terminal with activated virtualenv.

### Getting this project:
In your home folder, clone this project:
```sh
$ git clone git@github.com:renatolipi/backend_experiment.git
```

### Install Python packages requirements:
Get into `backend_experiment`'s folder and install requirements:
```sh
$ cd /home/user/backnd_experiment
$ pip install -r requirements.txt
```

### "Hello World" test:
To check if it's all working, start your test server:
```sh
$ python company_project/manage.py runserver
```
Go to another terminal (this new one doesn't need to have virtualenv activated):
```sh
$ curl  http://localhost:8000/api/v1/health
```
If the response was `{"content":"ok"}`, then your installation is done.

