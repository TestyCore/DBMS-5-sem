**Tatarinov Vyacheslav 153503**
# School

## Functional requirements
* Guest:
  * Registration.
  * Authorization.
  * View published news and announcements.
  * View school staff.
  * View information about the school.
* Student:
  * All Guest functionality
  * View lesson schedule.
  * View his own grades.
* Teacher:
  * All Guest functionality.
  * View his own schedule.
  * Give grades to students.
* Administrator:
  * Edit information about the school.
  * Edit student and teacher personal info.
  * Create and edit lesson schedule.
  * Publish news and announcements.
  * View teachers and students logs.



## Description
#### User:
1. `Id (int)` - PK.
2. `First_name (char)` - User's first name.
3. `Last_name (char)` - User's last name.
4. `Second_name (char)` - User's second name.
5. `Email (char)` - User's email.
6. `Age (int)` - User's age.
7. `Role (FK)` -  User's role. "MTO" to Role Table.

#### Role:
1. `Id (int)` - PK.
2. `Name (char)` - Role that is assigned to user during registration.

#### Event:
1. `Id (int)` - PK. "MTM" to Class Table.
2. `Title (char)` - Event title.
3. `DateTime (datetime)` - Time of the event.
4. `Place (char)` - Place of the event.

#### Class:
1. `Id (int)` - PK. "MTM" to Class Table.  "OTO" to User Table (One class can have only one classroom teacher and vice versa)
2. `Name (char)` - Name of the particular class (ex. 7"A", 11"B").  

#### Article:
1. `Id (int)` - PK.
2. `Title (char)` - Article title.
3. `Author (FK)` - Article author (student or teacher). "MTO" to User Table.
4. `Date (date)` - Article publishing date.
5. `Content (char)` - Information provided in the article.

#### Cabinet:
1. `Id (int)` - PK.
2. `Name (int)` - cabinet number at school.
   
#### Subject:
1. `Id (int)` - PK.
2. `Subject (char)` - Name of subject learned at school.

#### Review:
1. `Id (int)` - PK.
2. `User (FK)` - User that left a review. "MTO" to User Table.
3. `Date (date)` - Date when user left a review.
4. `Content (char)` - Information that user write in a review.
5. `Rate (int)` - User's rate.

#### Calls_time:
1. `Id (int)` - PK.
2. `Time (time)` - School call schedule.

#### Journal:
1. `Id (int)` - PK.
2. `User (FK)` - User whos actions were logged. "MTO" to User Table.
3. `Datetime (datetime)` - Datetime when user's actions where logged.
4. `Action_type (FK)` - Type of action that was logged. "MTO" to Action_type Table

#### Action_type:
1. `Id (int)` - PK.
2. `Name (char)` - Type of action that is logged.

   



   
