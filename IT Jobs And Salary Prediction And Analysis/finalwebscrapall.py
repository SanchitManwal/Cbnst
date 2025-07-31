from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import pandas as pd

# Set up ChromeDriver
service = Service("C:/Users/user/Downloads/chromedriver-win64 (2)/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Open Naukri website
driver.get("https://www.naukri.com/")

# Wait for the search input field to load
wait = WebDriverWait(driver, 10)


# 🎯 Find the "Jobs" menu div
jobs_menu = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[4]/div[2]/nav/ul/li[1]/a/div')))

# 🎯 Hover over "Jobs"
action = ActionChains(driver)
action.move_to_element(jobs_menu).perform()

# 🎯 Wait for "IT JOBS" to appear & Click it
it_jobs = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[4]/div[2]/nav/ul/li[1]/div/ul[1]/li[2]/a/div')))
it_jobs.click()


# Apply sorting filter (optional)
down = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="filter-sort"]')))
down.click()
date_but = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="jobs-list-header"]/div[2]/span/div/ul/li[2]/a')))
date_but.click()

# Wait for job listings to load
time.sleep(5)
filt = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="functionAreaIdGid"]/span')))
filt.click()


ui = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="swiperType"]/div/div[2]/div[6]/label/i')))
ui.click()
datasci = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="swiperType"]/div/div[2]/div[1]/label/i')))
datasci.click()


app = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tooltip"]/div[2]/div[3]/div[2]')))
app.click()


df = pd.DataFrame(columns=["Name","Company","Rating","Skills","Salary", "Location","Exp","Job_Description","Reviews","Date","Page_count"])


page_count=0
while True:  # Set the number of pages to scrape
    page_count+=1
    time.sleep(5)  # Allow time for jobs to load
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    postings = soup.find_all("div", class_="srp-jobtuple-wrapper")

    for post in postings:
        try:
            name = post.find("a", class_="title").text.strip()
        except:
            name = "Not Available"

        try:
            sal = post.find("span", class_="ni-job-tuple-icon-srp-rupee").text.strip()
        except:
            sal = "Not Available"

        try:
            loc = post.find("span", class_="ni-job-tuple-icon-srp-location").text.strip()
        except:
            loc = "Not Available"

        try:
            day = post.find("span", class_="job-post-day").text.strip()
        except:
            day = "Not Available"

        try:
            expi = post.find("span", class_="expwdth").text.strip()
        except:
            expi = "Not Available"

        try:
            comp_name = post.find("a", class_="comp-name mw-25").text.strip()
        except:
            comp_name = "Not Available"
        try:    
            rat = post.find("span", class_="main-2").text.strip()
        except:
            rat = "Not Available"

        try:    
            jd = post.find("span", class_="job-desc ni-job-tuple-icon ni-job-tuple-icon-srp-description").text.strip()
        except:
            jd = "Not Available"
        
        try:    
            rev = post.find("a", class_="review ver-line").text.strip()
        except:
            rev = "Not Available"
        
        try:
            # 🎯 Locate the <ul> that contains skills
            skills_list = post.find("ul", class_="tags-gt")
    
            # 🎯 Extract all <li> elements containing skills
            if skills_list:
                skill = ", ".join([li.text.strip() for li in skills_list.find_all("li", class_="dot-gt tag-li")])
            else:
                skill = "Not Available"

        except Exception as e:
            skill = "Not Available"
        
        df = pd.concat([df, pd.DataFrame([{"Name": name, "Salary": sal, "Location": loc,"Exp":expi, "Date": day,"Page_count":page_count,"Company":comp_name,"Rating":rat,"Skills":skill,"Job_Description":jd,"Reviews":rev}])], ignore_index=True)

    

    # Scroll to the "Next" button before clicking
    try:
        next_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#lastCompMark > a:nth-child(4)')))
        time.sleep(1)  
        next_button.click()
    except:
        print("No more pages found. Exiting loop.")
        break

print(f"Scraping stopped after {page_count} pages.")


# Save the DataFrame as a CSV file on the desktop
df.to_csv("C:/Users/user/Desktop/job2.csv", index=False)
print("File saved successfully on Desktop!")

# Close the browser
driver.quit()
