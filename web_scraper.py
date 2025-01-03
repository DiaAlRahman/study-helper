import requests
from bs4 import BeautifulSoup
import os

# Base URL of the website
BASE_URL = "https://papers.gceguide.cc/a-levels/physics-(9702)/"


def fetch_page(url):
    """Fetch the HTML content of a given URL."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch {url}. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
    return None


def find_directory_link(base_url, year):
    """Find the link to the directory for the specified year."""
    html_content = fetch_page(base_url)
    if not html_content:
        return None

    soup = BeautifulSoup(html_content, 'html.parser')
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if str(year) in href:
            return base_url.rstrip('/') + '/' + href
    return None


def find_pdf_links(directory_url):
    """Find all PDF links in the specified directory."""
    directory_content = fetch_page(directory_url)
    if not directory_content:
        return []

    soup = BeautifulSoup(directory_content, 'html.parser')
    qp_links, ms_links = [], []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        split_href = href.split('_')
        if split_href[-1].endswith('.pdf'):
            if split_href[2] == 'qp':
                qp_links.append(directory_url.rstrip('/') + '/' + href)
            elif split_href[2] == 'ms':
                ms_links.append(directory_url.rstrip('/') + '/' + href)
    return qp_links, ms_links 


def download_pdfs(pdf_links, output_dir, isQP):
    """Download all PDFs from the list of links to the specified directory."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Create 'ms' and 'qp' inside output_dir
    subdirectory = 'qp' if isQP else 'ms'

    subdir_path = os.path.join(output_dir, subdirectory)
    os.makedirs(subdir_path, exist_ok=True)
    
    for pdf_link in pdf_links:
        pdf_name = pdf_link.split("/")[-1]
        pdf_path = os.path.join(subdir_path, pdf_name)
        try:
            pdf_response = requests.get(pdf_link)
            if pdf_response.status_code == 200:
                with open(pdf_path, 'wb') as pdf_file:
                    pdf_file.write(pdf_response.content)
                print(f"Downloaded: {pdf_name}")
            else:
                print(f"Failed to download: {pdf_name}. Status code: {pdf_response.status_code}")
        except requests.RequestException as e:
            print(f"Error downloading {pdf_link}: {e}")


def download_year_pdfs(year):
    """Main function to download all PDFs for a specified year."""
    print(f"Processing year {year}...")
    directory_link = find_directory_link(BASE_URL, year)
    if not directory_link:
        print(f"Failed to locate the directory for year {year}.")
        return

    print(f"Found directory link: {directory_link}")
    qp_links, ms_links = find_pdf_links(directory_link)

    if not qp_links or not ms_links:
        print(f"No PDF links found for year {year}.")
        return

    print(f"Found {len(qp_links)} qp links for year {year}.")
    print(f"Found {len(ms_links)} ms links for year {year}.")
    output_dir = f"{year}_pdfs"
    download_pdfs(qp_links, output_dir, isQP=True)
    download_pdfs(ms_links, output_dir, isQP=False)
    print(f"All downloads for year {year} are complete.")


START_YEAR, END_YEAR = 2022, 2024
download_year_pdfs(2023)