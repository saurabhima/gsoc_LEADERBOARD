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
In order to connect the MySQL database the user must provide the config file containing details of __SQLALCHEMY_DATABASE_URI__. An example config file is given below
> SQLALCHEMY_DATABASE_URI='mysql://username:password@localhost/databasename'

The Donor Management Workflow Flask application can be executed by the following command
 > CONFIG=databaseconfigfile python leaderboard.py

The __databaseconfigfile__ file contains the __SQLALCHEMY_DATABASE_URI__ as mentioned above.

The python interpreter will respond with the IP and Port on which the Flask app is running

Eg
> Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

The user can then use this web address to open the default page or index.html
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
    * **Approve User** - Allows Administrator to approve a new user for a specific role. Without explicit approval from an Administrator a new user cannot Login or perform any functions.
    * **Delete User** - Allows Administrator to Suspend or Delete an existing user account.(Currently under development)
    * **Email Setup** - Allows Administrator to Add/Delete or Modify Email Templates which would be used by Volunteers to send Emails to Donors.These templates provide the bare structure on which the volunteers can build their mail and thus gives a standard interface to volunteers for quick email. These Email Templates are divided into the following parts
        * **Salutation** - Eg Dear Mr XXX
        * **Main Body** - The Bare Content of the Email
        * **Closing** - Eg With Warm Regards
        * **Signature** - Signature of the logged user
    * **Allot Volunteer to Donor** - Allows Administrator to allot a dedicated Volunteer to every prospective donor who is responsible for 1contacting the donor and persuading him/her to donate money for the project. The volunteer would generally act as a ___Single Point of Contact___ to the donor.

* **Donor Leader Board** - This module is visible by default and allows everyone to track the various donors who have credited confirmed donations to the project . Only certain details of the donor are visible. In case the donor wished to remain anonymous, this facility could be added while committing the donation amount.

* **Donor Management** - This sub modules allows the various authorized users to perform the following roles
    * __Add Prospective Donors__ - This module allows all users to add credentials of a new prospective user into the Workflow Application. 
    * __Update Donor Contact__ - This module allows all users to modify contact information (including Phone and Email) of Donors who's details already exist in the Application. 
    * __Donor Phone Contact Logging__ - This module allows all users to Log details of telephonic conversation with Donors. Details of previous Phone and Email Conversations are available to the Volunteer for reference. 
    * __Donor Mailing (Including Single Mail,Bulk Email and Bulk Email with Mail Merge)__ - This module allows all users to send Emails to Donors using either a ___Saved Template___ or by using ___Manual Composition___ option. Once the volunteer selects a template they are provided with a semi-filled structure of the Email which can be modified before sending. Details pertaining the donor and the volunteer are automatically entered by the application in the respective fields 
    * __Donation Commit__ - This module allows Volunteers to enter details of donations which have been committed by a donor. These details include the committed amount as well as the mode of transfer of the donation. These details are used by the Supervisors to track such users in order to facilitate easy transfer of the donation to the project account.  
    * __Donation Credit and Receipt Generation__ - This module allows all users to enter details of donation amount which has been credited to the project account by committed donors. Once the details are entered in the application it allows automatic generation of ___Receipt___ in form of a PDF file which is automatically sent to the Donor on his email and in case if the Donor wishes it is also sent to him by Post.

### Directory Structure
The project follows the standard Flask Directory Structure. The detailed directory structure is being updated and would be posted soon.
* __root__
    * __static__
        * ___css___ - Contains CSS files used by HTML files in ___templates___ folder.
        * ___fonts___ - Contains Fonts files used by HTML files in ___templates___ folder.
        * ___images___ - Contains images  used by HTML files in ___templates___ folder.
        * ___js___ - Contains Javascript files used by HTML files in ___templates___ folder.
    * __templates__ - Contains HTML templates used by Flask for various Endpoints.
    * __tests__ - Contains Unit Test modules for testing the application.
    * __receipts__ - Contains copies of receipts generated by the application for credited donations for record keeping.
        
