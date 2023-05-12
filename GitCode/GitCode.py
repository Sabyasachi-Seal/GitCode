# installing dependencies
import os
import time


def get_links(driver):
    # getting the solved problems

    # Status button
    while (True):
        try:
            ff = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Status')]")))
            ff.click()
            break
        except Exception as e:
            driver.refresh()
            time.sleep(5)

    time.sleep(1)

    # Solved button

    while (True):
        try:
            ff = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Solved')]")))
            ff.click()
            break
        except Exception as e:
            driver.refresh()
            time.sleep(5)

    time.sleep(1)

    # need to wait while the page loads, this checks if the reset button is loaded
    WebDriverWait(driver, 30).until(EC.presence_of_element_located(
        (By.XPATH, "//*[contains(text(), 'Reset')]")))
    time.sleep(10)

    list_of_links = []
    list_of_names = []

    page = 1
    breakOut = False

    while (True):

        if (breakOut):
            break
        # getting the list of problems
        print("Page: " + str(page))

        if page != 1:
            while (True):
                try:
                    nextButton = driver.find_elements(
                        By.XPATH, ".//nav[@role = 'navigation']//button[@aria-label='next']")[-1]
                    time.sleep(1)
                    try:
                        nextButton.click()
                    except Exception as e:
                        breakOut = True
                        break
                except Exception as e:
                    print(e)
                    driver.refresh()
                    time.sleep(3)

        ind = 0

        while (ind < len(driver.find_elements(By.XPATH, ".//div[@role = 'rowgroup']//div[@role = 'row']"))):

            # this gets the div of the row
            while (True):
                try:
                    WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                        (By.XPATH, ".//div[@role = 'rowgroup']//div[@role = 'row']")))
                    innerDiv = driver.find_elements(
                        By.XPATH, ".//div[@role = 'rowgroup']//div[@role = 'row']")[ind]
                    WebDriverWait(innerDiv, 30).until(
                        EC.presence_of_element_located((By.XPATH, ".//div[@role = 'cell']")))
                    innerDiv = innerDiv.find_elements(
                        By.XPATH, ".//div[@role = 'cell']")[1]
                    break
                except Exception as e:
                    driver.refresh()
                    time.sleep(5)

            name = innerDiv.text  # this gets the name of the problem

            while (True):
                try:
                    link = WebDriverWait(innerDiv, 30).until(
                        EC.presence_of_element_located((By.TAG_NAME, 'a')))
                    # gets the link of the problem
                    link = link.get_attribute("href")
                    break
                except Exception as e:
                    driver.refresh()
                    time.sleep(5)

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


def acceptAlert(alert):
    try:
        alert.accept()
    except Exception as e:
        pass


def initialiseDriver(option):
    if option == 1:
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    elif option == 2:
        return webdriver.Firefox(service=Service(GeckoDriverManager().install()))


