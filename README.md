# This is an example api for a NLP model deployment

## API


Firstly check if your docker daemon is running and if not run it:

$ sudo dockerd

Then to build the docker image use command below inside api_dir directory (..path to/nlp_app/api_dir):

$ docker build -t nlp_api .

Then move your output directory contents with your model to api_dir/api/output10k or just download my pretrained Modern Talking lyrics generation weights at: https://drive.google.com/open?id=1MDFcUF7vylJCvoIHMv4AtP9Xw_-KNvXl

Then in the same directory you've built docker image use this to run the api (..path to/nlp_app/api_dir):

$ docker run -p 80:80 nlp_api

Check if api is running by going to:

http://localhost/generator?text=who%20am%20I?

wait a bit and congrats! You should get a json response with lyrics.

Change the part after ?text= to your preffered promt like http://localhost/generator?text=my%20lyrics%20input

Generate lyrics using your new API.

## APP

You need to install requirements in app_dir/requiremnts.txt either using a seperate pipenv, docker image or just straight with pip if you choose so. I use pipenv and suggest you do the same. Or conda enviroment.

Afterwards, just enable the newly installed enviroment and run app.py:

$ python app.py

You should see a link in the terminal: http://127.0.0.1:8050/

Open it and congrats!! you are in
