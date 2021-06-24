import requests
from bs4 import BeautifulSoup
from pprint import pprint
import sqlalchemy

list_of_jobs = []
NUM_OF_PAGES = 10
URL = "https://www.indeed.com/jobs?q=javascript&l="
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

def get_number_of_jobs(soup):
    count_pages = soup.find(id="searchCountPages").text.strip()
    count_pages_list = count_pages.split(" ")
    num_job_str = count_pages_list[3].replace(",","")
    num_jobs = int(num_job_str)
    # Number of Jobs
    print(f"Number of Jobs: {num_jobs} ")

def get_next_page(soup):
    pagination = soup.find("ul", class_="pagination-list")
    pages = pagination.find_all("li")
    last_page = pages[-1].find("a")['href']
    next_page = f"https://www.indeed.com{last_page}"
    return next_page

def get_jobs(soup):
    # list of jobs
    job_list = soup.find_all("div", class_="jobsearch-SerpJobCard")
    for job in job_list:
        title = job.find("a",class_="jobtitle").text.strip()
        company_name = job.find("span", class_="company").text.strip()
        location = job.find("span", class_="location")
        rating = job.find("span", class_="ratingsContent")
        if location:
            location = location.text.strip()
        if rating:
            rating = rating.text.strip()
        job_dict = {
            "title":  title if title else None,
            "company_name": company_name if company_name else None,
            "location": location if location else None,
            "rating": rating if rating else None
        }
        list_of_jobs.append(job_dict)

# how do we loop through the first 10 pages and get all of the jobs
def loop_through_pages():
    URL = "https://www.indeed.com/jobs?q=javascript&l="
    current_page = 0
    while current_page < NUM_OF_PAGES and URL:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        print("loading:", URL)
        get_jobs(soup)
        URL = get_next_page(soup)
        current_page += 1


# URL = "https://www.indeed.com/jobs?q=javascript&l="
# for page in range(NUM_OF_PAGES):
#     page = requests.get(URL)
#     soup = BeautifulSoup(page.content, 'html.parser')

#     get_jobs(soup)
#     print("loading:", URL)
#     print(len(list_of_jobs))
#     URL = get_next_page(soup)





get_number_of_jobs(soup)
get_next_page(soup)
get_jobs(soup)
loop_through_pages()



pprint(len(list_of_jobs))



