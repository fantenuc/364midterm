SI364Midterm - Frankie Antenucci
My application uses the News API to allow the user to enter a topic they would like to receive article headlines about. The users of the application, the search terms entered, as well as the headlines returned are all entered into a database. The user can then view all of the users of the application, and the headlines that are returned in the corresponding routes. The user can also rate a news source of their choosing and that data is entered into the database, as well as displayed on the page. There is a "leave a review" section of the application where the users can leave their comments about their experience with the application and if they would use the application again.


ALL ROUTES
http://localhost:5000/ -> base.html
http://localhost:5000/names -> name_example.html
http://localhost:5000/headlines -> all_headlines.html
http://localhost:5000/rate_sources -> rate_sources.html
http://localhost:5000/comments -> leave_comments.html
http://localhost:5000/view_comments -> comments.html


THINGS I COMPLETED (ALL (bolded) - including extra 200 points)

Ensure that the SI364midterm.py file has all the setup (app.config values, import statements, code to run the app if that file is run, etc) necessary to run the Flask application, and the application runs correctly on http://localhost:5000 (and the other routes you set up)
Add navigation in base.html with links (using a href tags) that lead to every other viewable page in the application. (e.g. in the lecture examples from the Feb 9 lecture, like this )
Ensure that all templates in the application inherit (using template inheritance, with extends) from base.html and include at least one additional block.
Include at least 2 additional template .html files we did not provide.
At least one additional template with a Jinja template for loop and at least one additional template with a Jinja template conditional.
These could be in the same template, and could be 1 of the 2 additional template files.
At least one errorhandler for a 404 error and a corresponding template.
At least one request to a REST API that is based on data submitted in a WTForm.
At least one additional (not provided) WTForm that sends data with a GET request to a new page.
At least one additional (not provided) WTForm that sends data with a POST request to the same page.
At least one custom validator for a field in a WTForm.
At least 2 additional model classes.
Have a one:many relationship that works properly built between 2 of your models.
Successfully save data to each table.
Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for).
Query data using an .all() method in at least one view function and send the results of that query to a template.
Include at least one use of redirect. (HINT: This should probably happen in the view function where data is posted...)
Include at least one use of url_for. (HINT: This could happen where you render a form...)
Have at least 3 view functions that are not included with the code we have provided. (But you may have more! Make sure you include ALL view functions in the app in the documentation and ALL pages in the app in the navigation links of base.html.)

Additional Requirements for an additional 200 points (to reach 100%) -- an app with extra functionality!

(100 points) Include an additional model class (to make at least 4 total in the application) with at least 3 columns. Save data to it AND query data from it; use the data you query in a view-function, and as a result of querying that data, something should show up in a view. (The data itself should show up, OR the result of a request made with the data should show up.)

(100 points) Write code in your Python file that will allow a user to submit duplicate data to a form, but will not save duplicate data (like the same user should not be able to submit the exact same tweet text for HW3).
