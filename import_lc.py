import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_links(driver):
	time.sleep(2)
	# getting the solved problems

	# Status button
	ff = driver.find_element(By.XPATH, "//*[contains(text(), 'Status')]")
	ff.click()
	time.sleep(2)

	# Solved button
	ff = driver.find_element(By.XPATH, "//*[contains(text(), 'Solved')]")
	ff.click()
	time.sleep(3)

	# making the list as 100 per page
	ff = driver.find_element(By.XPATH, "//*[contains(text(), '50 / page')]")
	ff.click()
	time.sleep(2)
	# selecting 100 per page
	ff = driver.find_element(By.XPATH, "//*[contains(text(), '100 / page')]")
	ff.click()
	time.sleep(2)


	# getting the list of problems
	i = []
	# this is the div of rows
	list_of_problems = driver.find_elements(By.XPATH, "//div[@role = 'rowgroup']")

	for i in list_of_problems:
		innerDiv = i.find_elements(By.XPATH, "//div[@role = 'cell']")[1]
		link = innerDiv.find_element(By.XPATH,'./following::a')
		print(i.text, innerDiv.text, link.text, link.get_attribute('href'))

	
	totalnumber = len(list_of_problems)

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
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
	driver.maximize_window()

	print ("Opening LeetCode...")
	driver.get("https://leetcode.com/")

	print ("Executing login...")
	link = driver.find_element("link text", "Sign in")
	link.click()
	try:
		elem = WebDriverWait(driver, 30).until(
		EC.presence_of_element_located((By.ID, "id_login")) #This is a dummy element
	)
	finally:
	
		form_textfield = driver.find_element(By.ID, 'id_login')
		form_textfield.send_keys(args.email)

		# driver.implicitly_wait(10)
		form_textfield2 = driver.find_element(By.ID, 'id_password')
		form_textfield2.send_keys(args.password)

		# driver.implicitly_wait(10)
		nextButton = driver.find_element(By.ID, 'signin_btn')
		driver.execute_script("arguments[0].click();", nextButton)

		try:
			elem = WebDriverWait(driver, 30).until(
			EC.presence_of_element_located((By.CLASS_NAME, "ant-dropdown-link")))
		finally:
			print ("Login completed...")

			i = 0

			while(True):
				time.sleep(5)
				driver.get("https://leetcode.com/problemset/all/")

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
						time.sleep(2)

						# Grep problem's specifications
						problem = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div[3]")
						text = str(problem.text.encode('ascii', 'ignore').decode('ascii'))
						text = text.replace("\nSubscribe to see which companies asked this question","")
						text = text.replace("\nShow Tags","")
						text = text.replace("\nShow Similar Problems","")

						time.sleep(2)
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
