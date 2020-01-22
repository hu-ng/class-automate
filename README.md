# Automatic classroom creation!

This project was created out of the need to make my life as a Teaching Assistant easier. At the end of each CS111B (Linear Algebra) course, students have to take online interviews with the professors as part of their final assessments. For students to have these interviews, I need to create dozens upon dozens of virtual classrooms on a the proprietary learning platform that my school uses for **all** academic activity (it's pretty cool, check it [out](https://www.minerva.kgi.edu/)!). 

It's a very long and menial task, consist of going through CSV files and manual data entry into the platform. All of this means that it is the perfect job for some Python action!

Essentially, the project uses Selenium and the Chrome WebDriver to perform actions on the browser using code. I used it to log in the platform and created a function to generate a classroom from a pre-populated CSV file. For every row in the CSV, the script creates a classroom and returns its URL. All I need to then is to store the URLs in the CSV and upload it, so that students know which classrooms they need to enter for their scheduled interviews!

I imagine it would have been much easier for the product team behind the platform to create a native classroom creation functionality, but until that becomes a reality, this project can help future TAs like myself save *a lot* of time.
