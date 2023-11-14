# Backend for ecommerce website

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
- [Dependencies](#dependencies)
- [Installation](#installation)

## Overview

This repository contains the backend implementation for a website built using Python Django and Django Rest Framework (
DRF). The backend is responsible for handling data storage, retrieval, and processing for the website.

## Getting started

Before you begin, ensure you have met the following requirements:

- You have [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed on your
  machine.

Make sure to set the required environment variables in the .env file before running the project.
Refer to the .env.example file for a template of the required variables.

## Dependencies

## Installation

After you create .env file and set required variables inside of it, run the following command in your terminal

```docker-compose up -d --build```

- The `-d` flag used to run docker in detached mode so you can use your terminal
- The `--build` flag ensures that the images are built before starting the containers.

To stop the project and containers, press Ctrl+C in the terminal
or run `docker-compose down` where docker-compose is
running. This will gracefully shut down the containers.
