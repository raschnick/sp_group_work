# sp_group_work - coinfo
by Sascha, Simon and Nick

## Building a docker image from the Dockerfile
#### IMPORTANT: Make sure to overwrite the API_KEY values in the build-args!
```docker build --build-arg API_KEY_ARG=INSERT_VALUE --build-arg FOMO_API_KEY_ARG=INSERT_VALUE --tag sp-coinfo .```


## Local Setup Guide

###Installing the Dependencies
Create a virtual env and run:

```pip install -r requirements.txt```

### Running the App
The coinapi adn token fomo api keys are injected with environment variables, so make sure they are set when running it without a container! (env variable names: "API_KEY" & "FOMO_API_KEY)!

Run the app locally:

```python app.py```

Running the app in a container locally: (image must be built first, as seen above)

```docker run -d -p 5000:5000 sp-coinfo```

## AWS lightsail Setup Guide
#### IMPORTANT Prerequisite: an installed, configured AWS CLI & a docker image (as built above)

### Create a lightsail container service
```aws lightsail create-container-service --service-name sp-coinfo-service --power small --scale 1```

### Push your docker image to lightsail
```aws lightsail push-container-image --service-name sp-coinfo-service --label sp-coinfo --image sp-coinfo```

Update the flask.image property in the lightstail/container.json image reference from the output of this command!

### Deploy the container with the config to lightsail
```aws lightsail create-container-service-deployment --service-name sp-coinfo-service --containers file://lightsail/containers.json --public-endpoint file://lightsail/public-endpoint.json```

Copy the url out of the response of this comment, you will be able to reach it shortly!

### Check the status or get the endpoint url again
```aws lightsail get-container-services --service-name sp-coinfo-service```

### Delete your service (if needed)
```aws lightsail delete-container-service --service-name sp-coinfo-service```