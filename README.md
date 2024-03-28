# Backend for ecommerce website

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
- [Launch](#installation)

## Overview

This repository contains the backend implementation for a website built using Python Django and Django Rest Framework (
DRF). The backend is responsible for handling data storage, retrieval, and processing for the website.

## Getting started

Before you begin, ensure you have met the following requirements:

- You have [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed on your
  machine.

Make sure to set the required environment variables in the .env file before running the project(Note, that
`ALLOWED_HOSTS` accepts comma separated values).
Refer to the .env.example file for a template of the required variables.

## Launch

After you create .env file and set required variables inside of it, run the following command in your terminal

1. **Run Docker**:
   - Execute the following command in your terminal:

     ```bash
     docker-compose up -d --build
     ```

   - Use `-d` flag for detached mode.
   - `--build` flag ensures docker images are built before container startup.

2. **Stop the Project**:
   - To stop the project and containers, run:

     ```bash
     docker-compose down
     ```

   - Execute this command in the terminal where `docker-compose` is running.
   - This gracefully shuts down the containers.

3. **Create Superuser**:
   - After successful launch, run:

     ```bash
     docker-compose exec web python3 manage.py createsuperuser --settings=ecommerce_backend.settings.local
     ```
4. **Access Admin Panel**:
   - Visit the admin panel by entering one of the hostnames declared in the `.env` `ALLOWED_HOSTS` variable followed by `/admin/`.
   - Log in with the credentials you provided while creating the superuser.