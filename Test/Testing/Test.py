from lib2to3.pgen2 import driver
from time import time
from selenium import webdriver
import time
driver = webdriver.Chrome(
    r"D:\BE\BE Project\SEM-7-Progress\LoanApprovalStatus\Test\Testing\chromedriver.exe")
driver.get("http://127.0.0.1:5000/")
time.sleep(3)
driver.close()
