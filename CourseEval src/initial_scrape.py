import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote

# 1. Load the page
url = "https://asen-jhu.evaluationkit.com/Report/Public/Results?Course=functional+programming&Instructor=&Search=true"
session = requests.Session()
response = session.get(url)
print(response.text)

# 2. Parse HTML and extract all buttons
soup = BeautifulSoup(response.text, "html.parser")
pdf_buttons = soup.find_all("a", class_="sr-pdf")

# 3. Build and download each PDF
for i, button in enumerate(pdf_buttons, start=1):
    print(button)
    id0 = button.get("data-id0")
    id1 = button.get("data-id1")
    id2 = button.get("data-id2")
    id3 = button.get("data-id3")

    # Clean/Decode the values
    id1 = unquote(id1)
    id2 = unquote(id2)
    id3 = unquote(id3)

    # Build the URL
    pdf_url = f"https://asen-jhu.evaluationkit.com/Reports/SRPdf.aspx?{id0},{id1},{id2},{id3}"
    print(f"[+] Downloading PDF #{i} from {pdf_url}")

    # Download and save
    pdf_resp = session.get(pdf_url)
    with open(f"report_{i}.pdf", "wb") as f:
        f.write(pdf_resp.content)

print("✅ All PDFs downloaded!")
