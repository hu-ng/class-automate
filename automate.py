from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
from data_handle import data, StudentData
from env import email_address, pwd


class Seminar:
    def __init__(self, headless=False):
        """
        Logs into Seminar
        """
        self.opts = Options()
        self.opts.headless = headless
        self.opts.add_argument("--enable-automation")
        self.opts.add_argument("--window-size=1900x900")
        self.driver = Chrome(options=self.opts)


    def sign_in(self):
        self.driver.get("http://seminar.minerva.kgi.edu/app")

        # Finds login button and click it
        login = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.ID, "js-google-sign-in"))
        )
        # Wait for Javascript to load
        time.sleep(2)
        login.click()

        # Switch the login pop-up
        WebDriverWait(self.driver, 10).until(EC.number_of_windows_to_be(2))
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[1])

        # Wait until the login window has loaded, select email
        locator_email = "Email" if self.opts.headless else "identifierId"
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
        time.sleep(2)

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


    def create_new_classroom(self, course_name, prof_name, prof_email, student_data=None):
        # Go to "All Events"
        self.driver.get("http://seminar.minerva.kgi.edu/app/all-events")

        print('Going to \"All Events\"')
        WebDriverWait(self.driver, 10).until(EC.title_contains("All Events"))

        # Click button to create new classroom
        print(f"Creating new classroom for {course_name}")
        self.driver.find_element_by_xpath("//button[text()='Create Classroom']").click()

        # Check that the new class page has loaded
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//h2[text()='Class Information']")))

        # Session name
        session_name = f"{course_name} Technical Interview - {student_data.name}"
        class_name_field = self.driver.find_element_by_xpath("//input[@class='value-box']")
        self.driver.execute_script("arguments[0].value = ''", class_name_field)
        class_name_field.send_keys(session_name)
        class_name_field.send_keys(Keys.RETURN)
        print(f"Entered session name: {session_name}")
        self.class_edit_updated()


        # Class date
        date_picker_field = self.driver.find_element_by_xpath("//input[contains(@class, 'hasDatepicker')]")
        self.driver.execute_script("arguments[0].value = ''", date_picker_field)
        date_picker_field.send_keys(student_data.day)
        date_picker_field.send_keys(Keys.RETURN)
        print(f'Picking date {student_data.day}')
        self.class_edit_updated()


        # Class hour picker
        parent_locator_time_hour = "//select[@class='date' and @name='hour']"
        self.driver.find_element_by_xpath(f"{parent_locator_time_hour}").click()
        hour_choice = self.driver.find_element_by_xpath(f"{parent_locator_time_hour}/option[@value='{student_data.time.hour}']")
        hour_choice.click()
        time.sleep(3)
        WebDriverWait(self.driver, 10).until(EC.element_selection_state_to_be(hour_choice, True))

        # Class minute picker
        parent_locator_time_minute = "//select[@class='date' and @name='minute']"
        self.driver.find_element_by_xpath(f"{parent_locator_time_minute}").click()
        minute_choice = self.driver.find_element_by_xpath(f"{parent_locator_time_minute}/option[@value='{student_data.time.minute}']")
        minute_choice.click()
        time.sleep(3)
        WebDriverWait(self.driver, 10).until(EC.element_selection_state_to_be(minute_choice, True))

        # Class AM/PM picker
        parent_locator_time_am_pm = "//select[@class='date' and @name='am-pm']"
        self.driver.find_element_by_xpath(f"{parent_locator_time_am_pm}").click()
        am_pm_choice = self.driver.find_element_by_xpath(f"{parent_locator_time_am_pm}/option[@value='{student_data.am_pm}']")
        am_pm_choice.click()
        time.sleep(3)
        WebDriverWait(self.driver, 10).until(EC.element_selection_state_to_be(am_pm_choice, True))
        print(f"Class time: {student_data.time} {student_data.am_pm}")

        # Click professor field
        time.sleep(5)
        print('Picking professor')
        professor_disp_field = self.driver.find_element_by_css_selector("span.select2-selection__arrow")
        actions = ActionChains(self.driver)
        actions.move_to_element(professor_disp_field).click().perform()

        # Search for professor and select the right one
        parent_locator_professor = "//div[@class='form-wrapper teacher-wrapper']"
        professor_search_field = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, f"{parent_locator_professor}//input[@class='select2-search__field']"))
        ).send_keys(prof_name)

        professor_option = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, f"{parent_locator_professor}//li[contains(text(), '{prof_email}')]"))
        ).click()
        print(f"Selected Prof: {prof_name}, {prof_email}")

        # Student picker
        print('Picking student')
        parent_locator_student = "//div[@class='form-wrapper students-wrapper']"
        student_search_field = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, f"{parent_locator_student}//input")))
        student_search_field.click()
        student_search_field.send_keys(student_data.name)
        print(f"{parent_locator_student}//li[contains(@class, 'select2-results__option') and contains(text(), '{student_data.email}')]")
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, f"{parent_locator_student}//li[contains(@class, 'select2-results__option') and contains(text(), '{student_data.email}')]"))
        ).click()
        

        # Enable recording
        print('Check recording')
        self.driver.find_element_by_xpath("//div[@class='form-wrapper is-record-wrapper']//input").click()

        # Click button to publish class
        print('Publishing class')
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.publish-class"))).click()
        return self.driver.current_url


if __name__ == "__main__":
    client = Seminar(headless=True)
    client.sign_in()
    class_urls = []
    for row in range(data.shape[0]):
        # course_name, prof_name, prof_email, student_data=None
        curr_data = StudentData(data.iloc[row])
        url = client.create_new_classroom(course_name="CS111B",
                                    prof_name="Tambasco",
                                    prof_email="ltambasco@minerva.kgi.edu",
                                    student_data=curr_data)
        class_urls.append(url)
    print(class_urls)