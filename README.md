State Time
==========
A lightweight timesheet system for State (or whomever) employees. A fork of [nad2000's Flask-Timesheets](https://github.com/nad2000/Flask-Timesheets).


# Goals

- An easy-to-use Timesheet entry system for employees, including the ability to allot hours spent on a project to a particular Grant Award and Grant Award Task/Service Area. 
- A back-end that makes it easy for managers to set up and maintain standard allocations, monitor employee hours, approve timesheets, etc. 
- Make a platform that is suited to the State of Rhode Island's needs, but easily adaptable to other states, municipalities, organizations, etc.

# TODO
- Move to PostgreSQL for Heroku purposes.
- Add allocations model.
- Update Data Models for users, etc.
- 12-Factor-ize, particurly for ENV variables.

# High-Level Object Design

- Users / Employees:
	- Initial Import from Payroll System of:
		- Names
		- Job Titles
		- Classification
		- Eligible for Overtime
		- Employee ID Number
	- Generated / Gathered:
		- Usernames
		    - Ideally SSO to Office 365/Google Apps, but that's far off.
		- Supervisor (Hierarchical, gains supervisor-admin permissions)
		- Emergency Contact
		- Physical Working Location (Emergency Purposes)
		- Normal working hours (if applicable)
- Timesheets: 
	- Hours - Categorized:
		- Normal working
		- Exception: 
			- Vacation
			- Sick
			- Personal
			- Bereavement
			- Holiday (which we should know in advance) 
			- Jury Duty
			- Workers Compensation
			- Union Duties
			- Training, Conference, or Seminar
			- Other
	- For employees eligible for Overtime, calculation of overtime hours.
	- Approval by Supervisor
		- Timestamped
		- Upon approval, timesheet data eligible for export
		- Ideally, summary dashboard with employee timesheet data, exception hours, etc. 
	- Lookback:
	    - 90 day retrospective analysis of actual hours worked on a particular grant as a proportion of 100% of total worked hours, in order to properly allot exception hours to those grants proportionally. 
	    - Running average calculated at time of timesheet entry
- Allocations:
	- Grant Award - If an employee is doing work related to a Federal or other grant, the name/ID of the grant in question. 
	- Grant Award Task - The Grant Task (or Service Area) the employee was working on. 
- Pay Period: The two-week cycle in which employees are paid.
- Agency:
    - The Agency for whom the employee works.
    - The accounting system Agency Code corresponding to this Agency.
    - Cost Center:
        - Agencies have different "cost centers" across different divisions and functions. 
    - Additional fields necessary? Facilities list? 
- Reminders (via Mailgun):
	- Employees - Input your time.
	- Managers - Approve timesheets.
- Export Files for:
	- Payroll Systems (specifically old-school Mainframes)
	- ERPs (specifically Oracle E-Business Suite)

### Roadmap Features
- Request for Time Off
    - Subject to Supervisor Approval Process
- API: 
        - Establish a standard timesheet POST API for devices like timeclocks, punch-card systems, barcode readers, etc.


## Screen shots

### Timesheet Filling and Submission
![ScreenShot](/Screenshots/s1.png?raw=true "Filling-in Timesheets")

### Update Account
![ScreenShot](/Screenshots/user_profile.png?raw=true "Update Account")

## Admin and Approver Functions

### Manage Accounts
![ScreenShot](/Screenshots/s4.png?raw=true "Manage Accounts")
![ScreenShot](/Screenshots/s5.png?raw=true "Manage Accounts")

### Timesheet Approving
![ScreenShot](/Screenshots/s2.png?raw=true "Timesheet Approving")

### Reporting and Export to MS Excel
![ScreenShot](/Screenshots/s3.png?raw=true "Reporting and Export to MS Excel")


# Docker environment configuration

## Setup a container with DB server:
```
docker run --name db -e MYSQL_ROOT_PASSWORD=test -d -p 3306:3306 mariadb
# -e -- environment
# -d -- run as a daemon
# -p -- map ports
```

## Run client to test connection to DB:
```
docker run --name mysql-client -it --link db:mysql --rm mariadb sh -c 'exec mysql -uroot -ptest -hmysql'
# -it -- interactive
# --rm -- remove after exiting 
```

## Create image for the app:
```
docker build -t flask_blog .
## -t -- tag
```
## Run a container with the new image:

```
docker run -id -p 5000:5000 -v $HOME/flask_blog:/opt/flask_blog --name blog --link db:mysql flask_blog bash
# -id -- interactive and daemon
# -v -- mount a volume 
```

### To access docker, create tables, and start the app:

```
docker exec -it blog bash 
# -it -- interactive terminal

./manage.py shell
from flask_blog inport db
db.create_all()
^D
./manage.py runserver
```

### To find out the IP of the container run:

```
docker inspect blog
#172.17.0.4
```


### License
**MIT**