### Important Python Files
The project is divided into various sub modules as per Flask convention. The details of important Python files are given below
* __config.py__ - Contains certain environment configuration variables which gives flexibility during migration of code to a different platform or directory. 
* __email_service.py__ - This file contains methods required to authenticate using OAUTH 2.0 protocol with ___Gmail__ and to send email using ___Google Python API___.
* __forms.py__ - This file contains ___wtforms___ structure which are used to process data entered by users using various endpoints. 
* __exception.py__ - This file contains code for ___Exception Handling___ used by Flask.
* __generate_receipt.py__ - This file is used to generate ___Donation Receipts___ in ___Pdf Format___ which are further sent to Donors using Email/Post.
* __leaderboard.py__ - The core ___Flask Application___ file which initializes the application. This file also contains code to connect to the ___MySQL Database___.
* __models.py__ - This file contains ___database models___ which are used to connect to the ___MySQL Database___. It uses ___sqlalchemy___ library to connect to the database.
* __sub_process.py__ - This is one of the most important files in the application and contains methods which are regularly called by other files in order to retrieve/process data.
* __upload_receipt_gdrive.py__ - This file is used to upload the donation receipts generated by ___generate_receipt.py___ file to ___Google Drive___ using ___Google Python API___.  
* __views.py__ - This file contains various ___Endpoints___ which are used in the application. The details of the endpoints are given below.

