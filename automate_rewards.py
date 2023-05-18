from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


chrome_options = Options()
chrome_options.add_argument("--headless")  
chromedriver_path = "/path/to/chromedriver"
driver = webdriver.Chrome()

# def sign_in(email, password):
#     driver.get("https://account.microsoft.com/rewards/")
#     sign_in_button = driver.find_element_by_xpath('//div[@class="claim-row"]/button')
#     sign_in_button.click()
#     time.sleep(2)
#     email_field = driver.find_element_by_xpath('//input[@name="loginfmt"]')
#     email_field.send_keys(email)
#     email_field.send_keys(Keys.RETURN)
#     time.sleep(2)
#     password_field = driver.find_element_by_xpath('//input[@name="passwd"]')
#     password_field.send_keys(password)
#     password_field.send_keys(Keys.RETURN)
#     time.sleep(2)

# def perform_search(query):
#     search_box = driver.find_element_by_xpath('//input[@id="sb_form_q"]')
#     search_box.send_keys(query)
#     search_box.send_keys(Keys.RETURN)
#     time.sleep(2)

# def main():
    # email = "your_email@example.com"  # Enter your Microsoft account email
    # password = "your_password"  # Enter your Microsoft account password
    # sign_in(email, password)
    # queries = ["search query 1", "search query 2", "search query 3"]  # Customize the search queries
    # for query in queries:
    #     perform_search(query)
    # driver.quit()


def perform_search(query):
    driver.get("https://www.bing.com/")
    search_box = driver.find_element(By.NAME, "q")
    search_box.clear()
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

# Main function
def main():
    queries = ["linkedin", "github", "youtube"]  # Customize the search queries
    for query in queries:
        perform_search(query)

    driver.quit()


if __name__ == "__main__":
    main()
