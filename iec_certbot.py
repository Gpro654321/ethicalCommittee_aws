import gspread
from jinja2 import Template 
import pandas as pd
import os
import datetime
import shutil
import sys

from iec_pdfcreator import html_to_pdf
from iec_sheet_copy import copy_file 



# use the service account credentials
gc = gspread.service_account(
    filename='./iec-certificate-fe8128ae7e58.json'
)

# open the spreadsheet with spreadsheet key
spreadsheet = gc.open_by_key('1p2G2br19t2AMUO4FHCLZVQN1L7KsFCtq9snoIpFbclE')

# open the worksheet using the sheet name
worksheet = spreadsheet.worksheet('Form responses 1')

# get all the row data
rows = worksheet.get_all_values()

# convert to pandas dataframe
df_original = pd.DataFrame.from_records(rows)

# exit the program if there is only one row
if df_original.shape[0] == 1:
    print("Exiting the program as there are no new entries")
    sys.exit(0)


column_headers = df_original.iloc[0]

print("column_headers")
print(column_headers)



# create a new dataframe which contains rows from 1 to last
df = df_original.iloc[1:]
df.columns = column_headers

print(df)
print(df.shape)

###############################################
# backup backup backup ########################
###############################################

# before anything take a copy of the spreadsheet
backup_folder_id = '1mOW_Q0-EQE40eWXc-HQlIZv56Z-F2xs5'
copy_file(backup_folder_id)

# create a template object
template = Template(open('./html_templates/base.html').read())

# create a directory to put the newly created html files
html_dir = "./html_files"
if not os.path.exists(html_dir):
    print("html_dir NOT found, creating it...")
    os.makedirs(html_dir)

# create a directory to put the newly created pdf files
pdf_dir = "./pdf_files"
if not os.path.exists(pdf_dir):
    print("pdf_dir NOT found, creating it ..")
    os.makedirs(pdf_dir)

    
# Apply the render function to each row and generate the HTML file
for index, row in df.iterrows():
    # fix the salutation
    if row['Designation'] == 'Faculty (Doctors or Doctrates)':
        sal = "Dr. "
    elif row['Designation'] == 'Post graduate':
        sal = 'Dr. '
    else:
        sal = ""
    print("salutation =",sal)

    # fix the speciality
    if str(row['Specialty']).upper() == "OTHERS":
        # if the user has chosen OTHERS in the speciality,
        # then would have specified their dept in "others, please specify" column
        alt_dept = str(row['If OTHERS, please specify']).upper()
    else:
        alt_dept = str(row['Specialty']).upper()
    
    # fix the institute
    if row['Name of the Institution'] == 'KAPVGMC':
        inst = 'K. A. P. VISWANATHAM GOVT. MEDICAL COLLEGE, TIRUCHIRAPALLI'
    else:
        inst = row['If other Institution, please specify'].upper()

    now = datetime.datetime.now()
    current_time_string = now.strftime("%Y%m%d%H%M%S%f")
    rendered_html = template.render(
        refno = current_time_string, 
        title = str(row['Title of the proposal']).upper(),
        salutation = sal,
        name = str(row['Name']).upper(),
        department = alt_dept.upper() ,
        institution = inst.upper(),
    )
    
    candidate_name = row['Name']
    # write the rendered html string to a file
    html_file_name = f"iec_cert_{index}_{candidate_name}.html"
    html_file_path = os.path.join(html_dir, html_file_name)
    with open(html_file_path, 'w') as f:
        print("creating file ",index)
        f.write(rendered_html)
    
    print("creating pdf file", index)
    html_to_pdf(html_file_path)

    # to prevent clutter of the html_files folder the html files
    # will be deleted once a pdf file is created out of it
    os.remove(html_file_path)


# after everything is completed delete the existing rows
worksheet.delete_rows(2,df_original.shape[0])
print("Deleted all rows except the headers in the sheet")
