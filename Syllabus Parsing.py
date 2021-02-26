#!/usr/bin/env python
# coding: utf-8

# # HW2 - Syllabus Parsing
# ## Christopher Chao

# In[1]:


import pandas as pd
import re
import pdfplumber
import os


# # IMPORTANT! Change to the directory of the syllabi folder location

# In[2]:


#Change this to the directory of the syllabi folder location
directory = os.fsencode('D:/Dropbox/School/20-21 S2/Data Wrangling/HW 2/syllabi')


# # Testing PDF to Text Package (pdfplumber)

# In[3]:


pdf = pdfplumber.open('syllabi/Syllabus_Sample.pdf')
page = pdf.pages[0]
text = page.extract_text()
#print(text)
pdf.close()


# # Retrieving All Syllabi and Saving Text As List
# * `list_of_syllabi` contains all the syllabi, each element is a syllabus.
# * Each element of `list_of_syllabi` is a list called `page_list`. 
# * Each element of `page_list` is a page of the pdf file converted to text. <br> <br>
# It should look like the format: <br>
# `[[Syllabus1_Page1, Syllabus1_Page2,...],[Syllabus2_Page1, Syllabus2_Page2,...]]`

# ## This cell will take a while to run, since it is reading through all syllabi and appending it to a list.

# In[4]:


list_of_syllabi = []
num_of_pdf = 0

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    
    page_list = []
    
    if filename.endswith(".pdf"):
        num_of_pdf += 1
        pdf = pdfplumber.open('syllabi/' + filename)

        pages = pdf.pages
        
        for i,pg in enumerate(pages):
            text = pages[i].extract_text()
            page_list.append(text)
            

        pdf.close()
        
        #print(page_list)
    else:
        continue
    list_of_syllabi.append(page_list)


# In[5]:


num_of_pdf


# In[6]:


#Prints out Syllabus 1's First Page
list_of_syllabi[0][0]


# ## This massive cell uses regex to find information and add it to a new list

# In[7]:


list_of_syllabi_parsed = []

#Most of the regex is found here
instructor_re = re.compile(r'(?i)(?<=Instructor).{100}|(?<=Professor).{100}',re.DOTALL)
course_re = re.compile(r'(?i)(?<=Course).{100}',re.DOTALL)
units_re = re.compile(r'(?i).{2}(?=unit[s]?[-]?).{50}|.{2}(?= credits).{50}',re.DOTALL)
office_re = re.compile(r'(?i)(?<=Office Hours).{200}',re.DOTALL)
name_re = re.compile(r'([A-Z]{1}[a-z]{1,30}[- ]{0,1}|[A-Z]{1}[- \']{1}[A-Z]{0,1}[a-z]{1,30}[- ]{0,1}){2,3}',re.DOTALL)
email_re = re.compile(r'(?:[A-Za-z0-9!#$%&\'*+\=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&\'*+\=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[A-Za-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])')
phone_re = re.compile(r'\(?\d{3}\)?[\s.-]?\d{3}[-]\d{4}|\d{3}[-]\d{4}')
time_re = re.compile(r'[0-2]?[0-9]:[0-5][0-9]')
timeto_re = re.compile(r'[0-2]?[0-9]:[0-5][0-9][am|pm]?[\s]?-[\s]?[0-2]?[0-9]:[0-5][0-9][am|pm]?')
digit_re = re.compile(r'[0-9]')
days_re = re.compile(r'(?i)((mon|tues|wed(nes)?|thur(s)?|fri|sat(ur)?|sun)(day)?)')
year_re = re.compile(r'(20|19)[0-9][0-9]')
classid_re = re.compile(r'[A-Z]{3,5}[\s_]?[0-9]{2,5}')

for i in range(num_of_pdf):
    #Joins all the pages of the PDF into one giant text.
    joined_pages_syllabus = " ".join(list_of_syllabi[i])
    
    name = name_re.search(joined_pages_syllabus)
    email = email_re.search(joined_pages_syllabus)
    phone = phone_re.search(joined_pages_syllabus)
    time = time_re.search(joined_pages_syllabus)
    class_time = timeto_re.search(joined_pages_syllabus)
    day = days_re.search(joined_pages_syllabus)
    year = year_re.search(joined_pages_syllabus)
    ID = classid_re.search(joined_pages_syllabus)
    
    #This list will store all the information
    current_syllabus = []
    
    #Divider line
    #print('==========================================')
    
