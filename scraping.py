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
def geturl():
    r = requests.get("https://w2prod.sis.yorku.ca/Apps/WebObjects/cdm")
    bs = BeautifulSoup(r.text, 'lxml')
    ul = bs.find('ul',class_='bodytext')
    href = ul.li.a['href']
    href = f"https://w2prod.sis.yorku.ca/{href}"
    print(href)
    r = requests.get(href)
    bs = BeautifulSoup(r.text, 'lxml')
    form = bs.find('form', {'method': 'post'})
    url = form['action']
    print(url)
    return url

# def getsubjectPopUp(url,subject):
#     # mainpage
#     r = requests.get(url)
#     wosid = url.split('/')[-2]
#     bs = BeautifulSoup(r.text, 'lxml')
#     options = bs.find_all('option')
#     for option in options:
#         if subject.lower() in option.text.lower():
#             subjectPopUp = int(option['value'])
#             print(subjectPopUp)
#             return subjectPopUp
#     return None

def getpage(url, subject):
    # subjectPopUp = getsubjectPopUp(url)
    wosid = url.split('/')[-2]
    params={
    'sessionPopUp': 0,
    # 0-207 subjects, 64 is EECS
    'subjectPopUp': subject,
    '3.10.7.5': 'Search Courses',
    'wosid': wosid
    }
    req = requests.post(url,data=params)

    soup = BeautifulSoup(req.text,'lxml')
    print(wosid)
    return soup
# def getpage(url,subject):
#     subjectPopUp = getsubjectPopUp(url,subject)
#     wosid = url.split('/')[-2]
#     params={
#     'sessionPopUp': 0,
#     # 0-207 subjects, 64 is EECS
#     'subjectPopUp': subjectPopUp,
#     '3.10.7.5': 'Search Courses',
#     'wosid': wosid
#     }
#     req = requests.post(url,data=params)
#
#     soup = BeautifulSoup(req.text,'lxml')
#     print(wosid)
#     return soup
def scrapeSubject(url,subject):
    soup = getpage(url,subject)
    sub = soup.find('td',{'width':'16%'}).text
    sub = sub.split(" ")[0]
    print(sub)
    return sub
def scrapeCourses(url,subject):
    numbers = []
    credits = []
    soup = getpage(url,subject)
    courses = soup.find_all('td',{'width':'16%'})
    for course in courses:
        try:
            number = course.text.split()[1]
            credit = course.text.split()[-1]
            numbers.append(number)
            credits.append(credit)
        except:
            numbers.append("none")
            credits.append("none")

    print(numbers)
    print(credits)
    return numbers,credits
def scrapeTitles(url,subject):
    result = []
    soup = getpage(url,subject)
    titles = soup.find_all('td', {'width': '24%'})
    for title in titles:
        try:
            title = title.text
            result.append(title)
        except:
            result.append("none")
    print(result)
    return result
    # return titles_
def scrapeDetails(url,subject):
    result = []
    soup = getpage(url,subject)
    details = soup.find_all('td', {'width': '30%'})
    for detail in details:
        if detail.text:
            try:
                href = detail.a['href']
                href = f"https://w2prod.sis.yorku.ca/{href}"
                result.append(href)
            except:
                result.append("none")
    print(result)
    return result
    # if details is None:

def getCourseRecords(url,subject):
    records = []
    subject_ = scrapeSubject(url,subject)
    numbers, credits = scrapeCourses(url,subject)
    titles = scrapeTitles(url,subject)
    details = scrapeDetails(url,subject)
    for i in range(len(numbers)):
        course_record = CourseRecord(subject_, numbers[i],credits[i], titles[i],details[i])
        records.append(course_record)
        course_record.print()
    return records
def getData(subject):
    url = geturl()
    scrapeDetails(url,subject)
    return getCourseRecords(url,subject)

if __name__ == "__main__":
    getData(64)



