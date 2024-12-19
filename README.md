# WonderIndia - Explore India's Culture

## Overview

**WonderIndia** is a web application built to explore the rich cultural heritage of India. It allows users to click on different states of India and learn about their famous foods, places, and user reviews. The application also includes a review submission feature and a contact us form for assistance.

### Features
- **State Exploration:** Users can explore famous places and foods from various states of India.
- **Review System:** Users can submit their reviews for different tourist destinations.
- **Contact Us Form:** Users can submit queries and issues.
- **Carousel for Reviews:** Display of reviews using a Bootstrap carousel for easy browsing.

## Technologies Used
- **Flask:** For building the web application.
- **Bootstrap:** For responsive design and components.
- **HTML/CSS:** For the structure and styling of the website.
- **Python:** For backend logic and server-side operations.
- **MySQL:** For storing state, place, and review data.

## Installation and Setup

### Prerequisites
- **Python 3.x**
- **Flask**: Install Flask using `pip install flask`.
- **MySQL**: You need a MySQL database setup.

### Setup Steps

#### 1. **Clone the Repository**
Clone the repository to your local machine:
    ```bash
      git clone https://github.com/bharani-reddy/wanderIndida-website.git
#### 2. Install Dependencies
Install the necessary Python dependencies:
     ```bash
        pip install flask
        pip install mysql-connector
#### 3. Set Up the Database
Create a MySQL database and import the schema to set up the necessary tables. This will store the data for states, places, foods, and reviews.

#### 4. Run the Application in Jupyter Notebook
This project is intended to be run in a Jupyter Notebook environment. To run it:

  - Open Jupyter Notebook on your local machine.
  - Navigate to the folder where the project files are located.
  - Open a new notebook or an existing notebook where you want to run the application.
  - Run the following command to start the Flask application directly from Jupyter:
    ```bash
      !flask run
This will start the Flask app and it will be accessible at http://localhost:5000.
### Code Explanation
## 1. HTML Template
The HTML structure is divided into multiple sections to handle different views and interactions:

- **Header Section:** Displays the title of the app and an introductory message.
- **State List:** Displays clickable cards for each state. When clicked, it takes the user to the state's specific page showing famous foods, places, and reviews.
- **State Content:** Displays the state's name, description, famous foods, and famous places.
- **Reviews Section:** Displays user reviews for the selected state. The reviews are shown in a carousel for easy navigation.
- **Add Review Form:** Allows users to submit their own reviews for a state and its places. Includes dropdowns for selecting state and place, a review rating, and the reviewer's name.
- **Contact Us Section:** Allows users to contact the support team by submitting their name, email, and issue description. 
## 2. Flask Routes
- **/ (Home Page):** The homepage that shows all the states and allows users to click on them for further exploration.
- **/<state_name> (State Page):** Displays detailed information about the selected state, including famous foods, places, and reviews.
- **/api/add_review (Add Review API):** Handles form submissions for adding a new review for a state/place. The review is then saved to the database.
## 3. Backend Logic
- **Database Connection:** The app connects to a MySQL database using the get_db_connection() function, which returns a connection object.
- **Review Submission:** When a user submits a review, the data is sent to the /api/add_review endpoint via a POST request. This data is then inserted into the database.
- **Contact Form:** The contact form sends a POST request to the backend, and the issue details are submitted via email (not implemented in full here but can be added using a service like SendGrid or SMTP).
## 4. JavaScript
- **State Dropdown Update:** The JavaScript listens for a change in the state dropdown and dynamically updates the places dropdown based on the selected state.
- **Review Submission:** The review submission button triggers a POST request to add the review to the database, with validation to ensure all required fields are filled out.
- **Contact Us Submission:** The contact form sends a POST request to submit the issue. Upon successful submission, it resets the form and shows a success message.
## 5. CSS Styling
- The application uses Bootstrap for a responsive layout and basic styles.
- Custom CSS is applied to enhance the user experience with hover effects on the state cards and styled review items and forms.
### Database Schema
The app requires the following tables in the MySQL database:

- **states:** Stores the state name and description.
- **places:** Stores the name and description of places within a state.
- **foods:** Stores the name, description, and image of famous foods for each state.
- **reviews:** Stores the reviews submitted by users, including the state name, place name, review, reviewer's name, and the date/time of the review.
Example schema for reviews:
    ```bash
      CREATE TABLE reviews (
          id INT AUTO_INCREMENT PRIMARY KEY,
          state_name VARCHAR(255) NOT NULL,
          place_name VARCHAR(255) NOT NULL,
          review TEXT,
          reviewer_name VARCHAR(255),
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      );
### Usage
- **Exploring States**
On the homepage, users can click on any state to explore its famous foods, places, and user reviews.
- **Submitting Reviews**
Users can submit a review for a state/place by filling out the review form. After submitting, the review is added to the database and shown on the state page.
- **Contacting Support**
Users can contact the support team via the "Contact Us" form, which sends their query to the support team.
- **Contributions**
If you'd like to contribute to this project, feel free to submit a pull request or open an issue for discussion. Contributions are always welcome!

https://drive.google.com/file/d/1dzQnuiePeUqRdz2p2UN-5Ub8DCHi2TND/view?usp=sharing
