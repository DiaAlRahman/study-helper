import pdfplumber
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import os
import fitz  # PyMuPDF

from question_bounds import QuestionBounds

QUESTION_END_MARK = 'D'


class Document:
    def __init__(self , paper_year , year_variant, subject_code, question_session , paper_type, paper_no , total_pages , pdf_content):
        self.paper_year = paper_year
        self.year_variant = year_variant
        self.subject_code = subject_code
        self.paper_session = question_session
        self.paper_type = paper_type
        self.paper_no = paper_no
        self.main_identifier = f'{self.subject_code}_{self.paper_session}{self.paper_year}_{self.paper_type}_{self.paper_no}{self.year_variant}'
        self.total_pages = total_pages
        self.pdf_content = pdf_content


class PDFExtraction:
    def __init__(self, input_pdf_path, output_folder):
        self.input_pdf_path = input_pdf_path
        self.output_folder = output_folder
        self.list_of_questions = []

    def capture_questions_from_pdf(self , start_page , end_page , start_question):
        with pdfplumber.open(self.input_pdf_path) as pdf:
            questions_in_previous_page = 0
            for page_no in range(start_page, end_page):
                page = pdf.pages[page_no]
                page_width = page.width
                page_height = page.height

                words = page.extract_words()
                print(f"Processing page {page_no + 1} with {len(words)} words...")

                # Capture questions on the current page
                self.capture_questions(words, start_question, page_no, page_width, page_height)

                # Update the start question number for the next page
                start_question += len(self.list_of_questions) - questions_in_previous_page
                questions_in_previous_page = len(self.list_of_questions)

    def capture_questions(self, list_of_words, start_question, page_no, page_width, page_height):
        is_capturing_question = True
        is_question_mark_found = False
        current_question = start_question

        for block in list_of_words:
            try:
                if is_capturing_question and int(block['text']) == current_question:
                    x0, top = block["x0"], block["top"]
                    if len(self.list_of_questions) > 0 and not self.list_of_questions[-1].is_last_question:
                        self.list_of_questions[-1].set_x_end(page_width, top)

                    self.list_of_questions.append(QuestionBounds(0, top, page_no, current_question))
                    is_capturing_question = False
                    is_question_mark_found = False
                    current_question += 1
            except ValueError:
                continue

            # Detect question mark and question end marker
            if not is_question_mark_found and block['text'].endswith('?'):
                is_question_mark_found = True
            elif is_question_mark_found and block['text'] == QUESTION_END_MARK:
                is_question_mark_found = False
                is_capturing_question = True

        # Set the end for the last question on the page
        if self.list_of_questions:
            self.list_of_questions[-1].set_x_end(page_width, page_height)
            self.list_of_questions[-1].is_last_question = True

    def save_question_bounding_boxes(self):
        # Create the output folder if it doesn't exist
        os.makedirs(self.output_folder, exist_ok=True)

        pdf_document = fitz.open(self.input_pdf_path)

        for question in self.list_of_questions:
            page_no = question.page_no
            page = pdf_document.load_page(page_no)

            x0, y0 = question.cordStart
            x1, y1 = question.cordEnd

            rect = fitz.Rect(x0, y0, x1, y1)
            pix = page.get_pixmap(clip=rect, dpi=300)
            image_path = os.path.join(self.output_folder, f"question_{question.question_no}_page_{page_no + 1}.png")

            pix.save(image_path)
            print(f"Saved: {image_path}")

        pdf_document.close()


input_pdf_path = "example.pdf"
output_folder = "extracted_questions"

test = PDFExtraction(input_pdf_path , output_folder)
test.capture_questions_from_pdf(2 , 18 , 1)
test.save_question_bounding_boxes()

