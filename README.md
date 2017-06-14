# **SphinxCAPT.org LEADERBOARD**
### Overview
In this project we are designing a FLASK based Web App to maintain Leaderboards for [SphinxCAPT.org](http://SphinxCAPT.org).
The app is based on the REST design with inherent security infrastructure. This project is being maintained as part of the Google Summer of Code 2017.
### Requirements
* **Backend**
    * Python 3
    * Flask
    * Pickle
* **Frontend**
    * Web Browser with HTML5
    * Javascript
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
