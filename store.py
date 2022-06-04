import time
import json
import pymysql
import scraping
from threading import Thread, Lock
from time import sleep, perf_counter
# Opening JSON file
f = open('db.json')

# returns JSON object as
# a dictionary
data = json.load(f)
connection = pymysql.connect(host=data["host"],
                             user=data["user"],
                             password=data["password"],
                             database=data["database"],
                             port=data["port"]
                             )
cursor = connection.cursor()
def createTable():
        cursor.execute(f'CREATE TABLE course( id BIGINT(7) NOT NULL AUTO_INCREMENT, '
                       f'subject VARCHAR (500), number VARCHAR(100), credit DOUBLE,'
                       f' title VARCHAR(500), detail VARCHAR(1000), PRIMARY KEY(id) );'
                       )
        cursor.execute(f"ALTER TABLE `course` ADD CONSTRAINT uniq UNIQUE (title);")
def getCourseRecords(url,subject):
    subject_ = scraping.scrapeSubject(url,subject)
    numbers, credits = scraping.scrapeCourses(url,subject)
    titles = scraping.scrapeTitles(url,subject)
    details = scraping.scrapeDetails(url,subject)
    for i in range(len(numbers)):
        try:
            cursor.execute(
                (f'INSERT IGNORE INTO course (subject, number, credit, title, detail) VALUES ("{subject_}", "{numbers[i]}", "{credits[i]}", "{titles[i]}", "{details[i]}");')
            )
        except:
            cursor.execute(
                (
                    f"INSERT IGNORE INTO course (subject, number, credit, title, detail) VALUES ('{subject_}', '{numbers[i]}', '{credits[i]}', '{titles[i]}', '{details[i]}');")
            )
        connection.commit()
def store_record(i):
    url = scraping.geturl()
    lock = Lock()
    lock.acquire()
    try:
        getCourseRecords(url, i)
        time.sleep(5)
    except:
        getCourseRecords(url, i + 1)
        time.sleep(5)
    lock.release()

def store(start, end):
    url = scraping.geturl()
    for i in range(start, end):
        print(i)
        store_record(i)
    # connection.close()
    # cursor.close()
# AP/ASL  1000   6.00
# A/ARTH 1000   3.00

def safe_store(start, end, lock):

    store(start,end)


def test():
    lock = Lock()
    thread1 = Thread(target=store, args=(85, 100))
    thread2 = Thread(target=store, args=(100, 150))
    thread3 = Thread(target=store, args=(150, 200))
    thread4 = Thread(target=store, args=(200, 209))
    threads = [thread1, thread2, thread3, thread4]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    # createTable()
    # test()
    store(85, 209)
    connection.close()
    cursor.close()