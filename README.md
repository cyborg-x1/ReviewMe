# ReviewMe
A tool for github to check where the user was mentioned and needs to review pull requests


Required settings file in ~/.reviewMe/settings.yaml:
```
repos:
  YOURORG1: [REPO0, REPO1, REPO2]
  YOURORG2: [REPO3]
update_rate: 10
username: YOURUSERNAME
working_days: [0, 1, 2, 3, 4]
working_hours: [6, 20]
```

* **username** Your username on github
* **repos** Array of your organisations with the repos you want to watch
* **updaterate** update rate when running (in minutes)
* **working_days** days you work starting with monday on 0 will not start on other days
* **working_hours** start-end - will not start outside this time



if it does not start add an empty data.yaml into the directory too.
