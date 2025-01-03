import requests
from bs4 import BeautifulSoup
import os

# Base URL of the website
base_url = "https://papers.gceguide.cc/a-levels/physics-(9702)/"

# Step 1: Fetch the base webpage
response = requests.get(base_url)
if response.status_code == 200:
    html_content = response.text
else:
    print("Failed to fetch the base webpage.")
    exit()

# Step 2: Parse the base page to find the 2022 directory link
soup = BeautifulSoup(html_content, 'html.parser')
directory_link = None

for a_tag in soup.find_all('a', href=True):
    href = a_tag['href']
    if "2022" in href:  # Find the link for the 2022 directory
        directory_link = base_url + '/' + href
        break

if not directory_link:
    print("Failed to locate the 2022 directory.")
    exit()

print(f"Found 2022 directory link: {directory_link}")

# Step 3: Fetch the 2022 directory page
response = requests.get(directory_link)
if response.status_code == 200:
    directory_content = response.text
else:
    print("Failed to fetch the 2022 directory webpage.")
    exit()

# Step 4: Parse the 2022 directory page to find PDF links
directory_soup = BeautifulSoup(directory_content, 'html.parser')
pdf_links = []

for a_tag in directory_soup.find_all('a', href=True):
    href = a_tag['href']
    if href.endswith('.pdf'):  # Look for PDF files
        pdf_links.append(directory_link + '/' + href)

print(pdf_links)

if not pdf_links:
    print("No PDF links found in the 2022 directory.")
    exit()

# Step 5: Download each PDF
output_dir = "2022_pdfs"
os.makedirs(output_dir, exist_ok=True)  # Create directory to save PDFs

for pdf_link in pdf_links:
    pdf_name = pdf_link.split("/")[-1]
    pdf_path = os.path.join(output_dir, pdf_name)

    # Download the PDF
    pdf_response = requests.get(pdf_link)
    if pdf_response.status_code == 200:
        with open(pdf_path, 'wb') as pdf_file:
            pdf_file.write(pdf_response.content)
        print(f"Downloaded: {pdf_name}")
    else:
        print(f"Failed to download: {pdf_name}")

print("All PDF downloads are complete.")
