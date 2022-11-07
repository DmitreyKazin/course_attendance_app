# Course Attendance Application

This application allows to manage and monitor student attendance in webex meetings.
- Flask is used as the web application framework.
- Jinja2 is used as a template wraper for html pages.
- MySQL was chosen to be the database provider.
- Jenkins is used as CI/CD pipeline. 
- Docker-compose and K8s are used as Orchestration tools for docker containers. Choose one of them to run the application.

## Application Routes

- **"/"** --> Main route, shows the managable table called "Stable Table".
- **"/temp"** --> Shows the summary generated from the CSV files, with attendance.py script.
- **"/all"** --> Shows a table with student name, and his total minutes time for every meeting.
- **"/add_student"** --> Add a new student to "Stable Table".
- **"/edit/<name>"** --> Edit a record for specific student in "Stable Table".
- **"/delete/<name>"** --> Delere a record for specific student in "Stable Table".

For more details, watch the video: [click here](https://vimeo.com/756572554#t=67)

## CI/CD - Jenkins

To launch Jenkins, I used two AWS EC2 servers, both builded from Linux 2 AMI. One of the servers is acting as the master, and the second one is a slave.
The CI/CD pipeline is running on jenkins slave (test machine), and here is the breakdown for the steps:
- Git checkout --> Clone GitHub rpeository.
- Attach Env Files --> Copyies environment files into the workspace.
- Health Check --> Gets HTTP response code for main application route.
- Build Images --> Two docker images are builded, one with "latest" tag and the second with job build number as a tag.
- Push to DockerHub --> Pushes both images into DockerHub repository.
- Deploy to Staging --> by using 'deploy.sh' bash script, the new version is deployed to the staging server (AES EC2 server).
- Deploy to Production --> By using 'deploy.sh' bash script, the new version is deployed to the production server (AWS EC2 server).

## Installation For Docker Compose

- Instal Docker, and Docker-Compose on your operating system, here are the installation links:

| Tool | Link   
| :---:   | :---: 
| Docker | [click here](https://docs.docker.com/get-docker/)   
| Docker-Compose | [click here](https://docs.docker.com/compose/install/)
> **_NOTE:_**  Docker-Compose is pre-installed in Win/Mac OS after installing Docker, but in Linux OS you'll have to install Docker-Compose seperatly.

- Before you run the application, you will need to add enviorment variables files, as mentioned below:

**1) "env/mysql.env"**
```
MYSQL_ROOT_PASSWORD=< YOUR_ROOT_PASSWORD >
MYSQL_DATABASE=< YOUR_DB_NAME >
```

**2) ".env"**
```
DB_USER = root
DB_PASS = < same as "MYSQL_ROOT_PASSWORD" in "env/mysql.env" >
DB_NAME = < same as "MYSQL_DATABASE" in "env/mysql.env" >
RMT_HOST = < remote machine address >
RMT_USER = < user in RMT_HOST >
RMT_PASSWD = < password in RMT_USER >
```

## Run The Application With Docker Compose

As I used Docker-Compose, you won't need to download any dependecies, except those mentioned in "Installation" section.

- **Run the application:**
```sh
# run the following command from the project directory
# you can use "-d" flag to run in de-attached mode
docker-compose up
```
- **Stop the application:**
```sh
# run the following command from the project directory
docker-compose down
```
> **_NOTE:_**  You can run the application with K8s as well, as described in kubernetes directory.