def main(path='.'):
    driver, selected = "", False
    browser_options = '''
    1. Chrome
    2. Firefox
    3. Exit
    '''
    # setting up the driver
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    while not selected:
        print(browser_options)
        option = int(input("-----> "))
        if option == 3:
            print("Exiting, Goodbye from GitCode!")
            exit(0)
        elif not (option == 1 or option == 2):
            print("Invalid Browser Selection!")
            exit(0)
        else:
            driver = initialiseDriver(option)
            print(driver)
            selected = True
    driver.maximize_window()

    # making alert object
    alert = Alert(driver)

    # handling os dir issue
    if path == '':
        path = '.'

    # making the soln folder if it doesnt exists
    if not os.path.exists(path):
        os.makedirs(path)

    # going to the leetcode page
    driver.get("https://leetcode.com/")

    # printing the nessary info for the user not to login
    driver.execute_script(
        "window.alert('Greetings from GitCode! Please do not interact with the browser now.')")
    time.sleep(5)
    acceptAlert(alert=alert)

    # login
    link = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(("link text", "Sign in")))
    link.click()
    try:
        # waiting till the login form is loaded
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "id_login")))
    finally:
        try:
            driver.execute_script(
                "window.alert('Now please login to your account.')")
            time.sleep(5)
            acceptAlert(alert=alert)

            # waiting till the login is completed
            sleepTime = 0
            sleepMax = 180  # 3 mins
            while (len(driver.find_elements(By.XPATH, ".//div[@id = 'navbar-right-container']//div")) <= 1):
                time.sleep(1)
                sleepMax = sleepMax + 1
                if sleepTime > sleepMax:
                    sleepTime = 0
                    driver.refresh()
        finally:
            print("Login completed...")
            driver.execute_script(
                "window.alert('Now sit back and watch GitCode do the work for you!')")
            time.sleep(5)
            acceptAlert(alert=alert)

            i = 0

            # going to problem page
            driver.get("https://leetcode.com/problemset/all/")
            time.sleep(10)

            # getting the list of links and names of them
            links_to_problems, names = get_links(driver)

            # making the folders and files
            while (i < len(links_to_problems)):

                # getting the name of the problem
                problemname = names[i].split(".")[-1].replace(".", "").strip()
                problemnumber = names[i].split(".")[0].strip()

                folder = str(path) + "/" + problemname + "/"

                skipfilename = problemnumber+"-"+problemname.lower().replace(" ", "-")
                print(skipfilename)
                # need to check if the problem is already present from leetcode
                if skipfilename in os.listdir(path):
                    i = i + 1
                    continue

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
                        question = problem.get_attribute("innerHTML").encode('utf-8')
                        question = question.decode('utf-8')
                        break
                    except Exception as e:
                        driver.refresh()
                        time.sleep(2)

                while True:
                    try:
                         # getting submission button
                        nextButton = WebDriverWait(driver, 30).until(EC.presence_of_element_located(("link text", "Submissions")))
                        nextButton.click()
                        break
                    except Exception as e:
                        driver.refresh()
                        time.sleep(2)

                # getting the accepted button
                while (True):
                    try:
                        nextButton = WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Accepted')]")))
                        nextButton.click()
                        break
                    except Exception as e:
                        driver.refresh()
                        time.sleep(2)

                # getting the first accepted submission code
                while (True):
                    try:
                        code_page = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.TAG_NAME, "code")))
                        code = code_page.text
                        break
                    except Exception as e:
                        driver.refresh()
                        time.sleep(2)

                # grepping the language of the code
                while (True):
                    try:
                        lang = code_page.get_attribute("class")
                        break
                    except Exception as e:
                        driver.refresh()
                        time.sleep(2)

                time.sleep(2)

                ext = ""
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
                f = open(folder + problemname.replace(" ",
                         "-").lower() + ext,  'w+', encoding="utf-8")

                # writing the code to the file
                f.write(code)
                f.flush()
                f.close()

                # making the readme file
                f = open(folder + f"README.md", "w+", encoding="utf-8")
                f.write(f"# [{problemname}]({links_to_problems[i]})\n")
                f.write(question)
                f.flush()
                f.close

                os.system(f"git add {path}/")

                # getting the runtime, runtime beats, memory, and memory beats
                while (True):
                    try:
                        # find the details button
                        detailsElement = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Details')]")))
                        # get its parent
                        detailsParent = detailsElement.find_element(By.XPATH, "..")

                        # this is just the runtime text element
                        runtimeElement = WebDriverWait(detailsParent, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Runtime')]")))
                        print(runtimeElement.text)
                        # this is the parent div of the runtime text element
                        runtimeParent = runtimeElement.find_element(By.XPATH, "..")
                        print(runtimeParent.text)
                        # this is the parent div of the parent div of the whole runtime element
                        runtimeClass = runtimeParent.find_element(By.XPATH, "..")
                        print(runtimeClass.text)
                        # this is the beats % for the runtime
                        runtimeBeats = runtimeClass.find_element(By.XPATH, ".//*[contains(text(), 'Beats')]")
                        # this is the parent div of the beats% for the
                        runtimeBeatsParent = runtimeBeats.find_element(By.XPATH, "..")
                        # this is the text of the beats% for the runtime
                        runtimeBeats = runtimeBeatsParent.text.split("\n")[-1]
                        # this is the runtime used
                        runtime = runtimeParent.text.split("\n")[-1].replace(" ", "")

                        # print(runtime, runtimeBeats)

                        # this is just the memory text element
                        memoryElement = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Memory')]")))
                        print(memoryElement.text)
                        # this is the parent div of the memory text element
                        memoryParent = memoryElement.find_element(By.XPATH, "..")
                        print(memoryParent.text)
                        # this is the parent div of the parent div of the whole memory element
                        memoryClass = memoryParent.find_element(By.XPATH, "..")
                        print(memoryClass.text)
                        # this is the beats % for the memory
                        memoryBeats = memoryClass.find_element(By.XPATH, ".//*[contains(text(), 'Beats')]")
                        # this is the parent div of the beats% for the
                        memoryBeatsParent = memoryBeats.find_element(By.XPATH, "..")
                        # this is the text of the beats% for the memory
                        memoryBeats = memoryBeatsParent.text.split("\n")[-1]
                        # this is the memory used
                        memory = memoryParent.text.split("\n")[-1].replace(" ", "")

                        # print(memory, memoryBeats)

                        break

                    except Exception as e:
                        print(e)
                        driver.refresh()
                        time.sleep(5)

                commitMessage = f"Time: {runtime} ({runtimeBeats}) | Memory: {memory} ({memoryBeats}) - GitCode"

                # now we need to commit the changes with proper commit message
                for file in os.listdir(folder):
                    commitFilname = folder.replace(
                        " ", "\ ") + file.replace(" ", "\ ")
                    addMessage = f"git add {commitFilname}"
                    print(addMessage)
                    os.system(addMessage)

                commitMessage = f"git commit -m '{commitMessage}'"
                os.system(commitMessage)

                i = i + 1

            driver.execute_script(
                "window.alert('You solved solutions have been exported to your GitHub repository! Thanks for using GitCode!')")
            time.sleep(5)
            acceptAlert(alert=alert)

            driver.close()


if __name__ == "__main__":
    os.system("clear && pip install -r requirements.txt && git pull && clear")
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.alert import Alert
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support.ui import WebDriverWait
    from webdriver_manager.core.utils import ChromeType
    from webdriver_manager.firefox import GeckoDriverManager
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.support import expected_conditions as EC
    main(path=input("Enter the path to save the files: "))
    # os.system("git push")
