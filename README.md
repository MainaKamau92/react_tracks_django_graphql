# Tracks Api
[![Build Status](https://travis-ci.com/MainaKamau92/udemy_graphene_project.svg?branch=master)](https://travis-ci.com/MainaKamau92/udemy_graphene_project)
[![Coverage Status](https://coveralls.io/repos/github/MainaKamau92/udemy_graphene_project/badge.svg?branch=master)](https://coveralls.io/github/MainaKamau92/udemy_graphene_project?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/42b13652f1aeb8c4e33f/maintainability)](https://codeclimate.com/github/MainaKamau92/udemy_graphene_project/maintainability)

# Project Title
## Tracks Django GraphQL Api Project 


# Project Overview
The Tracks project is a graphql api that enables users to create their favorite tracks and share them where their friends can like them.
# Prerequisites
For the web application to run locally a few requirements are necessary:
* Python 3 or newer
* virtualenv (For creating virtual environments and installing modules)
* All the listed dependencies in the **requirements.txt** file
* Git 


## Getting Started
1.  Run the following command from your git command line tool

    * `git clone https://github.com/MainaKamau92/udemy_graphene_project.git`

    >> The command clones a local copy of the project folder on your local machine
2. Navigate into the folder that has been created and create a virtual environment and activate the virtual environment by running:
    * `virtualenv venv`

 >> Activate the virtual environment by keying on a unix based system `source venv/bin/activate`

3. Run the migrations command to setup the database tables
    * `python3 manage.py makemigrations` (this command should create a migrations folder)
    * `python3 manage.py migrate`


8. Run the `python3 manage.py runserver` command to start the application(it should ideally be served on your local address(`127.0.0.1:8000`) on port 8000)
9. You should get this response on running the application
    ```
    Performing system checks...

    System check identified no issues (0 silenced).
    March 19, 2019 - 06:52:52
    Django version 2.1.7, using settings 'django_rest_api.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
    ```



## Working routes summary

* You should have a single api endpoint that is `http://127.0.0.1:8000/tracks/`

## Running Queries on the single api endpoint

* Creating a user

```
mutation {
  createUser(email:"jackdoe@test.com", password:"jackdoe123", username:"jackdoe"){
    user {
      id
      dateJoined
      email
    }
  }
}
```
* Accessing authorization token
>>> Put the authorization token in the Headers in the `Authorization` section preeceded by `JWT`.
i.e, `Authorization JWT token-of-random-string`

```
mutation {
  tokenAuth(username:"jackdoe", password:"jackdoe123"){
    token
  }
}
```

* Creating track

```
mutation {
  createTrack(title:"Not Afraid", description:"I am not afraid", url:"http://notafraid.com"){
    track{
      id
      description
    }
  }
}
```
* Updating track
```
mutation {
  updateTrack(title:"Not Afraid", description:"Afraid description", url:"http://notafraid.com", trackId: 1){
    track{
      id
      title
      url
      description
    }
  }
}
```
* Deleting  a track

```
mutation {
  deleteTrack(trackId: 1){
    trackId
  }
}
```

* Retrieving all tracks

```
{
  tracks{
    id
    title
    postedBy{
      id
      username
      email
    }
    likes{
      id
      track
    }
  }
}
```
* Searching for a track by title

```
{
  tracks(search: "Not afraid"){
    id
    title
    description
    url
  }
}
```
* Liking a track
```
mutation {
  createLike(trackId: 1){
    track {
      id
      title
      description
      url
    }
    user {
      id
      username
      email
    }
  }
}
```
* Retrieving all likes on all tracks
>>> Note: Individual likes on tracks can be retrieved by retrieving a single track and adding a likes field to the response 

```
{
  likes{
    id
    user {
      username
    }
    track {
      title
    }
  }
}
```



## Running the tests

In order to run the tests:
Having navigated to the folder with the manage.py run:
* `python3 manage.py test`
## Hosted on heroku
* [tracks_api](https://djangographene.herokuapp.com/tracks/)
## Build with
# ![Graphene Logo](http://graphene-python.org/favicon.png) Graphene-Django
