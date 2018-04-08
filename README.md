# gameAttitudesApp Intro
## To install
I use docker(https://www.docker.com/community-edition) to build my app, so please download docker at first. 
- Input `docker-compose build` in home directory of my application in the terminal. 
- Then use `docker-compose up` to run the app, and you will see a web page(localhost:5000) pumps up. 
- Post JSON data {"keyword": "nintendo"}/{"keyword": "playstation"}/{"keyword": "xbox"} to URL: localhost:5000/keyword to assign the keyword for tracking, but you need to restart the application after posting a new keyword data (`docker-compose stop` then `docker-compose up`)