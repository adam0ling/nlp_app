# This is an example api for a NLP model deployment

## Local

### API


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

### APP

You need to install requirements in app_dir/requiremnts.txt either using a seperate pipenv, docker image or just straight with pip if you choose so. I use pipenv and suggest you do the same. Or conda enviroment.

Afterwards, just enable the newly installed enviroment and run app.py:

$ python app.py

You should see a link in the terminal: http://127.0.0.1:8050/

Open it and congrats!! you are in



## Deploying to GCloud

So, hopefully you have the model running with the app and api locally, but now you want to deploy it to the cloud. This guide will help you out with exactly that.

The guide is designed dor deploying to Google Cloud. You need to be registered to use it. Newly created accounts have $300 free credit. Also, you need to have Cloud SDK installed. To do that check: https://cloud.google.com/sdk/install 

1. Open your Google Cloud console: https://console.cloud.google.com/
2. Create new project (if you have a new account there should be a pop up, if not click on the project name in the top left corner)
3. Give your project a name and click create
4. Wait till you get a notification that your project has been successfuly created
5. Open up the project and in the GCloud menu (burger button at the top left corner) select Kubernetes Engine
6. Clusters window will open up. Wait till Kubernetes Engine API is enabled.
7. After the API is created switch to your terminal and change directory to where the API is, so:

$ cd /path_to/nlp_app/api_dir

8. Now we will follow google guide to upload our docker image to the GCloud just instead of their sample app we will use ours: https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app

$ gcloud components install kubectl

$ export PROJECT_ID=[PROJECT_ID]

Here your PROJECT_ID can be found clicking on the project name in the top left corner in the console and then you'll see the ID column. Copy that.

$ docker build -t gcr.io/${PROJECT_ID}/nlp-app:v1 .

Make sure docker daemon is running, if not $ sudo dockerd

Run [$ docker images] to verify that the image was built, you should see a line like this:

    gcr.io/nlp-test-273608/nlp-app       v1                  b372c66efdea        19 hours ago        4.64GB

Now we need to upload it to the Container Registry.

$ gcloud auth configure-docker

$ docker push gcr.io/${PROJECT_ID}/nlp-app:v1

Now the image is there. All we need is to deploy it in a cluster. To start with we are going to create a cluster.

$ gcloud config set project $PROJECT_ID

$ gcloud config set compute/zone [COMPUTE_ENGINE_ZONE] 

Here COMPUTE_ENGINE_ZONE needs to be set. I suggest: us-central1-c. All options can be seen here: https://cloud.google.com/compute/docs/regions-zones#available

$ gcloud container clusters create nlp-cluster --num-nodes=2

Check that cluster is created:

$ gcloud compute instances list

You should see something like this:

    NAME                                        ZONE           MACHINE_TYPE   PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP    STATUS
    gke-nlp-cluster-default-pool-d9408fb4-1pt1  us-central1-c  n1-standard-1               10.128.0.3   34.71.58.247   RUNNING
    gke-nlp-cluster-default-pool-d9408fb4-p67q  us-central1-c  n1-standard-1               10.128.0.2   34.66.234.161  RUNNING

Now we need to deploy our application (well, api):

$ kubectl create deployment nlp-web --image=gcr.io/${PROJECT_ID}/nlp-app:v1

Check if the pod is running. It takes around 3-4mins for it to start up

$ kubectl get pods

Now all we need to do is expose that API:

$ kubectl expose deployment nlp-web --type=LoadBalancer --port 80 --target-port 80

Check for the external IP and copy it:

$ kubectl get service

nlp-web      LoadBalancer   10.63.246.239   34.66.234.161   80:31372/TCP   65s

We are finished with the API deployment.

9. Now go to the app.py file in /path_to/nlp_app/app_dir and in the update_output callback (look at the very end) change:

url = 'http://0.0.0.0/generator?text='+value  # change to actual api ip

with

url = 'http://[EXTERNAL_IP]/generator?text='+value  # change to actual api ip

so in my case:

url = 'http://34.66.234.161/generator?text='+value  # change to actual api ip

Save the file and rename it to main.py

Delete the Pipfile.

10. Open up the project and in the GCloud menu (burger button at the top left corner) select App Engine
11. Got to the app directory in the terminal: 

$ cd ../app_dir/

12. Deploy the app:

$ gcloud app deploy

It takes a while so grab a coffee or tea.

13. Now at the App Engine dashboard you should see that the application is created click the finish up button. Select a region which should be the same region as your kubernetes cluster. As for framework select "Other".
14. App should be deployed by now. To open it:

$ gcloud app browse

Congrats! You're in. Type your starting lyrics and wait for monkeys to finish the job. Cyber monkeys I mean.

15. Don't forget to delete the project after you're donw ith it as leaving it online will incur charges. To do that simply click the burger buttton near your account avatar in the top right corner then Project Settings and then click SHUT DOWN. Type project ID in the box and SHUT DOWN again. All done. All charges should be stopped now.

# Doesn't work?

* Check that you renamed app.py to main.py
* Check that you've deleted Pipfile from app_dir
* Check that your API is working by going to http://[YOUR_API_EXTERNAL_API]/generator?text=lyrics or in my case http://34.66.234.161/generator?text=lyrics
* If all that fails just leave a comment on the youtube video or dm me through any social and I'll try to help you out.

