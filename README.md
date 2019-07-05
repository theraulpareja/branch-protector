# branch-protector

Automate master branch protection for brand new repositories in your GitHub organization.

## Configuration

## Basic configuration

There are 2 main config files:

* branch-protector/app-branch-protector/.flaskenv To control flask app ports and environments
* 




Edit the .flaskenv file and change the values of FLASK_RUN_PORT and any other you might need

```
# Flask app vars
FLASK_APP=app-branch-protector.py
# Do not use development environment in prodution!, change FLASK_ENV to production
FLASK_ENV=development
# FLASK_ENV=prodution
FLASK_RUN_PORT=9090
```


## How to use it



### flask standalone

Clone the repo and run the basic configuration



### Docker 


### Google Cloud Run





```
FLASK_APP=app-branch-protector.py
FLASK_ENV=prodution
FLASK_RUN_PORT=9090
```

## How to test

Please check the tests/how-to-test.md file for information in regards testing


### References

https://techtutorialsx.com/2017/01/07/flask-parsing-json-data/
https://www.erol.si/2018/03/flask-return-204-no-content-response/
