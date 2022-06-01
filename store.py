import time
import json
import pymysql
import scraping


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
        cursor.execute(f'CREATE TABLE courses( id BIGINT(7) NOT NULL AUTO_INCREMENT, '
                       f'subject VARCHAR (500), number VARCHAR(100), credit DOUBLE,'
                       f' title VARCHAR(500), detail VARCHAR(1000), PRIMARY KEY(id) );'
                       )
        cursor.execute(f"ALTER TABLE `courses` ADD CONSTRAINT uniq UNIQUE (title);")
def getCourseRecords(url,subject):
    subject_ = scraping.scrapeSubject(url,subject)
    numbers, credits = scraping.scrapeCourses(url,subject)
    titles = scraping.scrapeTitles(url,subject)
    details = scraping.scrapeDetails(url,subject)
    for i in range(len(numbers)):
        try:
            cursor.execute(
                (f'INSERT IGNORE INTO courses (subject, number, credit, title, detail) VALUES ("{subject_}", "{numbers[i]}", "{credits[i]}", "{titles[i]}", "{details[i]}");')
            )
        except:
            cursor.execute(
                (
                    f"INSERT IGNORE INTO courses (subject, number, credit, title, detail) VALUES ('{subject_}', '{numbers[i]}', '{credits[i]}', '{titles[i]}', '{details[i]}');")
            )
        connection.commit()
def store():
    url = scraping.geturl()
    for i in range(0, 209):
        print(i)
        try:
            getCourseRecords(url,i)
            time.sleep(5)
        except:
            getCourseRecords(url, i+1)
            time.sleep(5)
    connection.close()
    cursor.close()
# AP/ASL  1000   6.00
# A/ARTH 1000   3.00
def test():
    createTable()
    store()

if __name__ == "__main__":
    test()