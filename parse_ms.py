# Extract the content of the PDF file and parse the question-key map
from PyPDF2 import PdfReader
import re

# Load the PDF
pdf_path = "9702_m17_ms_12.pdf"
reader = PdfReader(pdf_path)

# Extract text from the PDF
pdf_text = ""
for page in reader.pages:
    pdf_text += page.extract_text()

# Extract the question number and keys using regular expressions
# The table has a clear pattern: Question Number Key
pattern = r"(\d+)\s+([A-D])"
matches = re.findall(pattern, pdf_text)

# Convert the matches into a dictionary
question_key_map = {int(question): key for question, key in matches}

# print(question_key_map)
