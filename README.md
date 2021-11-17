# TESTS FOR SEAFARERS
## Video Demo: https://youtu.be/kq1zWEG4LO0
## Description:
The main purpose of my project is to help seafarers practice for any upcoming exams, or simply study and learn new stuff.
There are 2 folders in my final project folder, one named *static* and the other named *templates*.
In *static* there is only one file, named *styles.css*, which contains all the information and commands regarding styling of HTML elements.
Although I used **Bootstrap 5**, I included some personal touch. For example, I wanted all *login* and *register* forms to be aligned in the
center of the screen. Each question in tests being generated from the website looks like a separate form, easily distinguished from the others.
That was made by adding borders, fixed width, background color and aligning all the elements inside.

On the other hand, in the templates folder, all of the html files are located.
1. *layout.html* contains all the basic information the website uses. For instance, information such as meta tags, connecting Bootstrap,
linking *styles.css*. In the *<body> tag* of layout.html, you can find the navigation bar, which looks different depending on whether an
user is logged in or not. This is done by using **Jinja** and finally below is the footer.

2. My website is divided into two main views - first when the user is logged in and is viewing his/her history and the second one
is when the user is taking a test. *layout1.html* is the file which sets the basic view of test mode. Same as *layout.html*, in the beginning
*layout1.html* includes **Bootstrap**, sets meta tags and links *styles.css*. Next, the difference with the other layout.html file
is that the main navigation bar is different, and is basically missing.

3. *test1.html* is the main and the most sophisticated of all template files. First and foremost, by using *Jinja*, I have visualised
test and question generation. Depending on whether the user have selected 60 or the full number of question, the page is dynamically
altered. Here, a navigation bar is present, but only to display information regarding number of correct and wrong answers, time remaining.
There is also a submit button, located in the top right corner, which when pressed "sends" the test to user's history. The Javascript
at the beginning of test1.html creates a function to check whether an answer is correct or not. The correct answer is hidden in each
question, the function stores it into a variable. After that, it checks if the value of the selected option matches the value of the
correct answer, the background color of the question becomes green, and if not, color becomes red. At each click on any answer, the
function is called and updates number of wrong and correct answers by using DOM method *queryselectorall* and counting. The next function
implemented in the script part of this html file basically makes a countdown timer of 60 minutes.

4. *login.html* and *register.html* look almost the same. Each HTML visualizes a form where users can input their credentials and
log in or register.

5. *index.html* is the main view of the website when a person logs in. There, a user can see history of previously taken tests.
There is a separate table created in the database connected with this application, which keeps track of each user's tests, correct,
wrong answers, success rate and date and time test was taken.

**application.py** is the backend of my website, where all the magic is happening. At the beginning, I've implemented all the imports
required. Next, application is defined. After that session is configured to use filesystem instead of signed cookies. Then, after
ensuring templates are auto-reloaded and opening database, all the functions "moving" the website, are created.

1. *register* is a function which registers an user. When the user submits the form on the *register.html* then the functions checks
whether there is a username, a password, a confirmation and finally checks if such user already exists in the database. If all checks
are passed, user is returned to *index()* which, on the other hand, calls login function.

2. *login* is similar to register. The function checks the form input fields if are correctly filled and finally searches the
database for a user with these credentials. If all checks are ok, then the user is redirected to the home page, dynamically generated
by *index()*

3. *index()* queries the database for all tests made by the current user and fills the table with all the data.

4. *zavurshi()* defines the action to be executed when pressing the submit button on test mode. In the test1.html there is a form
which contains info about number of correct and wrong answers as well as success rate, but it is hidden. The function gets all that
information and inserts it into a table in the database.

5. *logout()* simply clears the session, thus logging out the user.

.tsv files contain all questions and answers contained in the tests and were used to update the database.

update.py is the Python application which takes a .tsv file and inserts the information in SQL database.