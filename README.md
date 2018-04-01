![Build Status](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiQ3VEenczSjIrTFZVS2s0NThpRXlCZHFiMk8wcmkwZHE4enhVK2UyM1hDdGdydVNMS3dreUpSUGxtclU1Smphd0d6WFZUT1Q5Y3NTRUN4bGNqdzVtRmhZPSIsIml2UGFyYW1ldGVyU3BlYyI6IjBMQzlQMWFveXFZNmhZaEwiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)

# Video editing api
### A (WIP)flask implementation of the moviepy library.

## To run the docker container
```sh
docker-compose up --build -d
```

# Functionality
### With each operation a new verion of the video being handled is created and can be referenced by it's given name in a way that it'll allow to "revert" changes or create several lighter versions of a larger file

## Uploading ne videos
### Will save received files and assign them a randmoly generated name
```
localhost:8080/uploader
```

### Alternatively to consuming the endpoint programatically it's posible to use a crude form to manually upload files
```
localhost:8080/upload
```

## Extracting a clip from a video
### Will create a new clip and return its name in a json format
```
localhost:8080/cut/<fileName>/starting/<startTime>/ending/<endTime>
```

## Changing the volume settings
### This allows to lower or completly remove the sound from a clip, taking the setting in the form of an integer that ranges between 0 to 10 where 10 is the current volume
```
localhost:8080/volume/<fileName>/<newLevel>
```

## Viewing files
### Sends the required files from the storage to the browser to be displayed
```
localhost:8080/retrieve/<fileName>
```
