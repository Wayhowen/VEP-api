# Django VEP API

Django API for VEP

## Initial Setup
All commands should be used from the project root directory

1.) Launch the database using command: 
`docker-compose up db`

2.) Run migrations by using command:
`docker-compose up setup-api`

3.) Copy the key from between the quotation marks, and paste it into the 
`api_internal/settings/base` to the `API_AUTHORIZATION_HEADER` settings as a value in the following
format: `"Api-Key [THE_KEY_PRODUCED]"`

## Running:
### Using docker-compose:
The project can be run by using a single command in the root directory:  
`docker-compose up api-external rabbit worker`


# Project Structure

The project structure is described in more detail in the Design Section of Project report.

The main parts of the project are `api_external` which is sometimes referred to as the `REST API` 
in the report, and `api_internal` which is sometimes referred to as the `worker`.

The files in the root directory are used to configure docker, prospector and git.

# Data folder

The data folder contains additional data such as postman collections used for manual testing or the
data from sensors gathered throught the project.