#Course Name
    try:
        after_course = course_re.search(joined_pages_syllabus).group(0)
        course_name = name_re.search(after_course).group(0)
        #print("Course Name: " + course_name)
        current_syllabus.append(course_name)
    except: 
        #print("Course Name Unavailable.")
        current_syllabus.append("")
    
#Course ID
    try:
        #print("CourseID: " + ID.group(0))
        current_syllabus.append(ID.group(0))        
    except: 
        #print("Course ID Unavailable.")
        current_syllabus.append("")
    
#Unit Count
    try:
        after_units = units_re.search(joined_pages_syllabus).group(0)
        unit_count = digit_re.search(after_units).group(0)
        #print("Units: " + unit_count)
        current_syllabus.append(unit_count)
    except: 
        #print("Unit Count Unavailable.")
        current_syllabus.append("")
            
#Instructor Name
    try:
        after_instructor = instructor_re.search(joined_pages_syllabus).group(0)
        instructor_name = name_re.search(after_instructor).group(0)
        #print("Instructor Name: " + instructor_name.strip())
        current_syllabus.append(instructor_name.strip())
    except: 
        #print("Instructor Name Unavailable.")
        current_syllabus.append("")
    
#Office Hours
    try:
        after_office = office_re.search(joined_pages_syllabus).group(0)
        office_hours = time_re.search(after_office).group(0)
        #print("Office Hours: " + office_hours)
        current_syllabus.append(office_hours)
    except: 
        #print("Office Hours Unavailable.")
        current_syllabus.append("")
    
#Email
    try:
        #print("Email: " + email.group(0))
        current_syllabus.append(email.group(0))
    except:
        #print("Email Unavailable.")
        current_syllabus.append("")
    
#Phone Number
    try:
        #print("Phone: " + phone.group(0))
        current_syllabus.append(phone.group(0))
    except:
        #print("Phone Number Unavailable.")
        current_syllabus.append("")
    
#Day
    try:
        #print("Day: " + day.group(0).capitalize())
        current_syllabus.append(day.group(0).capitalize())
    except: 
        #print("Day Unavailable.")
        current_syllabus.append("")
    
#Time
    try:
        #print("Class starts at: " + class_time.group(0))
        current_syllabus.append(class_time.group(0))
    except:
        #print("Time Unavailable.")
        current_syllabus.append("")

#Semester
    if (re.compile(r'(?i)Fall').search(joined_pages_syllabus) is not None):
        #print("Semester: Fall")
        current_syllabus.append("Fall")
    elif (re.compile(r'(?i)Spring').search(joined_pages_syllabus) is not None):
        #print("Semester: Spring")
        current_syllabus.append("Spring")
    elif (re.compile(r'(?i)Winter').search(joined_pages_syllabus) is not None):
        #print("Semester: Winter")
        current_syllabus.append("Winter")
    elif (re.compile(r'(?i)Summer').search(joined_pages_syllabus) is not None):
        #print("Semester: Summer")
        current_syllabus.append("Summer")
    else:
        #print("Semester Unavailable.")
        current_syllabus.append("")
    
#Year
    try:
        #print("Year: " + year.group(0))
        current_syllabus.append(year.group(0))
    except:
        #print("Year Unavailable.")
        current_syllabus.append("")

#Online
    if (re.compile(r'(?i)Online').search(joined_pages_syllabus) is not None):
        #print("Online: Yes")
        current_syllabus.append("Yes")
    else:
        #print("Online: No")
        current_syllabus.append("No")
        
    list_of_syllabi_parsed.append(current_syllabus)


# ## First 2 elements of the parsed list

# In[8]:


list_of_syllabi_parsed[0:2]


# ## Generating a Pandas dataframe of the parsed syllabi

# In[9]:


syllabi_parsed_df = pd.DataFrame(list_of_syllabi_parsed, columns = ['Course Name', 'Course ID', 'Units',
                                                                    'Instructor Name', 'Office Hours', 'Email',
                                                                    'Phone', 'Day', 'Class Time',
                                                                    'Semester', 'Year', 'Online'])
syllabi_parsed_df


# In[10]:


syllabi_parsed_df.to_csv('features-retrieved-by-ChrisChao.csv')

