# Tests branch-protector locally


## Change FLASK_ENV  to development for debuging

Is recomended to edit the edit the .flaskenv file and change the values of FLASK_ENV to development for better debuging, conider to change the port if needed too.

```
FLASK_APP=app-branch-protector.py
FLASK_ENV=prodution
FLASK_RUN_PORT=9090
```

## Simulate json payload posts from GitHub

To test the flask appliciation you will need to:

* Create a webhook in your GitHiub organization, you will need admin or owner permitions (use your organization to complete the url) https://github.com/organizations/<ORGANIZATION>/settings/hooks .
* Click radio button `Let me select individual events.` and select **ONLY** `Repositories` check box.
* Select `Acitve` check box an push `Add Webhook`
* Create a brand new repository within your organization and initialize it with a README file

If you don't have exposed DNS:PORT or IP:PORT to the public yet, you can go to your webhooks  https://github.com/organizations/YOUR-ORGA/settings/hooks click in `Edit` and scroll down to `Recent Deliveries` to select the Payload json request (click in `...`)

* Save a json payload under `branch-protector/test/test-payload-creation.json` with the name test-payload-creation.json, make sure this payload was generated due to repository **creation**.
* Save a json payload under `branch-protector/test/test-payload-deletion.json` with the name test-payload-deletion.json, make sure this payload was generated due to repository **deletion**.


First open a terminal and run the flask application

```
cd app-branch-protector
flask run
```

Open a second terminal and test branch-protector to simulate receiving the payload json post for GitHub due to a repository creation.
We should receive http 201 

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
