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
# according to subject name, return the subjectPopUp used for post method
def getsubjectPopUp(subject):
    # mainpage
    rs = requests.get("https://w2prod.sis.yorku.ca/Apps/WebObjects/cdm")
    
    r = requests.get("https://w2prod.sis.yorku.ca/Apps/WebObjects/cdm.woa/6/wo/TtYg7b0FwLJVOhXWKPjDDw/15.3.10.7")
    bs = BeautifulSoup(r.text, 'lxml')
    options = bs.find_all('option')
    for option in options:
        if subject.lower() in option.text.lower():
            subjectPopUp = int(option['value'])
            print(subjectPopUp)
            return subjectPopUp
    # raise Exception('Wrong major name')
def getpage(subject):
    subjectPopUp = getsubjectPopUp(subject)
    params={
    'sessionPopUp': 0,
    # 0-207 subjects, 64 is EECS
    'subjectPopUp': subjectPopUp,
    '3.10.7.5': 'Search Courses',
    'wosid': 'TtYg7b0FwLJVOhXWKPjDDw'
    }
    req = requests.post("https://w2prod.sis.yorku.ca/Apps/WebObjects/cdm.woa/6/wo/TtYg7b0FwLJVOhXWKPjDDw/15.3.10.7",
                      data=params)

    soup = BeautifulSoup(req.text,'lxml')
    return soup
def scrapeSubject(subject):
    soup = getpage(subject)
    sub = soup.find('td',{'width':'16%'}).text
    sub = sub.split(" ")[0]
    return sub
def scrapeCourses(subject):
    numbers = []
    credits = []
    soup = getpage(subject)
    courses = soup.find_all('td',{'width':'16%'})
    for course in courses:
        number = course.text.split(" ")[1]
        credit = course.text.split(" ")[-1]
        numbers.append(number)
        credits.append(credit)
        # print (f"{number} + {credit}")
    return numbers,credits
def scrapeTitles(subject):
    result = []
    soup = getpage(subject)
    titles = soup.find_all('td', {'width': '24%'})
    for title in titles:
        title = title.text
        result.append(title)

    return result
    # return titles_
def scrapeDetails(subject):
    details_ = []
    soup = getpage(subject)
    details = soup.find_all('td', {'width': '30%'})
    for detail in details:
        if detail.text:
            href = detail.a['href']
            href = f"https://w2prod.sis.yorku.ca/{href}"
            details_.append(href)
    return details_
    # if details is None:

def getCourseRecords(subject):
    records = []
    subject_ = scrapeSubject(subject)
    numbers, credits = scrapeCourses(subject)
    titles = scrapeTitles(subject)
    details = scrapeDetails(subject)
    for i in range(len(numbers)):
        course_record = CourseRecord(subject_, numbers[i],credits[i], titles[i],details[i])
        records.append(course_record)
        course_record.print()
    return records
if __name__ == "__main__":
    # records = getCourseRecords()
    subject = input("int put your major(for example EECS): ")
    try:
        getsubjectPopUp(subject)
    except Exception:
        print("Cannot find your major!")
