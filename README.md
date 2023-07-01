# webscraping-yorku-courses
Crawling through forms
### Update 2023.6.26
AWS DB expired, connect to local db
### Issue
- [X] [https://github.com/Gao-Xixi/webscraping-yorku-courses/issues/1]
> The previous code does not work because of the complex and dynamic generated url. 
> Selenium library now is used to solve this problem
### Update
Connected to AWS RDB MYSQL
### Difficuties

- Url changes dynamiclly
- Form method = post
## How to play with this project:
```
git clone this repository
create a new file json named db.json
store your mysql host, username, password, port info in json file
run store,py
```
![Screenshot](./docs/result.jpg)
