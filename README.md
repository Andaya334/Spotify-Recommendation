# Spotify-Recommendation
Machine Learning Project along with EDA and database management

This project produces a music recommendation system.

### back-end

Database: Created in Snowflake via python jupyter notebook using query SQL language to import data from csv to tables and columns within the database. Allows for smooth access to necessary data and allows for data adjustment or addition into the data warehouse.

API: created and powered using a Flask Python powered py script to connect the database to an api to ensure ease of access to the data stored within the data warehouse. Allows for the machine learning script to call information. In addition, this flask was implemented into Google Cloud Platform to create a url based api to create a channel for any user with access to the url to call the information from the data warehouse. This additional layer allows for more data insights into the quantity of calls to the snowflake are done and what specific information is being utilized from the warehouse.

Machine Learning: A python script was constructed utilizing sklearn library to create a music recommendation system that recommends ten songs when a specific song is inputted by the user based on genre, and other key features. the unique aspect si that the script calls on certain features of the database to have a unique recommendation based on mood such as danceability, tempo, likeness, and popularity.

### front-end

API: Another flask-powered api py script was created to create GUI (Graphic user-interface) for user engagement with the application. Unique features include slide bars for users to adjust the music recommendation based on their mood.

GUI: The user-interface has green and black colors to pay homage to the data's collection through Spotify. The slide bars are adjustable by user.

Tableau: Insights about the data were also explained through a Tableau dashboard to explain in detail of the attributes of each section of the features and data.

Power Point: Breaks down what each section explains in the project and how this project would benefit specific audiences such as the general music listener, music businesses and competitors, and Spotify.