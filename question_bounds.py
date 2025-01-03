class QuestionBounds:
    def __init__(self, xStart, yStart, page_no, question_no):
        self.cordStart = (xStart, yStart)
        self.cordEnd = None
        self.end_of_question = False
        self.page_no = page_no
        self.question_no = question_no
        self.is_last_question = False

    def set_x_end(self, xEnd, yEnd):
        self.cordEnd = (xEnd, yEnd)

    def set_end_of_question(self, end_of_question):
        self.end_of_question = end_of_question

    def __str__(self):
        return (f'question no {self.question_no} page no {self.page_no} start coordinates {self.cordStart} end coordinates {self.cordEnd}')
