import requests
from bs4 import BeautifulSoup


def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find_all("a", {"class": "s-pagination--item"})
    if pages:
        last_page = pages[-2].get_text(strip=True)
    else:
        last_page = 0
    return int(last_page)


def extract_job(html):
    title = html.find("a", {"class": "s-link"})["title"]
    company, location = html.find(
        "h3", {"class": "fc-black-700"}).find_all("span", recursive=False)
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)
    job_id = html['data-jobid']
    return {'title': title, 'company': company, 'location': location, "apply_link": f"https://stackoverflow.com/jobs/{job_id}"}


def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"scarapping so: Page: {page}")
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs(word):
    url = f"https://stackoverflow.com/jobs?q={word}&sort=i"
    last_page = get_last_page(url)
    if (last_page == 0):
        jobs = []
    else:
        jobs = extract_jobs(last_page, url)
    return jobs
