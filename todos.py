from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


def verifyText(locator, expectedtext, testname, logfile):
    elemtext = driver.find_element(*locator).text
    if elemtext == expectedtext:
        logfile.write("Test {} passed\n".format(testname))
    else:
        logfile.write(
            "Test {0} failed. element expected text should be {1} but it is {2}\n".format(testname, expectedtext,
                                                                                        elemtext))
        raise Exception
    return


def verifyNotPresent(locator, testname, logfile):
    elements = driver.find_elements(*locator)
    if len(elements) == 0:
        logfile.write("test {} passed\n".format(testname))
    else:
        logfile.write("test {} failed\n".format(testname))
        raise Exception("element present")


if __name__ == '__main__':
    # constants
    task = "sanity"
    timeout = 5
    headertext = "todos"
    url = "http://todomvc.com/"
    # locators
    headerlocator = (By.XPATH, "//h1")
    todolist = "//ul[@id='todo-list']"
    todo_list_items = todolist + "/li"
    firstlocatorstring = "{0}[1]".format(todo_list_items)
    firsttasklocator = (By.XPATH, firstlocatorstring)
    selectstrings = "//a[@href='{}']"
    activebtn = (By.XPATH, selectstrings.format("#/active"))
    completedbtn = (By.XPATH, selectstrings.format("#/completed"))
    allbtn = (By.XPATH, selectstrings.format("#/"))
    derstroy_button = "//input[@type='checkbox']"
    taskinputlocator = (By.ID, "new-todo")
    clearLocator = (By.ID, "clear-completed")
    # test
    logfile = open('testlog.txt', 'w')
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    driver.find_element_by_link_text("AngularJS").click()
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(headerlocator))
    verifyText(headerlocator, headertext, "Header text test", logfile)
    driver.find_element(*taskinputlocator).send_keys(task + "\n")
    verifyText(firsttasklocator, task, "add task sanity test", logfile)
    driver.find_element(*activebtn).click()
    verifyText(firsttasklocator, task, "verify text in active section test", logfile)
    driver.find_element(*(By.XPATH, "{0}{1}".format(firstlocatorstring, derstroy_button))).click()
    driver.find_element(*completedbtn).click()
    verifyText(firsttasklocator, task, "verify text in completed section test", logfile)
    driver.find_element(*clearLocator).click()
    verifyNotPresent(firsttasklocator, "delete task test", logfile)
    logfile.close()
    time.sleep(3)
    driver.quit()



