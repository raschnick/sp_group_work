FROM python:3.10

EXPOSE 5000/tcp

WORKDIR /app

ARG API_KEY_ARG="has to be set by in the docker build"
ENV API_KEY=$API_KEY_ARG

ARG FOMO_API_KEY_ARG="has to be set by in the docker build"
ENV FOMO_API_KEY=$FOMO_API_KEY_ARG

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "./app.py" ]