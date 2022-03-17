# sp_group_work

## Setup Guide
Create a virtual env and run:

```pip install -r requirements.txt```

## Build docker image from Dockerfile

```docker build --tag sp-group-work .```

## Running the App:
Running the app locally:

```python app.py```

Running the app in a container: (image must be built first)
```docker run -d -p 5000:5000 sp-group-work```
