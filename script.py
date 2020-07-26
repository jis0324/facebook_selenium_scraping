import os
import time
from selenium import webdriver
import traceback

base_dir = os.path.dirname(os.path.abspath(__file__))

def set_driver():
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) ' \
        'Chrome/80.0.3987.132 Safari/537.36'
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument('--no-sandbox')
    chrome_option.add_argument('--disable-dev-shm-usage')
    chrome_option.add_argument('--ignore-certificate-errors')
    chrome_option.add_argument("--disable-blink-features=AutomationControlled")

    chrome_option.add_argument(f'user-agent={user_agent}')
    # chrome_option.headless = True
    
    driver = webdriver.Chrome(options = chrome_option)
    return driver

def main():
    group_url_list = list()

    url = 'https://www.facebook.com/'
    email = 'working.user101@gmail.com'
    password = 'workinguser01'

    # /* Move to facebook.com */
    driver = set_driver()
    driver.get(url)
    time.sleep(30)
    
    try:
        
        # /* Login */
        login_email = driver.find_element_by_css_selector("input.login_form_input_box[type='email']")
        login_email.send_keys(email)
        time.sleep(5)

        login_password = driver.find_element_by_css_selector("input.login_form_input_box[type='password']")
        login_password.send_keys(password)
        time.sleep(5)

        driver.find_element_by_css_selector("input[aria-label='Log In']").click()
        time.sleep(10)

        # /* Search groups */
        search_keys = list()
        with open(base_dir + '/search_key.txt', 'r') as search_key_file:
            search_keys = [row.strip() for row in search_key_file.read().split('\n')]

        for search_key in search_keys:
            try:
                driver.get('https://www.facebook.com/search/groups/?q={search_key}&epa=SERP_TAB'.format(search_key=search_key))
                time.sleep(10)

                init_groups = driver.find_elements_by_xpath("//div[@id='BrowseResultsContainer']//div[@data-testid='browse-result-content']/div[1]/div[1]//a")
                for init_group in init_groups:
                    group_url = init_group.get_attribute('href')
                    if group_url:
                        if not group_url.strip() in group_url_list:
                            group_url_list.append(group_url.strip())
                            with open (base_dir + '/group_urls.txt', 'a') as group_urls_txt:
                                group_urls_txt.write(group_url + '\n')

                max_height = driver.execute_script("return document.body.scrollHeight")
                max_height_flag = 0

                while True:
                    # scroll down
                    driver.execute_script("window.scrollTo(0, " + str(max_height) + ");")
                    time.sleep(20)
                    # get current document height
                    current_height = driver.execute_script("return document.body.scrollHeight")

                    if current_height > max_height:
                        max_height = current_height
                    else:
                        max_height_flag += 1
                        if max_height_flag > 3:
                            max_height_flag = 0
                            break
                    continue

                groups = driver.find_elements_by_xpath("//div[@data-testid='results']/div/div/div/div[2]/div/div[1]/div[1]/div/div/div/a")
                
                for group in groups:
                    group_url = group.get_attribute('href')
                    if group_url:
                        if not group_url.strip() in group_url_list:
                            group_url_list.append(group_url.strip())
                            with open (base_dir + '/group_urls.txt', 'a') as group_urls_txt:
                                group_urls_txt.write(group_url + '\n')

                print(" Filtered Group URLs Count : ", len(group_url_list))
            except Exception as err :
                print(err)
                continue
        
    except:
        print(traceback.print_exc())
        print("element not found..")

if __name__ == '__main__':
    main()
