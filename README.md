# Course Attendance Application
This application allows to manage and monitor student attendance in webex meetings.
- Flask is used for the web application.
- Jinja2 is used as a template wraper for html pages.
- MySQL was chosen to be the database provider.
- Docker-compose is used to run the application and the database seperatly within containers.

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

**2) ".env"** will contain the bellow content:
```
DB_USER = root
DB_PASS = < same as "MYSQL_ROOT_PASSWORD" in "env/mysql.env" >
DB_NAME = < same as "MYSQL_DATABASE" in "env/mysql.env" >
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

## TO-DO

- **Application**:
  - Download the CSV files from an outside server using SFTP.
  - Add filter by date to "/all" route.
  - Display "Total Meetings Time" in "/" page.
  - Auto-fill the "Total_Percentage" column after filling the "Total_Min" column.

- **DevOps**:
  - Create Jenkins pipeline that will connect the app repository on github to Jenkins.
  - Run application on Kubernetes.
  - Create a pipeline that builds, tests, and deploys the application to Kubernetes.
  - Deploy to AWS.
