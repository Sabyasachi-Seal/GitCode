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
	time.sleep(1)

	# Solved button
	ff = driver.find_element(By.XPATH, "//*[contains(text(), 'Solved')]")
	ff.click()
	time.sleep(1)

	# making the list as 100 per page
	ff = driver.find_element(By.XPATH, "//*[contains(text(), '50 / page')]")
	ff.click()
	time.sleep(1)
	# selecting 100 per page
	ff = driver.find_element(By.XPATH, "//*[contains(text(), '100 / page')]")
	ff.click()
	time.sleep(1)


	# getting the list of problems

	# this is the list of div of rows
	list_of_problems = driver.find_elements(By.XPATH, ".//div[@role = 'rowgroup']//div[@role = 'row']")
	
	list_of_links = []
	list_of_names = []

	for i in list_of_problems:

		# this gets the div of the row
		innerDiv = i.find_elements(By.XPATH, ".//div[@role = 'cell']")[1]
		
		name = innerDiv.text # this gets the name of the problem
		link = innerDiv.find_element(By.TAG_NAME,'a').get_attribute("href") # gets the link of the problem
		
		list_of_links.append(link)
		list_of_names.append(name)
	
	totalnumber = len(list_of_problems)
	print ("Total number of problems: " + str(totalnumber))

	print(list_of_links)
	print(list_of_names)

	return list_of_links[1:], list_of_names


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

		form_textfield2 = driver.find_element(By.ID, 'id_password')
		form_textfield2.send_keys(args.password)

		nextButton = driver.find_element(By.ID, 'signin_btn')
		driver.execute_script("arguments[0].click();", nextButton)

		try:
			# waiting till the login is completed
			WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "ant-dropdown-link")))
		finally:
			print ("Login completed...")
			i = 0

			time.sleep(5)

			driver.get("https://leetcode.com/problemset/all/")

			links_to_problems, names = get_links(driver)

			while (i < len(links_to_problems)):

				problemname = names[i].split(".")[-1].replace(".", "").strip() # getting the name of the problem

				folder = str(args.path) + "/" + problemname + "/"

				if os.path.exists(folder):
					i = i + 1
					continue

				if not os.path.exists(folder):
					os.makedirs(folder)
					driver.get(links_to_problems[i])
					time.sleep(2)

					# Grep problem's specifications
					problem = driver.find_element(By.CLASS_NAME, "_1l1MA") # this gets the div with the div of the text of the problem

					question = str(problem.text.encode('ascii', 'ignore').decode('ascii')) # this gets the question of the problem

					# getting submission button
					nextButton = driver.find_element("link text", "Submissions")
					nextButton.click()
					time.sleep(2)

					# getting the accepted button
					nextButton = driver.find_element(By.XPATH, "//*[contains(text(), 'Accepted')]")
					nextButton.click()
					time.sleep(2)

					# getting the first accepted submission code 
					code_page = driver.find_element(By.TAG_NAME, "code")

					lang = code_page.get_attribute("class")
					print(lang)

					time.sleep(5)

					if "language-java" in lang:
						ext = ".java"
					elif "language-python" in lang:
						ext = ".py"
					elif "language-cpp" in lang:
						ext = ".cpp"
					elif "language-c" in lang:
						ext = ".c"

					f = open(folder + problemname.replace(" ", "-").lower() + ext,  'w+')

					f.write(code_page.text)
					f.flush()
					f.close()

					f = open(folder + f"{problemname}.md", "w+")
					f.write(f"# {problemname}" + "\n## From: " + driver.current_url + "\n\n")
					f.write(question)
					f.flush()
					f.close

				i = i + 1
			driver.close()

def parse_args():
	import argparse
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
