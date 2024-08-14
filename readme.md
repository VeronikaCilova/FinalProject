# SDA Final Project
# Created by PythonRemoteCZ18 Team 1: Magda & Veronika

## Name:
### Personal Portal (Wingman)

## Brief description:
The goal was to create a website that allows users to enter goals, performance reviews and feedback,
also to display and track relevant performance information and follow up with productivity tasks 
(incl. training's planning). Any registered user can sign up. The users are employees (staff) - leaders and subordinates. 
The website also has a TODO section, that allows users to follow uo on most urgent tasks.

## Technologies:
Python, Django, GIT, HTML, CSS, JavaScript, Selenium

## Basic entities:
![diagram](images/db_wingman.jpg)

## Main System Features:
 - Home page: User registration and login
 - Profile page: User profile/dashboard
 - Goals page: Creating and editing goals
 - Reviews page: Creating and editing reviews
 - Kudos page: Creating, sending and receiving instant feedback
 - Productivity page: Adding and displaying productivity to-do-lists

## Functionalities:
### Homepage
  * login/logout; 
  * registration form to set up the account
  * company banner and Personal Platform description
    ![homepage](images/homepage.jpg)

### Profile (user page)
  * profile presentation
  * information about the employee
  * overview of subordinates
  * overview of accomplished goals
    ![profile](images/profile.jpg)

### Personal goals overview
  * displays list of goals
  * create/edit/delete goals
    ![goals](images/goals.jpg)

### Goal details page
  * displays goals info (incl. deadline, description, priority, status) + update/delete

### Performance reviews
  * displays all reviews (self-reviews & subordinates')
  * add/edit/delete review (text) - self-review
  * add/edit/delete review (text) - leader's review
  * create review page allows users to suggest useful trainings
    ![reviews](images/reviews.jpg)

### Feedback widget
  * enables to add instant feedback(kudos)
    ![kudos](images/kudos.jpg)

### Productivity list
  * displaying to do list
  * enables adding todos
    ![todo](images/todo.jpg)
