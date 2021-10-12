import requests
from bs4 import BeautifulSoup

class CourseRecord:
    def __init__(self,subject, number, credit, title, detail):
        self.subject = subject
        self.number = number
        self.credit = credit
        self.title = title
        self.detail = detail
    def print(self):
        print(f'Course: {self.subject} {self.number}  {self.credit}')
        print(f'Title: {self.title}')
        print(f'Detail: {self.detail}')
def getpage():
    params={
    'sessionPopUp': 0,
    # 0-207 subjects, 64 is EECS
    'subjectPopUp': 64,
    '3.10.7.5': 'Search Courses',
    'wosid': 'TtYg7b0FwLJVOhXWKPjDDw'
    }
    req = requests.post("https://w2prod.sis.yorku.ca/Apps/WebObjects/cdm.woa/6/wo/TtYg7b0FwLJVOhXWKPjDDw/15.3.10.7",
                      data=params)

    soup = BeautifulSoup(req.text,'lxml')
    return soup
def scrapeSubject():
    soup = getpage()
    title = soup.find('td',{'width':'16%'}).text
    subject = title.split(" ")[0]
    return subject
def scrapeCourses():
    numbers = []
    credits = []
    soup = getpage()
    courses = soup.find_all('td',{'width':'16%'})
    for course in courses:
        number = course.text.split(" ")[1]
        credit = course.text.split(" ")[-1]
        numbers.append(number)
        credits.append(credit)
        # print (f"{number} + {credit}")
    return numbers,credits
def scrapeTitles():
    result = []
    soup = getpage()
    titles = soup.find_all('td', {'width': '24%'})
    for title in titles:
        title = title.text
        result.append(title)

    return result
    # return titles_
def scrapeDetails():
    details_ = []
    soup = getpage()
    details = soup.find_all('td', {'width': '30%'})
    for detail in details:
        if detail.text:
            href = detail.a['href']
            href = f"https://w2prod.sis.yorku.ca/{href}"
            details_.append(href)
    return details_
    # if details is None:

def getCourseRecords():
    records = []
    subject = scrapeSubject()
    numbers, credits = scrapeCourses()
    titles = scrapeTitles()
    details = scrapeDetails()
    for i in range(len(numbers)):
        course_record = CourseRecord(subject, numbers[i],credits[i], titles[i],details[i])
        records.append(course_record)
        course_record.print()
    return records
if __name__ == "__main__":
    # records = getCourseRecords()
    getCourseRecords()