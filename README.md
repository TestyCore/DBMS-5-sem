**Tatarinov Vyacheslav 153503**
# School

# Functional requirements
* Guest
  * Registration
  * Authorization
  * View published news and announcements
  * View school staff
  * View information about the school

</br>

* Authorized (student)
  * All Guest functionality
  * View lesson schedule
  * View his own grades
    
</br>

* Staff (teacher)
  * All Guest functionality
  * View his own schedule
  * Give grades to students

</br>

* Administrator
  * Edit information about the school
  * Edit student and teacher personal info
  * Create and edit lesson schedule
  * Publish news and announcements
  * View teachers and students logs

</br>
</br>

# Entities
## user
1. `id INT` - PK
2. `first_name VARCHAR(45)` - user's first name
3. `last_name VARCHAR(45)` - user's last name
4. `username VARCHAR(30)` - user's username
5. `password VARCHAR(50)` - user's password
6. `email VARCHAR(255)` - user's email
7. `is_staff TINYINT(1)` - user's status option, assigned to user during registration
8. `is_superuser TINYINT(1)` - user's status option, assigned to user during registration

* OneToMany to "review"
* OneToMany to "article"
* OneToMany to "journal"
* OneToOne to "student"
* OneToOne to "teacher"
  </br>
  </br>
  </br>

  
## event
1. `id INT` - PK
2. `title VARCHAR(255)` - event title
3. `date DATETIME` - time of the event
4. `place VARCHAR(255)` - place of the event

* ManyToMany to "class"
  </br>
  </br>
  </br>


## class
1. `id INT` - PK
2. `name VARCHAR(10)` - name of the particular class (ex. 7"A", 11"B")

* ManyToMany to "event"
* OneToMany to "timetable"
* OneToMany to "student"
* OneToOne to "teacher"
  </br>
  </br>
  </br>

  
## article
1. `id INT` - PK
2. `title VARCHAR(255)` - article title
4. `date DATE` - article publishing date
5. `content TEXT` - information provided in the article

* ManyToOne to "user"
  </br>
  </br>
  </br>


## cabinet
1. `id INT` - PK
2. `name INT` - cabinet number at school

* OneToMany to "timetable"
  </br>
  </br>
  </br>


## subject
1. `id INT` - PK
2. `name VARCHAR(40)` - name of subject learned at school

* OneToMany to "timetable"
* OneToMany to "teacher"
  </br>
  </br>
  </br>


## review
1. `id INT` - PK
3. `date DATE` - date when user left a review
4. `content TEXT` - information that user write in a review
5. `rate INT` -  rate that user left

* ManyToOne to "user"
  </br>
  </br>
  </br>


## lesson_time
1. `id INT` - PK
2. `time_start TIME` - lesson start time
3. `time_end TIME` - lessont end time

* OneToMany to "timetable"
  </br>
  </br>
  </br>


## journal
1. `id INT` - PK
3. `date DATETIME` - datetime when user's actions been logged

* ManyToOne to "user"
* ManyToOne to "action_type"
  </br>
  </br>
  </br>


## action_type
1. `id INT` - PK
2. `name VARCHAR(50)` - type of action that been logged

* OneToMany to "journal"
  </br>
  </br>
  </br>


## teacher
1. `id INT` - PK

* OneToOne to "user"
* OneToOne to "class"
* ManyToOne to "subject"
  </br>
  </br>
  </br>


## student
1. `id INT` - PK

* OneToOne to "user"
* ManyToOne to "class"
  </br>
  </br>
  </br>


## timetable
1. `id INT` - PK
2. `day_of_week VARCHAR(12)` - day of week (ex. Tuesday)
* ManyToOne to "class"
* ManyToOne to "lesson_time"
* ManyToOne to "cabinet"
* ManyToOne to "subject"
  </br>
  </br>
  </br>   
