import os
import json
from dotenv import load_dotenv
import psycopg2
import argparse
load_dotenv()
password = os.getenv("NEON_PASSWORD")
host = os.getenv("NEON_HOST")

conn = psycopg2.connect(
    host=host,
    dbname="neondb",
    user="neondb_owner",
    password=password,
    port="5432",
    sslmode="require"
)


parser = argparse.ArgumentParser(description='Process json files in a directory')
parser.add_argument('--directory', type=str, help='Directory containing json files to put into the database')
args = parser.parse_args()

json_dir = args.directory

cursor = conn.cursor()

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