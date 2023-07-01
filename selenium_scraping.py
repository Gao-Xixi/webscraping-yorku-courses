import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from threading import Thread, Lock

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
PATH = "/Users/smallcrop/Desktop/GITHUB REPO/chromedriver"
def get_page_source(start, end):
    result = []
    driver = webdriver.Chrome(PATH)

    driver.get("https://w2prod.sis.yorku.ca/Apps/WebObjects/cdm")
    # first page

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Subject"))
        )
        driver.find_element(By.LINK_TEXT, "Subject").click()
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "subjectSelect"))
        )
        sessions = driver.find_element(By.XPATH, '//*[@id="sessionSelect"]/option[3]').click()
        subjects = driver.find_elements(By.CSS_SELECTOR, '#subjectSelect > option')
        num_of_options = len(subjects)
        print(num_of_options)
        for i in range(start, end):
        # for i in range(0, num_of_options):
            subjects = driver.find_elements(By.CSS_SELECTOR, '#subjectSelect > option')
            subjects[i].click()
            #  Search course button
            driver.find_element(By.XPATH,
                                '/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td/form/table/tbody/tr[4]/td[2]/input')\
                    .click()


            # get_url = driver.current_url
            #
            # print("The current url is:" + str(get_url))
            time.sleep(5)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'lxml')
            result += getCourseRecords(soup)

            time.sleep(5)
            # Navigate back
            driver.back()
            # # find next url from beginning
            # driver.get("https://w2prod.sis.yorku.ca/Apps/WebObjects/cdm")
            # # first page
            # driver.find_element(By.LINK_TEXT, "Subject").click()
            # time.sleep(2)
        return result
    finally:
        driver.quit()

def scrape_range(start, end):

    lock = Lock()
    lock.acquire()
    try:
        get_page_source(start,end)
        time.sleep(5)
    except:
        time.sleep(5)
    lock.release()

def scrapeSubject(soup):
    sub = soup.find('td',{'width':'16%'}).text
    sub = sub.split(" ")[0]
    print(sub)
    return sub
def scrapeCourses(soup):
    numbers = []
    credits = []
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
def scrapeTitles(soup):
    result = []
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
def scrapeDetails(soup):
    result = []
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

def getCourseRecords(soup):
    records = []
    subject_ = scrapeSubject(soup)
    numbers, credits = scrapeCourses(soup)
    titles = scrapeTitles(soup)
    details = scrapeDetails(soup)
    for i in range(len(numbers)):
        course_record = CourseRecord(subject_, numbers[i],credits[i], titles[i],details[i])
        records.append(course_record)
        course_record.print()
    return records

# def run():
    # lock for loop, not work ,only one thread works
    # for i in range(thread_len - 1):
    # thread1 = Thread(target=scrape_range, args=(0, 50))
    # thread2 = Thread(target=scrape_range, args=(50, 100))
    # thread3 = Thread(target=scrape_range, args=(100, 150))
    # thread4 = Thread(target=scrape_range, args=(150, 207))
    # threads= [thread1, thread2,thread3,thread4]
    #
    # for thread in threads:
    #     thread.start()
    # for thread in threads:
    #     thread.join()
if __name__ == "__main__":
    # run()
    get_page_source(0,2)