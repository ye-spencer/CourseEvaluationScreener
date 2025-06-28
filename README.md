# JHU ACM Course Evaluation Project

## Overview

This project scrapes and analyzes course evaluation data from Johns Hopkins University. It downloads evaluation data for specified courses, processes the JSON files, and stores the results in a PostgreSQL database for further analysis. The data includes metrics such as teaching effectiveness, course quality, workload, and other student feedback metrics.

## Contributors

- Spencer Y.
- Tianji L.
- Johnny S.

## Known Issues

### Course Name Subsets

Some courses have names that are subsets of each other (e.g., "Operating Systems" and "Advanced Operating Systems"). When downloading data for "Operating Systems," the system also downloads data for "Advanced Operating Systems."

## Roadmap

### Data Collection Expansion

Currently, data collection is limited to manually collected courses from the Computer Science department. Future development will expand to all departments.

### API Development

Data is currently stored in the database without a presentation layer. Development of an API/backend is planned to analyze and present the data.

## Proposed Enhancements

### Course Search by Number

Since classes have had variable course numbers and course names, we should group by course number instead of course name, as course numbers are the Registrar's primary method of differentiating classes.

### Schedule Comparison Tool

Implement functionality to compare two schedules based on difficulty, workload, and other metrics.

## Usage Guide

This guide walks you through the process of converting a class list to database-stored data.

### Step 1: Download PDFs

1. Create a `.env` file with valid JHU SSO credentials:
   ```
   CURRENTJHUSSOUSERNAME=your_username
   CURRENTJHUSSOPASSWORD=your_password
   ```

2. Run the scraper:
   ```bash
   python login_scraper.py --courses <filename.txt>
   ```
   
   Where `filename.txt` contains course names (one per line) to download. This opens a Selenium-driven Chrome browser and downloads files to `course pdfs/filename/` by default.

### Step 2: Extract Data from PDFs

```bash
python extract_pdf.py --directory <pdf_directory>
```

Where `pdf_directory` is the directory containing the PDFs to parse. Intermediate JSON files are saved to `results/pdf_directory` by default.

### Step 3: Upload Data to Database

1. Add database credentials to your `.env` file:
   ```
   NEON_HOST=your_host
   NEON_PASSWORD=your_password
   ```

2. Upload the processed data:
   ```bash
   python post_to_database.py --directory <json_directory>
   ```
   
   Where `json_directory` contains the JSON files of processed course evaluations to insert into the database.
