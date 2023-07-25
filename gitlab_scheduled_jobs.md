Create a folder for your script. Inside it you'll need:

main script python file (should be able to execute the command with python file.py)

any helper python files

requirements.txt (generated with pip freeze > requirements.txt)

.gitlab-ci.yml file (the hardest part of this whole process and its not that hard)

Once you have this setup go ahead and git init. You'll need a gitlab account so go ahead and make one. Create your first project and upload it to your gitlab account.

You'll need a few things in your .gitlab-ci.yml file. this file contains instructions for Gitlab to run your script.

image: "python:3.9"
before_script:
- python --version
- python -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
stages:
- Main
main:
stage: Main
script:
- python file.py

At the top you need to choose a docker image to use (this is the only docker you'll use)

You'll need to tell Gitlab what to do before executing the script, here we'll create a virtual environment and install packages.

Next we'll define what stages there are to building your script. We only need one stage to run the script.

Push this up to gitlab and you'll see the pipeline run under "CI/CD" -> "Pipeline", you can click on the job to see the status.

Once your pipeline runs successfully you can go to "CI/CD" -> "Schedules" to create a new schedule. You'll need to use cron syntax to create the schedule so checkout crontab.guru if you are not familiar.

Gitlab has great documentation and this would cost you nothing for a small script run daily.