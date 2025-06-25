# Course Evaluation Screener Integration with Semester.ly

## Overview

Hi, and thank you for your interest in contributing to the course evaluation screener, specifically the portion that is going to be integrated into Semester.ly.

We're currently running this project asynchronously, where anyone can work on anything, and changes will be applied to the main branch through pull requests.

Our main goal right now is to develop a robust API to provide various metrics (for example, the difficulty of a course) based on the data we collect from the university though the course evaluations.

If you have any questions, feel free to email us at <jhuacmofficers@gmail.com>

## Current State & Progress

### Extraction and Parsing of Course Evaluation Documents

Currently, this repository contains working code to extract and parse course evaluation documents from the university. However, this code is fragmented and requires manual operation (as seen in the readme) to both extract and parse. We want to be able to have a simple process for collecting all the historical course evaluation data. However, it is possible to do this with a bit of effort manually.

The bigger issue is maintenance. New course evaluation data is released every semester, and we need to have a sustainable method for collecting only the new data every semester. Preferably this is automated, since a lack of ease in maintenance caused a similar project to this be discontinued.

In addition, we have only collected the data for one course, EN.601.464 Computer Vision, and this has acted as our test case to develop the API.

### The API

The backend api is far from complete. As a matter of fact, it is barebones right now. There is only structure. It currently uses Next.js and the my-app/src/app/api/route routing. Since this will be our only interface to semester.ly (as well as a possible future custom frontend), our plan is to make it quite good, and provide info. 

The API should get data from the database (eventually a precomputed version, )

The database being used currently is a PostGres 17. In order to work with the database, you'll need the Environmental Variables

We currently need to increase the number of API calls we support (use your imagination to see what you would like to see), as well improve error handling, among other things.

### Future Proofing this Project

The previous version of this project died due to lack of maintainability and loss of interest because it was not automated. We hope to be able to solve this problem after a basic verison of this project is developed.

## Setup

As far as I know, the only real setup is to create a .env file. There are four necessary variables, please email the officers for them.

CURRENTJHUSSOUSERNAME = 'VALID_JHU_EMAIL'
CURRENTJHUSSOPASSWORD = 'VALID_JHU_PASSWORD'

NEON_PASSWORD = 'PASSWORD'
NEON_HOST = 'HOSTNAME'
