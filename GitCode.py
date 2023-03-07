# installing depednencies
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import os
os.system("pip install selenium")
os.system("pip install webdriver-manager")


def get_links(driver):
    time.sleep(2)
    # getting the solved problems

    # Status button
    while(True):
        try:
            ff = driver.find_element(By.XPATH, "//*[contains(text(), 'Status')]")
            ff.click()
            break
        except:
            driver.refresh()
    time.sleep(1)

    # Solved button
    
    while(True):
        try:
            ff = driver.find_element(By.XPATH, "//*[contains(text(), 'Solved')]")
            ff.click()
            break
        except:
            driver.refresh()
    time.sleep(1)

    list_of_links = []
    list_of_names = []

    def find(driver):
        # getting the navigation element
        return driver.find_elements(By.XPATH, ".//nav[@role = 'navigation']//button[@aria-label='next']")[-1]

    page = 1

    while (True):
        # getting the list of problems
        print("Page: " + str(page))

        if page != 1:
            WebDriverWait(driver, 20).until(find)
            try:
                driver.find_elements(By.XPATH, ".//nav[@role = 'navigation']//button[@aria-label='next']")[-1].click()
            except Exception as e:
                print(e)
                break

        ind = 0;

        while(ind < len(driver.find_elements(By.XPATH, ".//div[@role = 'rowgroup']//div[@role = 'row']"))):

            # this gets the div of the row
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, ".//div[@role = 'rowgroup']//div[@role = 'row']")))
            innerDiv = driver.find_elements(By.XPATH, ".//div[@role = 'rowgroup']//div[@role = 'row']")[ind]
            WebDriverWait(innerDiv, 30).until(EC.presence_of_element_located((By.XPATH, ".//div[@role = 'cell']")))
            innerDiv = innerDiv.find_elements(By.XPATH, ".//div[@role = 'cell']")[1]

            name = innerDiv.text  # this gets the name of the problem
                
            link = WebDriverWait(innerDiv, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
            while(True):
                try:
                    link = link.get_attribute("href")  # gets the link of the problem
                    break
                except:
                    link = WebDriverWait(innerDiv, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))

            list_of_links.append(link)
            list_of_names.append(name)

            ind = ind + 1

        time.sleep(5)

        page = page + 1

    totalnumber = len(list_of_links)
    print("Total number of problems: " + str(totalnumber))

    print(list_of_links)
    print(list_of_names)

    list_of_links = list_of_links[1:]
    list_of_names = list_of_names[1:]

    return list_of_links, list_of_names


def main(args):
    # setting up the driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()

    # removing the soln folder if it exists
    if os.path.exists(args.path):
        os.system(f"rm -rf {args.path}")

    os.makedirs(args.path)
    os.system(f"git add {args.path}")

    # going to the leetcode page
    driver.get("https://leetcode.com/")

    # login
    link = WebDriverWait(driver, 30).until(EC.presence_of_element_located(("link text", "Sign in")))
    link.click()
    try:
        # waiting till the login form is loaded
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "id_login")))
    finally:
        # username field
        form_textfield = driver.find_element(By.ID, 'id_login')
        form_textfield.send_keys(args.email)

        # password field
        form_textfield2 = driver.find_element(By.ID, 'id_password')
        form_textfield2.send_keys(args.password)

        # sign in button
        nextButton = driver.find_element(By.ID, 'signin_btn')
        driver.execute_script("arguments[0].click();", nextButton)

        try:
            # waiting till the login is completed
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "ant-dropdown-link")))
        finally:
            print("Login completed...")
            i = 0
            time.sleep(5)

            # going to problem page
            driver.get("https://leetcode.com/problemset/all/")

            # getting the list of links and names of them
            links_to_problems, names = get_links(driver)

            # making the folders and files
            while (i < len(links_to_problems)):

                # getting the name of the problem
                problemname = names[i].split(".")[-1].replace(".", "").strip()

                folder = str(args.path) + "/" + problemname + "/"
                
                if os.path.exists(folder):
                    i = i + 1
                    continue

                os.makedirs(folder)
                driver.get(links_to_problems[i])

                # Grep problem's specifications
                while True:
                    try:
                        # this gets the div with the div of the text of the problem
                        problem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "_1l1MA")))

                        # this gets the question of the problem
                        question = problem.get_attribute("innerHTML")

                        # getting submission button
                        nextButton = WebDriverWait(driver, 30).until(EC.presence_of_element_located(("link text", "Submissions")))
                        nextButton.click()
                        break
                    except:
                        driver.refresh()

                # getting the accepted button
                while(True):
                    try:
                        nextButton = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Accepted')]")))
                        nextButton.click()
                        break
                    except:
                        driver.refresh()

                

                # getting the first accepted submission code
                code_page = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "code")))

                # grepping the language of the code
                while(True):
                    try:
                        lang = code_page.get_attribute("class")
                        break
                    except:
                        continue

                time.sleep(2)

                # setting the extension of the file
                if "language-java" in lang:
                    ext = ".java"
                elif "language-python" in lang:
                    ext = ".py"
                elif "language-cpp" in lang:
                    ext = ".cpp"
                elif "language-c" in lang:
                    ext = ".c"

                # making the file
                f = open(folder + problemname.replace(" ","-").lower() + ext,  'w+')

                # writing the code to the file
                f.write(code_page.text)
                f.flush()
                f.close()

                # making the readme file
                f = open(folder + f"{problemname}.md", "w+")
                f.write(f"# {problemname}" +f"\n### [LeetCode Link]({driver.current_url})\n")
                f.write(question)
                f.flush()
                f.close

                # now we need to commit the changes with proper commit message
                commitmessage = f"Added {problemname} solution"
                os.system("git commit -m " + commitmessage)

                i = i + 1

            driver.close()


def parse_args():
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description='LeetCode to GitHub Exporter.')
    parser.add_argument('email', action='store', help='Email')
    parser.add_argument('password', action='store', help='Password')
    parser.add_argument('path', action='store', help='Path to save files')

    if len(sys.argv) != 4:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()


if __name__ == "__main__":
    main(parse_args())