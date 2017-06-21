# **SphinxCAPT.org LEADERBOARD**
### Overview
In this project we are designing a FLASK based Web App to maintain Leaderboards for [SphinxCAPT.org](http://SphinxCAPT.org).
The app is based on the REST design with inherent security infrastructure. This project is being maintained as part of the Google Summer of Code 2017.
### Background
This project was envisaged in order to provide developers and volunteers with a one-stop- solution for managing and tracking donations and details of prospective donors for the SphinxCapt project at CMU. The project included a leaderboard of Donor, which is our special way of thanking donors who are supporting the project. The project also provides a workflow to the project members and volunteers to log telephonic and email correspondence with all donors. 
### Requirements
* **Backend**
    * Python 3
    * Flask
    * Pickle
* **Frontend**
    * Web Browser with HTML5
    * Javascript

### Installation
* **Install Python 2.7** - In case Python 2.7 is not already installed on your computer you need to install it. You can refer to these tutorial videos for help.
    * Windows Install 
    
    [![Python 2.7 Windows Install](https://img.youtube.com/vi/QYUBz4mrnFU/0.jpg)](https://www.youtube.com/watch?v=QYUBz4mrnFU)
    
    * Ubuntu Install
    
        Python 2.7 is installed by default in case of Ubuntu. If you are using some other flavour of Debian or a minimal install version then you need to install Python 2.7 seperately. You can also confirm the default Python version using the following command
        > python -V
       
       In case you cannot find Python 2.7 on your PC, you can use the following video tutorial to install.
       
       [![Python 2.7 Ubuntu Install](https://img.youtube.com/vi/MH4anq35I4o/0.jpg)](https://www.youtube.com/watch?v=MH4anq35I4o)
    * Virtual Environment Install - In case you wish to execute the code in a Python Virtual Environment (VirtualEnv) you can use the tutorial below.
     
        [Python Virtual Environment Tutorial](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/)
* **Package Install** - The required Python packages can be installed using the following commands
    > pip install -r requirements.txt
### Execution
The Donor Management Workflow Flask application can be executed by the following command
 > python leaderboard.py
## Donor Leaderboard
 The Donor Leaderboard gives the details of all donors who have helped support this project through donations. These donations are used to buy Amazon Mechanical Turk Credits for the project. The Donor Leaderboard lists donors as per their donated amount. It also provides the facility to maintain anonymity of donors (if they wish to) as well as search for donors using various search criteria. In future we wish to make this leaderboard more interesting.
## Donor Management Workflow
This module will provide the various types of users to access sub modules which will help them in managing donors across various stages of the donation process. The various stages are mentioned in details below.
### User Types
 * **Administrator** - This type of user is basically for overall management of the user group and the backend functionality. The Administration module of the index page is only visible to this kind of user
 * **Supervisor** - This type of user has rights to add and modify donor details and contacts and also freeze the donation amount and payment method and generate reciept for the same. Additional funcionalities can be added at a later stage.
 * **Volunteer** - This type of user has access to details of various prospective donors with contact details but can only perform mailing and phone contact logging. Other roles can also be added to this account type at a later stage.
### Work Flow Sub  Modules
The Donor Management workflow System has the following sub modules which are accessible to specific user types who can use these modules to manage the prospective donors at various stages of the donation process
* **Administration**
    * **User Registration Sub Module** - Allows new users to register for various roles subject to approval by a administrator account.This module is accessible by default.
    * **User Login** - Allows registered and approved users to login.
    * **Delete User** - Allows Administrator to Suspend or Delete an existing user account.

* **Donor Leader Board** - This module is visible by default and allows everyone to track the various donors who have committed and freezed the donation to the project. Only certian details of the donor are visible. In case the donor wished to remain anonymous, this facility could be added while commiting the donation amount.

* **Donor Management** - This sub modules allows the various authorized users to perform the following roles
    * Add Prospective Donors
    * Update Donor Contact
    * Donor Phone Contact Logging
    * Donor Mailing
    * Donation Commit and Reciept
    * Accounts
### Directory Structure
The project follows the standard Flask Directory Structure as given below.
### Database
This project is currently using Pickle files to store data related to both donors as well as workflow users. The name of the files are mentioned in the config.py file under the following variables

* User Account Database - USER_DETAILS_PICKLE_FILE
* Donor Details Database - DONOR_DETAILS_PICKLE_FILE

The database would be migarted to a conventional SQL DBMS platform in the future.
    
### Task List
    
 - [x] Index Page and Menu Items
 - [x] User Login Module
 - [x] User Registration Module
 - [x] Prospective Donor Registration
 - [x] Update Donor Contacts
 - [x] Phone Contact Logging
 - [ ] Email Contact
 - [ ] Track Donor Communication
 - [ ] Commit Donation and Receipt
 - [ ] Accounting
 - [ ] Logging

### About the Author
This project is sponsored by Google Summer of Code 2017 and maintained by [Saurabh Singh](mailto:saurabhima@gmail.com) under the mentorship of James Salsman and Tom Hartung with support from the whole CMU Sphinx Team.

### Notes
