import pdfplumber
import re
import argparse
import json
import os

def extract_info(text):
    fields = {
        "Term": None,
        "Course Number": None,
        "Course Name": None,
        "Instructor": None,
        "Quality Mean": None,
        "Quality Responses": 0,
        "Teaching Effectiveness Mean": None,
        "Teaching Effectiveness Responses": 0,
        "Intellectual Challenge Mean": None,
        "Intellectual Challenge Responses": 0,
        "TA Evaluation Mean": None,
        "TA Evaluation Responses": 0,
        "Feedback Usefulness Mean": None,
        "Feedback Usefulness Responses": 0,
        "Workload Mean": None,
        "Workload Responses": 0,
    }

    term_match = re.search(r"(\d{4}) (Spring|Fall|Summer)", text)
    if term_match:
        fields["Term"] = f"{term_match.group(2)} {term_match.group(1)}"

    course_match = re.search(r"Course:\s*((EN|AS)\.\d+\.\d+\.\d+\.\w+)\s*:\s*(.+?)\s*\n", text, re.DOTALL)
    if course_match:
        fields["Course Number"] = course_match.group(1)
        fields["Course Name"] = course_match.group(3)

    instructor_match = re.search(r"Instructor:\s*(.*)", text)
    if instructor_match:
        fields["Instructor"] = instructor_match.group(1).strip()

    blocks_ids = {
        "1 - The overall quality of this course is:" : "Quality",
        "2 - The instructor's teaching effectiveness is:" : "Teaching Effectiveness",
        "3 - The intellectual challenge of this course is:" : "Intellectual Challenge",
        "4 - The teaching assistant for this course is:" : "TA Evaluation",
        "6 - Feedback on my work for this course is useful:" : "Feedback Usefulness",
        "7 - Compared to other Hopkins courses at this level, the workload for this course is:" : "Workload"
    }

    blocks = re.split(r"\n(?=\d+\s*-\s*)", text)
    for block in blocks:
        has_id = False
        for id, tag in blocks_ids.items():
            if block.strip().startswith(id):
                if (has_id):
                    print(f"Error: Multiple block IDs found in block: {block}")
                    continue
                match = re.search(r"Response Rate\s+Mean\s+STD\s+Median\s+(\d+/\d+).*?%.*?([0-9]+\.[0-9]+)", block, re.DOTALL)
                if not match:
                    print(f"Error: Could not extract block: {block}")
                    continue
                fields[tag + " Mean"] = match.group(2)
                fields[tag + " Responses"] = match.group(1).split("/")[0]
                has_id = True
    return fields

def get_info_pdfread(pdf_path):
    
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"
    return extract_info(full_text)


parser = argparse.ArgumentParser(description='Process PDF files in a directory')
parser.add_argument('directory', type=str, help='Directory containing PDF files to process')
args = parser.parse_args()

directory_add_path = args.directory.replace(" ", "_").replace("/", "-").replace(".", "")
if not os.path.exists(f"results/{directory_add_path}"):
    os.makedirs(f"results/{directory_add_path}")

for filename in os.listdir(args.directory):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(args.directory, filename)
        try:
            pdf_info = get_info_pdfread(pdf_path)
            with open(f"results/{directory_add_path}/{filename}.json", "w") as f:
                json.dump(pdf_info, f, indent=4)
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")



# Next Workflow
# Get results by PDFRead
# Get result by PDFScan
# Get result by trained transformer
# Other check results