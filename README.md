# Automatic classroom creation!
This project was created out of the need to make my life as a Teaching Assistant easier. At the end of each CS111B (Linear Algebra) course, students have to take online interviews with the professors as part of their final assessments. For students to have these interviews, I need to create dozens upon dozens of virtual classrooms on a the proprietary learning platform that my school uses for **all** academic activity (it's pretty cool, check it [out](https://www.minerva.kgi.edu/)!). 

It's a very long and menial task, consist of going through CSV files and manual data entry into the platform. All of this means that it is the perfect job for some Python action!

Essentially, the project uses Selenium and the Chrome WebDriver to perform actions on the browser using code. I used it to log in the platform and created a function to generate a classroom from a pre-populated CSV file. For every row in the CSV, the script creates a classroom and returns its URL. All I need to then is to store the URLs in the CSV and upload it, so that students know which classrooms they need to enter for their scheduled interviews!

I imagine it would have been much easier for the product team behind the platform to create a native classroom creation functionality, but until that becomes a reality, this project can help TAs like myself save *a lot* of time.

## Setting up (For Professors and future TAs)
- Make sure to have Python installed
- It's best to use [virtualenv](https://virtualenv.pypa.io/en/latest/) to create a virtual environment and isolate this project from the rest of your system, but it is fine if you choose not to do so.
- Navigate to the project folder and run `pip install -r requirements.txt` to download necessary packages
- IMPORTANT: Download the [Chrome WebDriver](https://chromedriver.chromium.org/downloads) and place the `.exe` file in your PATH. I placed in the `Scripts` directory of my virtual Python environment. You need the WebDriver to essentially use Chrome from the command line.
- Create an `env.py` file and enter your *@minerva.kgi.edu* credentials in the following format
```python
email_address = YOUR EMAIL
pwd = YOUR PASSWORD
```
- Have the CSV file with student data in the same directory
- To execute the script, run `python automate.py NAME_OF_CSV_FILE.csv`
