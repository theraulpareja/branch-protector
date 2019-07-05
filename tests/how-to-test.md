# Tests 


### Change FLASK_ENV  to development for debuging

Is recomended to edit the edit the .flaskenv file and change the values of FLASK_ENV to development for better debuging, conider to change the port if needed too.

```
FLASK_APP=app-branch-protector.py
FLASK_ENV=prodution
FLASK_RUN_PORT=9090
```

### Simulate json payload posts from GitHub

To check only the flask appliciation, there are json files under the tests/ directory that you can use to mimic the json POST payload sent by  GitHub webhook setup.

First open a terminal and run the flask application

```
cd app-branch-protector
flask run
```

Open a second terminal and test branch-protector to simulate receiving the payload json post for GitHub due to a repository creation.
We should receive http 200 application/json "XXXX"

```
cd tests
curl -v -X POST localhost:9090/branch-protector -d @test-payload-creation.json --header "Content-Type: application/json"
```

Test branch-protector for **non creation** repository events json payloads posts
We should receive http 200 application/json "not a repository creation event"

```
cd tests
curl -v -X POST localhost:9090/branch-protector -d @test-payload-deletion.json --header "Content-Type: application/json"
```

Test branch-protector for non JSON  payloads posted
We should receive http 400 application/json "JSON payload not found"

```
cd tests
curl -v -X POST localhost:9090/branch-protector -d 'currupipi'
```
