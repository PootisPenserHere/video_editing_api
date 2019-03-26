[![Build Status](https://travis-ci.org/PootisPenserHere/video_editing_api.svg?branch=master)](https://travis-ci.org/PootisPenserHere/video_editing_api)

# Video editing api

## Table of content
1. [About the project](#about-the-project)
2. [Running the project](#running-the-project)
    1. [Upstream docker image](#upstream-docker-image)
    2. [Development mode](#development-mode)
3. [Services](#services)
    1. [Uploading videos](#uploading-videos)
    2. [Cutting the video](#cutting the video)
    3. [Lowering the volume](#lowering the volume)
    4. [Resize clip](#resize clip)
    5. [Retriving a video](#retriving a video)

### About the project
The objective of this project is to create an easy to use and portable service to quickly do basic edits to videos on the go.

With each action a new file with a randomized name will be created in the **./videos** directory inside the project, the reason to keep each version is to provide an easy to track progress and a way to restore to a previous point in history.

### Running the project
The project has been adapted to run within a docker container and may be pulled from the docker registry or built with docker-compose in development mode.

#### Upstream docker image
```bash
sudo docker pull jpdaramburos/video_editing_api:latest
sudo docker run -p 8080:5000 -v /root/video_api:/code/videos -d jpdaramburos/video_editing_api:latest
```

This will  create a volume mapped to the **/root/video_api** dir where the different videos and clips will be stored.

#### Development mode
Running the container
```bash
sudo docker-compose up --build -d
```

To stop the containers and dicard the images
```bash
sudo docker-compose down --rmi all -v
```

## To run the docker container
```sh
docker-compose up --build -d
```

### Services
Each Interaction  with the api that peform operations on a video or uploads new content will result in a new file being created with a random name, yielding a response as follows:
```json
{
  "message": "31O9V0BVAVLWPA1LMLYR.mp4", 
  "status": "success"
}
```

#### Uploading videos
Videos are uploaded with a **POST** request to the endpoint
```bash
localhost:8080/upload
```

Note: the following header will be necessary:
```
Content-Type multipart/form-data
```

Alternatively a template allowing manual upload of files can be rendered through the same endpoint with a verb **GET**

#### Cutting the video
A clip may be created making a **GET** request to the endpoint
```
localhost:8080/cut/<filename>/start/<start>/end/<end>
``` 

Where **filename** is the full name with extension of a file that has already been uploaded or created in a previous step.

**start** and **end** are integer values representing the second of the origin video where the clip will start and the second where it'll end, respectively.

#### Lowering the volume
Due to limitations the volume may only be lowered, this can be done with a **GET** request to the endpoint
```
localhost:8080/volume/<filename>/<volume>
```

Where **filename** is the full name with extension of a file that has already been uploaded or created in a previous step.

The volume setting is an integer between 0 and 10 where 10 is the current value, being the highest setting.

#### Resize clip
Videos may be resized with the endpoint
```
localhost:8080/resize/<filename>/width/<width>/height/<height>
```

Where **width** and **height** are integer values defining the dimenions of the new clip.

#### Retriving a video
The endpoint **/retrieve** when called with a **GET** request returns the chosen video with the appropriate headers.
```
localhost:8080/retrieve/<filename>
```
Where **filename** is the full name with extension of a file that has already been uploaded or created in a previous step.
