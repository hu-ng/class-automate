from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
from env import email_address, pwd


class Seminar:
  def __init__(self):
    """
    Logs into Seminar
    """
    self.opts = Options()
    self.opts.headless = True
    self.opts.add_argument("--enable-automation")
    self.opts.add_argument("--window-size=1600x900")
    self.driver = Chrome(options=self.opts)


  def sign_in(self):
    self.driver.get("http://seminar.minerva.kgi.edu/app")

    # Finds login button and click it
    login = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.ID, "js-google-sign-in"))
    )
    # Wait for JavaScript to load
    time.sleep(2)
    login.click()

    # Switch the login pop-up
    WebDriverWait(self.driver, 10).until(EC.number_of_windows_to_be(2))
    handles = self.driver.window_handles
    self.driver.switch_to.window(handles[1])

    locator_email = "Email" if self.opts.headless else "identifierId"
    # Wait until the login window has loaded, select email
    email = WebDriverWait(self.driver, 5).until(
      EC.presence_of_element_located((By.ID, locator_email))
    )

    # Send email
    print("Entering email...")
    email.send_keys(email_address)

    # Click next
    locator_next = "next" if self.opts.headless else "identifierNext"
    self.driver.find_element_by_id(locator_next).click()

    # Find password
    locator_pwd = "Passwd" if self.opts.headless else "password"
    if self.opts.headless:
      password = self.driver.find_element_by_id(locator_pwd)
    else:
      password = WebDriverWait(self.driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='password']/div[1]/div/div[1]/input"))
      )

    # Enter password
    print("Entering password...")
    password.send_keys(pwd)

    # Sign In
    print("Signing in...")
    locator_signin = "signIn" if self.opts.headless else "passwordNext"
    self.driver.find_element_by_id(locator_signin).click()

    # You're in Seminar!
    self.driver.switch_to.window(handles[0])

    WebDriverWait(self.driver, 10).until(EC.title_contains("Minerva"))
    self.driver = self.driver
    print("Logged in!")

  
  def class_edit_updated(self):
    update_notice_locator = (By.CSS_SELECTOR, "div.generic-message-view > div")
    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(update_notice_locator))
    WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element(update_notice_locator, "was updated"))
    print("Change was updated")
  
  
  def create_new_classroom(self, data=None):
    # class name, class date, class time, instructor name, instructor email, student name, student email 
    # Go to "All Events"
    self.driver.get("http://seminar.minerva.kgi.edu/app/all-events")

    print('Going to \"All Events\"')
    WebDriverWait(self.driver, 10).until(EC.title_contains("All Events"))

    # Click button to create new classroom
    print("Creating new classroom...")
    self.driver.find_element_by_xpath("//button[text()='Create Classroom']").click()

    # Check that the new class page has loaded
    WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//h2[text()='Class Information']")))

    # Class name: test = CS111 Test 2
    print("Entering class name")
    class_name_field = self.driver.find_element_by_xpath("//input[@class='value-box']")
    self.driver.execute_script("arguments[0].value = ''", class_name_field)
    class_name_field.send_keys("CS111 Test 8")
    class_name_field.send_keys(Keys.RETURN)
    self.class_edit_updated()


    # Class date: test = 1/29/2020
    print('Picking date')
    date_picker_field = self.driver.find_element_by_xpath("//input[contains(@class, 'hasDatepicker')]")
    self.driver.execute_script("arguments[0].value = ''", date_picker_field)
    date_picker_field.send_keys("1/29/2020")
    date_picker_field.send_keys(Keys.RETURN)
    self.class_edit_updated()


    # Class hour picker: test = 5
    print('Hours')
    parent_locator_time_hour = "//select[@class='date' and @name='hour']"
    self.driver.find_element_by_xpath(f"{parent_locator_time_hour}").click()
    hour_choice = self.driver.find_element_by_xpath(f"{parent_locator_time_hour}/option[@value='{5}']")
    hour_choice.click()
    time.sleep(3)
    WebDriverWait(self.driver, 10).until(EC.element_selection_state_to_be(hour_choice, True))

    # Class minute picker: test = 30
    print("Minute")
    parent_locator_time_minute = "//select[@class='date' and @name='minute']"
    self.driver.find_element_by_xpath(f"{parent_locator_time_minute}").click()
    minute_choice = self.driver.find_element_by_xpath(f"{parent_locator_time_minute}/option[@value='{30}']")
    minute_choice.click()
    time.sleep(3)
    WebDriverWait(self.driver, 10).until(EC.element_selection_state_to_be(minute_choice, True))

    # Class AM/PM picker: test = am
    print("AM/PM")
    parent_locator_time_am_pm = "//select[@class='date' and @name='am-pm']"
    self.driver.find_element_by_xpath(f"{parent_locator_time_am_pm}").click()
    am_pm_choice = self.driver.find_element_by_xpath(f"{parent_locator_time_am_pm}/option[@value='{'am'}']")
    am_pm_choice.click()
    time.sleep(3)
    WebDriverWait(self.driver, 10).until(EC.element_selection_state_to_be(am_pm_choice, True))

    # Finding professor
    # Click to select professor box
    time.sleep(5)
    print('Picking professor')
    professor_disp_field = self.driver.find_element_by_css_selector("span.select2-selection__arrow")
    actions = ActionChains(self.driver)
    actions.move_to_element(professor_disp_field).click().perform()

    # Search for professor and select the right one
    parent_locator_professor = "//div[@class='form-wrapper teacher-wrapper']"
    professor_search_field = WebDriverWait(self.driver, 5).until(
      EC.presence_of_element_located((By.XPATH, f"{parent_locator_professor}//input[@class='select2-search__field']"))
    ).send_keys("Tambasco")

    professor_option = WebDriverWait(self.driver, 5).until(
      EC.presence_of_element_located((By.XPATH, f"{parent_locator_professor}//li[contains(text(), '{'tambasco'}')]"))
    ).click()

    # Student picker: test = Hai
    print('Picking student')
    parent_locator_student = "//div[@class='form-wrapper students-wrapper']"
    student_search_field = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, f"{parent_locator_student}//input")))
    student_search_field.click()
    student_search_field.send_keys("hai")
    WebDriverWait(self.driver, 5).until(
      EC.presence_of_element_located((By.XPATH, f"{parent_locator_student}//li[contains(@class, 'select2-results__option') and contains(text(), '{'danghoang'}')]"))
    ).click()

    # Enable recording
    print('Check recording')
    self.driver.find_element_by_xpath("//div[@class='form-wrapper is-record-wrapper']//input").click()

    # Click button to publish class
    print('Publishing class')
    publish_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.publish-class"))).click()
    return self.driver.current_url


client = Seminar()
client.sign_in()
client.create_new_classroom()