### Database
The project used a MySQL database to store details of Donors,Communication (Telephonic & Email), User Details as well as Accounting transactions. The Current Scheme for the databse can be founded in the [___Schema.png___](https://github.com/saurabhima/gsoc_LEADERBOARD/blob/master/Schema.png) file in the repo.
 ![Schema](https://github.com/saurabhima/gsoc_LEADERBOARD/blob/master/Schema.png)

### SQLAlchemy Models
The project uses a large number of ___SQLAlchemy Models___ to connect to the application database. The details of these models are given below.
* __User__ - Contains model description of registered users of the application. This model connects to the _workflow_users_ table of the database.
* __Donor__ - Contains model description of Donors who have been registered in the application and connects to the _donor_details_ table.
* __DonorPhoneLog__ - Contains model description of Telephone Logs entered by Volunteers with Donors and connects to the _donor_phone_logs_ table.
* __DonorEmailLog__ - Contains model description of Email Logs entered by Volunteers with Donors and connects to the _donor_email_logs_ table.
* __CommittedDonation__ - Contains model description of committed donation details which have been given to the volunteer by the donors. This model connects to the _committed_donation_details_ table.
* __CreditDonation__ - Contains model description of credited donation details which have been transferred  to the project accounts by the donors. This model connects to the _credit_donation_details_ table.
* __EmailTemplate__ - Contains model description of Email templates which have been created by administrators to be used to send emails to donors.This model connects to the _email_templates_ table.
* __BulkEmailList__ - Contains model description of Bulk Email List which contains details of donors who are addresses in the bulk email module.This model connects to the _bulk_email_list_ table.

### Flask Endpoint Description
  This section provides an overview of all the endpoints available to users in the Donor Management Workflow
  * __/__ - This module will launch index.html and give the default view of the application
  * __/default__ - This endpoint is only for testing purpose to check redirecting of webpages
  * __/donorleaderboard__ - This endpoint will launch the ___donor_leaderboard.html___ webpage which displays the current Donor Leaderboard to all users
  
  * __User Management Endpoints__
    
    * __/user_register__ - This endpoint is used for registering new users and launches ___register_new_user.html___
    * __/process_new_user_register__ - This endpoint collects the POST response from  ___/user_register___ endpoint and extracts user credentials like email address, phone, name, username, password etc and stores it in the User Account Database. After this the user is redirected to ___index.html___
    * __/user_login__ - This endpoint is used for logging existing and approved users and launches ___user_login.html___
    * __/user_login_process__ - This endpoint collects the POST response from  ___/user_login___ endpoint and extracts user credentials like username and password and matches it with credentials stored in the User Account Database. On matching the user status is changed to ___Logged___ and user is redirected to ___index.html___. In case of failed login the user is directed to the ___Login Error Page___ i.e. ___invalid_login.html___
    * __/logout__ - This endpoint deletes the user login session variables and updates the status to Not Logged. The user is then redirected to ___index.html___
    * __/approve_new_user__ - This endpoint is only available to ___Administrator___ User Group and allows these users to approve pending users who have freshly registered. This endpoint launches ___approve_user.html___. In case these is no user account pending for approval, the user is redirected to ___index.html___
    * __/approve_new_user_process__ - This endpoint collects the POST response from  ___/approve_new_user___ endpoint and extracts user credentials like email address, phone, name, username etc. In case the user is approved by the Administrator the account status is changed to ___Active___. In case the administrator rejects the user account, the same is removed from the list of pending users.
  
  * __Donor Management Endpoints__
    
    * __/register_new_donor__ - This endpoint is used by authorized users to add details of prospective donors to the ___Donor Details Database___ which would be further used in the workflow during the whole donor management process
    * __/process_donor_form__ - This endpoint collects the POST response from  ___/register_new_donor___ endpoint and extracts Donor user credentials like email address, phone, name, organisation etc and stores it in the Donor Details Database
    * __/donor_contact_update__ - This endpoint launches ___donor_contact_update.html___ and used to update contact details of registered donors. The user can choose the specific donor by searching for the donor from the list and update the contact information
    * __/donor_contact_update_process__ - This endpoint extract the ___Donor ID___ selected by the user for updating contact information in the ___/donor_contact_update___ endpoint and passes this ID to ___donor_contact_update_form.html___ where it is read by Jinja for displaying the available contact info about the donor
    * __/donor_contact_update_form_process__ - This endpoint collects the POST response from  ___/donor_contact_update_process___ endpoint and extracts the updated Donor contact info like email address and phone and updates it in the Donor Details Database
    * __/donor_phone_contact__ - This endpoint lauches ___donor_phone_contact.html___ which is used to select the donor with whom the user wants to log the telephonic conversation. The user can select the target donor from the Donor List and using form submission this information is passed to the ___/donor_phone_contact_process___ endpoint
    * __/donor_phone_contact_process__ - This endpoint collects the POST response from  ___/donor_phone_contact___ endpoint and extracts Donor ID. Then is searches the Donor ID in the Donor Details Database to extract other credential of the user. Details of previous conversations with the donor are also retrieved. The endpoint further passes this information to ___donor_phone_contact_logging.html___
    * __/donor_phone_log_process__ - This endpoint collects POST response from ___donor_phone_contact_logging.html___. These details include summary of the telephonic conversartion with the donor as well as details shared with the donor. These details are updated in the __DONOR_CONTACT_LOGS_FILE___ 
### Task List
    
 - [x] Index Page and Menu Items
 - [x] User Login Module
 - [x] User Registration Module
 - [x] Prospective Donor Registration
 - [x] Update Donor Contacts
 - [x] Phone Contact Logging :phone:
 - [x] Email Contact :incoming_envelope:
 - [x] Bulk Emailing :incoming_envelope:
 - [x] Bulk Emailing using Mail Merge :incoming_envelope:
 - [ ] Track Donor Communication
 - [x] Commit Donation and Receipt
 - [ ] Accounting
 - [ ] Logging

### About the Author
This project is sponsored by Google Summer of Code 2017 and maintained by [Saurabh Singh](mailto:saurabhima@gmail.com) under the mentorship of James Salsman and Tom Hartung with support from the whole CMU Sphinx Team.

### Notes
Completed  Receipt Generation & Accounting :credit_card:
 
Updating of README file for new endpoints and database needed to be done.

### Announcements 
:mega:
