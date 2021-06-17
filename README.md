# bootcamp-students-unite

# Project Title

A short description about the project and/or client.

## Getting Started

Clone down the repository
Npm start

### Prerequisites

The things you need before installing the software.

- Code Editor
- Github Repo

# boot-camp-students-server

Back End Capstone

## To Run Locally

Clone down the directory
` git clone git@github.com:Younique98/bootcamp-students-unite-client.git`

Run the following commands to install pipenv and create a virtual environment.

    ```pip3 install --user pipx```
    ```pipx install pipenv ```
    ```pipenv shell```

Next, install these third-party packages

`pipenv install`

Load Fixtures

`python3 manage.py migrate`
`python3 manage.py loaddata bootcampgraduates`
`python3 manage.py loaddata groupprojects`
`python3 manage.py loaddata jobboards`
`python3 manage.py loaddata tokens`
`python3 manage.py loaddata users`

Then start the server

`python3 manage.py runserver`

URL

https://bootcamp-students-unite.herokuapp.com/

Description

Api for backend capstone

### Installation

A step by step guide that will tell you how to get the development environment up and running.

```
$ git clone ***
$ git checkout -b branchname
$ npm start
```

## Usage

A few examples of useful commands and/or tasks.

```
$ npm start
```

## Deployment

Additional notes on how to deploy this on a live or release system. Explaining the most important branches, what pipelines they trigger and how to update the database (if anything special).

### Server

- Live: MongoDB & AWS Cloud
- Development: localhost://3000

### Branches

- Main:
- Feature:
- Bugfix:
- etc...

## Additional Documentation and Acknowledgments

![Bootcamp Students Unite](https://user-images.githubusercontent.com/18708698/121244017-3e6b6b00-c853-11eb-8e4d-afe767744a38.png)
![Bootcamp Students Unite Wirefame](https://user-images.githubusercontent.com/18708698/121246667-44af1680-c856-11eb-93bf-3e0ba600f1e4.png)
