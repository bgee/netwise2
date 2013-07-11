from openpyxl import load_workbook
import os
from docx import *



current_dir = os.path.dirname(os.path.abspath(__file__))

work_list = os.path.join(current_dir, 'first_result.xlsx')

book = load_workbook(work_list)

sheet = book.worksheets[0]
