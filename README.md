# JHU ACM Course Evaluation Project

## Overview

This project scrapes and analyzes course evaluation data from Johns Hopkins University. It downloads evaluation data for specified courses, processes the JSON files, and stores the results in a PostgreSQL database for further analysis. The data includes metrics like teaching effectiveness, course quality, workload, and other student feedback metrics.

## Contributors

Spencer Y., Tianji L., Johnny S.

## Issues

### Course Name Subsets

Some courses have names that are subsets of each other (ex. "Operating Systems" and "Advanced Operating Systems"), so downloading for Operating Systems also downloads Advanced Operating Systems.

## Next Steps

### Scrape Data for all Departments

Currently, we are only able to collect data for manually collected courses for the computer science department.

### Create API/Backend to analize and present data

Data is currently stored, with nothing presenting it

### Integration into Semester.ly

## New Ideas

### Search by Course

As classes have had variable course numbers and course names, we should instead only group by course number, as that is likely the Registrar's way of differentiating classes, not course name

### Schedule comparisons

Given two schedules, compare difficulty, workload, etc.

## Tutorial

In order to go from a class list (compiled through your favorite method) to data in the database

### Downloading PDFs

Include a set of valid pair of JHU SSO sign on in a .env file, under CURRENTJHUSSOUSERNAME and CURRENTJHUSSOPASSWORD

Use `python login_scraper.py --courses <filename.txt>`, where each line in filename.txt is the name of a course you want to download for. This will open a Selenium-driven chrome browser.

Downloads the files into the folder `course pdfs/filename/` by default

### Extracting Data from PDFs

Use `python extract_pdf.py --directory <pdf_directory>`, where pdf_directory is the directory of the PDFs you want to parse

Downloads intermediate JSON files into the folder `results/pdf_directory` by default, with some edits to the raw pdf_directory to ensure safety.

### Posting Data to Database

Include a set of valid pair of database host and password in a .env file, under NEON_HOST and NEON_PASSWORD

Use `python post_to_database.py --directory <json_directory>` where <json_directory> contains JSON files of processed course evaluations to insert into the database.
