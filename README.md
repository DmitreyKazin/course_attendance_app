# Course Attendance Application
This application allows to manage and monitor student attendance in webex meetings.
- Flask is used for the web application.
- Jinja2 is used as a template wraper for html pages.
- MySQL was chosen to be the database provider.
- Docker-compose is used to run the application and the database seperatly within containers.
- Jenkins is used as CI/CD pipeline. The pipeline is clons GitHub repository, builds an Image, pushes it to DockerHub, cleans up memory, and sends email at the end.

For more details, watch the video: [click here](https://vimeo.com/756572554#t=67)
## Application Routes

- **"/"** --> Main route, shows the managable table called "Stable Table".
- **"/temp"** --> Shows the summary generated from the CSV files, with attendance.py script.
- **"/all"** --> Shows a table with student name, and his total minutes time for every meeting.
- **"/add_student"** --> Add a new student to "Stable Table".
- **"/edit/<name>"** --> Edit a record for specific student in "Stable Table".
- **"/delete/<name>"** --> Delere a record for specific student in "Stable Table".

## Installation

- Instal Docker, and Docker-Compose on your operating system, here are the installation links:

| Tool | Link   
| :---:   | :---: 
| Docker | [click here](https://docs.docker.com/get-docker/)   
| Docker-Compose | [click here](https://docs.docker.com/compose/install/)
> **_NOTE:_**  Docker-Compose is pre-installed in Win/Mac OS after installing Docker, but in Linux OS you'll have to install Docker-Compose seperatly .

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

## Run The Application

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
