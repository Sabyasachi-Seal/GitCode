import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By


def get_links(driver):
	# Problem page
	total = driver.find_element(By.XPATH, "//*[@id='brief_stats']/p/strong").text
	totalnumber = int(total.split(' ')[0])
	currentnumber = 0
	##print "Problems found: " + str(totalnumber)

	ff = Select(search_box = driver.find_element("name", "filterchosen"))
	ff.select_by_visible_text("Solved Problems")
	list_of_links = []
	list_of_problems = search_box = driver.find_element("name", "problemList").\
							  find_element_by_tag_name("tbody").\
							  find_elements_by_tag_name("tr")
	for row in list_of_problems:
		check = row.find_element_by_tag_name("td")
		if check.is_displayed():
			currentnumber = currentnumber + 1
			list_of_links.append(row.find_element_by_tag_name("a"));
			sys.stdout.write("[ " + str(float(currentnumber)/float(totalnumber)*100)[:5] + "% ] Loading next problem... \r")
			sys.stdout.flush()
	return list_of_links


def print_links(driver):
	list_of_links = get_links(driver)
	for a in list_of_links:
		print (a.text)


def main(args):
	chromedriver = "<PATH_TO_CHROMEDRIVER>/chromedriver" # Set this to your chromedriver's location
	os.environ["webdriver.chrome.driver"] = chromedriver
	driver = webdriver.Chrome(chromedriver)
	driver.maximize_window()

	print ("Opening LeetCode...")
	driver.get("https://leetcode.com/")

	print ("Executing login...")
	link = driver.find_element("link text", "Sign in")
	link.click()
	driver.implicitly_wait(10)
	
	form_textfield = driver.find_element(By.ID, 'id_login')
	form_textfield.send_keys(args.email)

	driver.implicitly_wait(10)
	form_textfield2 = driver.find_element(By.ID, 'id_password')
	form_textfield2.send_keys(args.password)

	driver.implicitly_wait(10)
	nextButton = driver.find_element(By.ID, 'signin_btn')
	driver.execute_script("arguments[0].click();", nextButton)

	print ("Login completed...")
	print ("Loading new problems...")

	i = 0
	driver.implicitly_wait(2000)

	while(True):
		driver.get("https://leetcode.com/problemset/algorithms/#")
		driver.implicitly_wait(2000)
		links_to_problems = get_links(driver)
		while (i < len(links_to_problems)):
			filename = links_to_problems[i].text
			folder = str(args.path) + "/" + filename + "/"
			if os.path.exists(folder):
				i = i + 1
				continue
			if not os.path.exists(folder):
				os.makedirs(folder)
				links_to_problems[i].click()
				driver.implicitly_wait(2000)
				# Grep problem's specifications
				problem = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div[3]")
				text = str(problem.text.encode('ascii', 'ignore').decode('ascii'))
				text = text.replace("\nSubscribe to see which companies asked this question","")
				text = text.replace("\nShow Tags","")
				text = text.replace("\nShow Similar Problems","")
				driver.implicitly_wait(2000)
				nextButton = driver.find_element("link text", "My Submissions")
				nextButton.click()
				driver.implicitly_wait(10000)
				nextButton = driver.find_element(By.PARTIAL_LINK_TEXT, 'Accepted')
				nextButton.click()
				time.sleep(5)
				code_page = driver.find_element_by_tag_name("body").text
				time.sleep(5)
				result = code_page[code_page.find("class "):code_page.find("Back to problem")]
				#print "== " + str(i+1) + "/" + str(len(links_to_problems)) + " == " + filename
				# #print result
				if "Language: python" in code_page:
					f = open(folder + "main.py", 'w+')
				elif "Language: java" in code_page:
					f = open(folder + "/main.java", 'w+')
				f.write(result)
				f.flush()
				f.close()
				f = open(folder + "requirements.txt", "w+")
				f.write(filename + "\nFrom: " + driver.current_url + "\n\n")
				f.write(text)
				f.flush()
				f.close
				break
		i = i + 1
		if (i >= len(links_to_problems)):
			break
	driver.close()

def parse_args():
    import argparse
    import itertools
    import sys

    parser = argparse.ArgumentParser(description='LeetCode - Google Login script.')
    parser.add_argument('email', action='store', help='email')
    parser.add_argument('password', action='store', help='password')
    parser.add_argument('path', action='store', help='Path to save files')
    if len(sys.argv)!=4:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()

if __name__ == "__main__":
    main(parse_args())
