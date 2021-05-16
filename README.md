# Django VEP API

Django API for VEP

## Initial Setup
All commands should be used from the project root directory

1.) Launch the database using command 
`docker-compose up db` and wait for the database to start.

2.) Run migrations by using command in a separate console window:
`docker-compose up setup-api` and wait for them to finish

3.) Copy the key from between the quotation marks, and paste it into the 
`api_internal/settings/base` to the `API_AUTHORIZATION_HEADER` settings as a value in the following
format: `"Api-Key [THE_KEY_PRODUCED]"`

## Running:
### Using docker-compose:
The project can be run by using a single command in the root directory:  
`docker-compose up api-external rabbit worker` and the API should be available at:
http://0.0.0.0:8000/


# Project Structure

The project structure is described in more detail in the `2.2 Detailed Design` section of project
report.

The main parts of the project are `api_external` which is sometimes referred to as the `REST API` 
in the report, and `api_internal` which is sometimes referred to as the `worker`.

The files in the root directory are used to configure docker, prospector and git.

# Data folder

The data folder contains additional data gathered and used throughout the project:
- postman: collections which can be used to reproduce the manual tests that I have created
- sensor_data: folder with data gathered using the VEP app, this data can be used to check if the
program is working
- data_with_videos: examples of different types of gait mentioned in the report and data gathered 
for those walks
- old_arshads_code: folder with the Arshad's code before refactoring, just for reference