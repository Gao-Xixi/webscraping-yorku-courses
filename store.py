import time
import json
import random

import pymysql
import selenium_scraping as sc
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
def insertCourseRecords(record):
    print(record.subject)

    try:
        cursor.execute(
            (f'INSERT IGNORE INTO course (subject, number, credit, title, detail) VALUES ("{record.subject}", "{record.number}", "{record.credit}", "{record.title}", "{record.detail}");')
        )
    except:
        cursor.execute(
            (
                f"INSERT IGNORE INTO course (subject, number, credit, title, detail) VALUES ('{record.subject}', '{record.number}', '{record.credit}', '{record.title}', '{record.detail}');")
        )
    connection.commit()
def store_record(record):

    lock = Lock()
    lock.acquire()
    try:
        insertCourseRecords(record)
        time.sleep(5)
    except:
        print(record)
        time.sleep(5)
    lock.release()
#
def store(records, start, end):
    for i in range(start, end):
        store_record(records[i])
    # connection.close()
    # cursor.close()
# # AP/ASL  1000   6.00
# # A/ARTH 1000   3.00
#
#
def run():
    records = sc.get_page_source()
    print(records)
    for record in records:
        print('insert')
        print(record)
        insertCourseRecords(record)

    # thread_len = 4
    # threads = []
    # records = sc.get_page_source()
    # print(len(records))
    # list1 = [random.randint(1, len(records)) for _ in range(thread_len - 1)]
    # list1.append(0)
    # list1.append(len(records) - 1)
    # list1.sort()
    #
    # for i in range(thread_len - 1):
    #     thread = Thread(target=store, args=(records, list1[i], list1[i + 1]))
    #     threads.append(thread)
    #
    # for thread in threads:
    #     thread.start()
    # for thread in threads:
    #     thread.join()

if __name__ == "__main__":
    # createTable()
    run()
    connection.close()
