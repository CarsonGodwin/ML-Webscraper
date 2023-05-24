from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import random
from selenium.webdriver.common.keys import Keys
import time
import datetime
#Really cool and awesome webscrapper

options = webdriver.ChromeOptions()

#check that the correct version of the driver is installed for the version of Chrome is installed
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Define search categories and their corresponding probabilities for each time of day
categories_by_time = {
    'morning': {
        'morning_food.txt': 0.2,
        'morning_news.txt': 0.3,
        'R&P_beliefs.txt': 0.1,
        'random.txt': 0.2,
        'sports.txt':.02
    },
    'afternoon': {
        'afternoon_interests.txt': 0.2,
        'sports.txt':.02,
        'afternoon_food.txt': 0.3,
        'R&P_beliefs.txt': 0.1,
        'random.txt': 0.2
    },
    'evening': {
        'evening_interests.txt': 0.2,
        'sports.txt':.02,
        'evening_food.txt': 0.3,
        'R&P_beliefs.txt': 0.1,
        'random.txt': 0.2
    }
}

morning_searches = list(categories_by_time['morning'].keys())
afternoon_searches = list(categories_by_time['afternoon'].keys())
evening_searches = list(categories_by_time['evening'].keys())

def get_trait():
    'Get Personality trait file to open'

    # Determine the current time of day
    now = datetime.datetime.now()
    if now.hour >= 5 and now.hour < 12:
        time_of_day = 'morning'
    elif now.hour >= 12 and now.hour < 18:
        time_of_day = 'afternoon'
    else:
        time_of_day = 'evening'

    # Choose a random search category based on the time of day and their corresponding probabilities
    # category = random.choices(list(categories_by_time[time_of_day].keys()),
    #                           weights=list(categories_by_time[time_of_day].values()))[0]

    # Generate a random search query based on the category
    trait = ''
    if time_of_day == 'morning':
        trait = random.choice(morning_searches)
    elif time_of_day == 'afternoon':
        trait = random.choice(afternoon_searches)
    elif time_of_day == 'evening':
        trait = random.choice(evening_searches)

    return trait

    file_to_Open = trait

    #Return the name of the trait file to open
    return file_to_Open

def get_query(file_path):
    'Returns a random search query from a text file.'
    with open(file_path, 'r') as f:
        lines = f.readlines()
        line = random.choice(lines).strip()
        return line

def google_login(username, password):
    # Navigate to the Google sign-in page
    driver.get('https://accounts.google.com/signin')

    # Find the username input field and enter the username
    username_input = driver.find_element_by_xpath("//input[@type='email']")
    username_input.send_keys(username)
    username_input.send_keys(Keys.RETURN)

    # Wait for the password input field to appear
    time.sleep(3)
    # Find the password input field and enter the password
    password_input = driver.find_element_by_xpath("//input[@type='password']")
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    # Wait for the sign-in process to complete
    time.sleep(5)


results = {} # Initiate empty dictionary to capture results
def get_searchResults():
    for search in range(5):
        'Function to get search results from google and save them into a dictionary'
        #get a random search query from given txt files
        trait = get_trait()
        query = get_query(trait)
        # Specify number of pages on google search, each page contains 10 #links
        n_pages = 2
        links = [] # Store Results in list
        for page in range(1, n_pages):
            #create Url and enter it into driver
            url = "http://www.google.com/search?q=" + query + "&start=" + str((page - 1) * 10)
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            #Use beautiful soup to find all cases of certain class
            search = soup.find_all('div', class_="yuRUbf")
            #Add searches to list
            for h in search:
                links.append(h.a.text)
        #time_sleep = random.randint(0, 10)
        #time.sleep(time_sleep*60)
        results[query] = links
    driver.close()
    return results
    # Store the search results in the dictionary
    #results[query] = links

    print(results)
def store_results(dictionary):
    with open("SearchResults.txt", 'w') as f:
        for key, value in dictionary.items():
            f.write('%s:%s\n' % (key, value))

def main():
    #google_login('sloths', 'password')
    results = get_searchResults()
    store_results(results)
main()