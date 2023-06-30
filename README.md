# Final Project

## Introduction
The goal of this project is to demonstrate how an exam platform could be implemented to help people practice for university entrance exams. The platform is based on a web application that allows collaborators (people authorized by the administrator) to create questions and explanations for the exams, and students to practice the exams and check their results. It also provides information about the universities and the exams.

## Distinctiveness and Complexity
This project's extensive and fully functional web application, which enables users to interact with the database in a variety of ways, is one of the important elements that distinguish it from other projects in the course. There are 21 different models in the database itself, offering a wide range of possibilities for producing, organizing, and managing data.

In addition to its extensive database capabilities, the project is also highly complex, with a wide range of features and functionalities that make it a versatile tool for a variety of different use cases. Users can create exams, questions, answers, and explanations, and filter them in a variety of different ways, such as choosing only questions with answers or questions with no answers. The platform can meet the needs of a wide range of users because of its different user categories, which include administrators, collaborators, and students.

Built with the web development technologies learned in the course, including Django on the backend and Javascript on the frontend, this web application is also fully mobile responsive, ensuring that users can access and utilize the platform from virtually any device. All of these features work together to create a robust and comprehensive exam platform that is truly distinctive and complex.

## Project Structure
Using Django, Javascript, Bootstrap, and CSS, I created my web application. The project's structure is as follows:

### Exams
The exams section is where users can view all of the exams sorted by the name of the universities that have been created and are active.
- The exams can only be created by the administrator and he can also designate collaborators to edit the exams.
- By clicking on the university's name, the user can see the university's careers, the available exams, and related links.
- The exams view only shows 10 universities per page; the user can navigate through the pages.

### Exam
The exam section is where users can view the questions of the exam selected and take the exam.
- The exam can only be taken by students.
- The exam can only be edited by collaborators and administrators.
- The exam can be taken how many times the user (students) wants.
- The exam questions are sorted by order number.
- The question can be filtered using the following options:
    - Sin responder: Questions without answers.
    - Respondidas: Questions with answers.
    - Pendientes: Questions that the user has marked as pending.
    - Todas: All the questions.
- This section has an index to navigate through the questions.
- The time is shown in the top left corner and it's updated every second.
- If the user needed more time, he can keep answering the questions and later on submit the exam.

### Exam Result
The exam result section is where users can see the result of the exam taken and the explanation of each question.
- The exam result can only be seen by students.
- The question can be filtered using the following options:
    - Correctas: Questions that the user answered correctly.
    - Incorrectas: Questions that the user answered incorrectly.
    - Todas: All the questions.
- This section has an index to navigate through the questions.

### Exam Edition
The exam edition section is where collaborators can edit or create the questions of the exam selected.
- The exam edition can only be seen by collaborators.
- This section shows forms to edit or create questions, answers, and explanations.
- The options for the questions can be text or images.
- The questions can be filtered using the following options:
    - Fecha de Creación: Questions are ordered by creation date.
    - Categorias y Subcategorias: Questions are ordered by category and subcategory.
    - Número de Orden: Questions are ordered by the order number.
- This section has an index to navigate through the questions.
- The collaborators can see a preview of the question before saving it.

### Profile
The profile section is where users can see their information related to the platform.
- Depending on the user, the information shown is different.
    - Administrators: None.
    - Collaborators: The exams that he can edit.
    - Students: The exams that he has taken.
- The profile view only shows 10 exams per page; the user can navigate through the pages.

## Files and Directories
The principal files and directories are the following:

<!-- Table with 3 columns using html-->
<table>
    <tr>
        <th>Directory</th>
        <th>File / Directory</th>
        <th>Description</th>
    </tr>
    <tr>
        <td rowspan="6">\Project\static\Project</td>
        <td>\Images</td>
        <td>Images stored.</td>
    </tr>
    <tr>
        <td>\SVGs</td>
        <td>SVGs stored.</td>
    </tr>
    <tr>
        <td>exam_edit.js</td>
        <td>Makes the exam_edit page work correctly.</td>
    </tr>
    <tr>
        <td>exam_result.js</td>
        <td>Makes the exam_result page work correctly.</td>
    </tr>
    <tr>
        <td>exam.js</td>
        <td>Makes the exam page work correctly.</td>
    </tr>
    <tr>
        <td>styles.css</td>
        <td>Helps with the style of all the pages.</td>
    </tr>
    <tr>
        <td rowspan="9">\Project\Templates\Project</td>
        <td>exam_edit.html</td>
        <td>It shows the forms to edit or create any question for the exam selected.</td>
    </tr>
    <tr>
        <td>exam_result.html</td>
        <td>It shows the result of the test taken by the student and each question has its explanation.</td>
    </tr>
    <tr>
        <td>exam.html</td>
        <td>View of the exam selected.</td>
    </tr>
    <tr>
        <td>exams.html</td>
        <td>View of all exams sorted by the name of the universities.</td>
    </tr>
    <tr>
        <td>index.html</td>
        <td>View of the home page.</td>
    </tr>
    <tr>
        <td>layout.html</td>
        <td>The basic structure for all the pages.</td>
    </tr>
    <tr>
        <td>login.html</td>
        <td>View of the login page.</td>
    </tr>
    <tr>
        <td>profile.html</td>
        <td>View of the user's profile.</td>
    </tr>
    <tr>
        <td>register.html</td>
        <td>View of the registration page.</td>
    </tr>
</table>

## How to Run
To run the project, you need to have Python 3.10 and Django 4.1.3 installed.

In your terminal, `cd` into the `FINAL_PROJECT` directory.
Then run the following commands:
```bash
python manage.py makemigrations Project
python manage.py migrate
python manage.py runserver
```
## Additional Information
- The images for the questions and explanations are stored as URLs because they are meant to be stored in a cloud storage service.
- I modified de admin view to make it more user-friendly.
- The options of the questions are like that due to the fact that mostly in Peru the questions of university exams are multiple-choice options with 4 options and one correct answer.
- I added MathJax to the project to make it possible to write mathematical formulas in the web application.
