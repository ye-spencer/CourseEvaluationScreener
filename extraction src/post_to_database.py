"""
post_to_database.py

A script to insert course evaluation data from JSON files into a PostgreSQL database.
Processes JSON files containing extracted course evaluation data and stores them in a structured database.

Usage:
    python post_to_database.py --directory <json_directory>
    
    where <json_directory> contains JSON files of processed course evaluations to insert into the database.
    
    Environment variables required:
    - NEON_PASSWORD: Database password
    - NEON_HOST: Database host
"""

import os
import json
from dotenv import load_dotenv
import psycopg2
import argparse

### Load environment variables ###
load_dotenv()
postgres_url = os.getenv("NEON_CONNECTION")

### Connect to the database ###
conn = psycopg2.connect(postgres_url)

### Parse command line arguments ###
parser = argparse.ArgumentParser(description='Process json files in a directory')
parser.add_argument('--directory', type=str, help='Directory containing json files to put into the database')
args = parser.parse_args()

json_dir = args.directory
cursor = conn.cursor()

### Process each JSON file in the directory ###
for file in os.listdir(json_dir):
    if file.endswith('.json'):
        with open(os.path.join(json_dir, file), "r") as f:
            data = json.load(f)
            try:
                values = list(data.values())
                to_insert = values[0:4] + [float(x) for x in values[4::2]] + [int(x) for x in values[5::2]]
                cursor.execute("""INSERT INTO "cs-trial-courses"."course_evaluations" (
                    term, course_number, course_name, instructor,
                    quality_mean, teaching_effectiveness_mean, intellectual_challenge_mean, 
                    ta_evaluation_mean, feedback_usefulness_mean, workload_mean,
                    quality_responses, teaching_effectiveness_responses, intellectual_challenge_responses,
                    ta_evaluation_responses, feedback_usefulness_responses, workload_responses
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", to_insert)
                conn.commit()
                print(f"Inserted {file}")
            except Exception as e:
                conn.rollback()
                print(f"Failed on {file}: {e}")

cursor.close()
conn.close()