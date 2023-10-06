-- Amount of students in each class
WITH users_student AS(
SELECT users.first_name AS "fname", student.class_id AS "cls_id"
FROM users
INNER JOIN student ON users.id = student.users_id
)
SELECT COUNT(users_student.fname), class.name
FROM users_student
INNER JOIN class ON users_student.cls_id = class.id
GROUP BY 2
HAVING COUNT(users_student.fname) = 31
ORDER BY 1;

-- timetable var#1
WITH tclass AS(
    SELECT class.name AS "class", timetable.subject_id, timetable.cabinet_id, timetable.lesson_time_id, timetable.day_of_week
    FROM class
    INNER JOIN timetable ON class.id = timetable.class_id
),
tclass_subject AS(
    SELECT tclass.class AS "class", subject.name AS "subject", tclass.cabinet_id, tclass.lesson_time_id, tclass.day_of_week
    FROM tclass
    INNER JOIN subject ON subject.id = tclass.subject_id
),
tclass_subject_cabinet AS(
    SELECT tclass_subject.class AS "class", tclass_subject.subject AS "subject", cabinet.name AS "cabinet", tclass_subject.lesson_time_id, tclass_subject.day_of_week
    FROM tclass_subject
    INNER JOIN cabinet ON cabinet.id = tclass_subject.cabinet_id
)
SELECT tclass_subject_cabinet.class, tclass_subject_cabinet.subject, tclass_subject_cabinet.cabinet, lesson_time.time_start, lesson_time.time_end, tclass_subject_cabinet.day_of_week
FROM tclass_subject_cabinet
INNER JOIN lesson_time ON lesson_time.id = tclass_subject_cabinet.lesson_time_id;

-- timetable var#2
SELECT
    class.name AS "class",
    subject.name AS "subject",
    cabinet.name AS "cabinet",
    lesson_time.time_start,
    lesson_time.time_end,
    timetable.day_of_week
FROM timetable
INNER JOIN class ON class.id = timetable.class_id
INNER JOIN subject ON subject.id = timetable.subject_id
INNER JOIN cabinet ON cabinet.id = timetable.cabinet_id
INNER JOIN lesson_time ON lesson_time.id = timetable.lesson_time_id;

-- class_event table
SELECT 
    class.name AS "class",
    event.title AS "event",
    event.date
FROM class_event
INNER JOIN class ON class.id = class_event.class_id
INNER JOIN event ON event.id = class_event.event_id
WHERE class.name = '1''A''';

-- FULL JOIN
SELECT article.author_id,
    article.date AS "Article",
    review.date AS "Review",
    review.author_id
FROM article
FULL JOIN review ON article.author_id = review.author_id
ORDER BY 1;

-- LEFT JOIN
SELECT article.author_id,
    article.date AS "Article",
    review.date AS "Review",
    review.author_id
FROM article
LEFT JOIN review ON article.author_id = review.author_id
ORDER BY 1;

-- RIGHT JOIN
SELECT article.author_id,
    article.date AS "Article",
    review.date AS "Review",
    review.author_id
FROM article
RIGHT JOIN review ON article.author_id = review.author_id 
ORDER BY 1;

-- CROSS JOIN
SELECT article.author_id,
    article.date AS "Article",
    review.date AS "Review",
    review.author_id
FROM article
CROSS JOIN review
ORDER BY 1;

-- NATURAL JOIN
SELECT student.class_id,
    class_event.class_id
FROM student
NATURAL JOIN class_event
ORDER BY 1;

-- "SELF" JOIN
SELECT e.first_name || ' ' || e.last_name AS "employee",
m.first_name || ' ' || m.last_name AS "manager"
FROM employee e
INNER JOIN employee m ON m.employee_id = e.manager_id;

-- JOIN USING
SELECT student.class_id,
    class_event.class_id
FROM student
INNER JOIN class_event USING(class_id)
ORDER BY 1;

-- Create INDEX
CREATE INDEX idx_users_first_name
ON users(first_name);

EXPLAIN SELECT first_name FROM users WHERE first_name = 'Livy';

-- Drop INDEX
DROP INDEX idx_users_first_name;

-- Teacher - subject
SELECT users.first_name || ' ' || users.last_name AS "Uchilka",
subject.name AS "Nauka"
FROM teacher
INNER JOIN users ON users.id = teacher.users_id
INNER JOIN subject ON subject.id = teacher.subject_id;

-- all student on all events
WITH student_class AS(
    SELECT users.first_name || ' ' || users.last_name AS "Student",
        student.class_id
    FROM users
    INNER JOIN student ON users.id = student.users_id
)
SELECT student_class."Student",
event.title AS "Event"
FROM class_event
INNER JOIN student_class ON student_class.class_id = class_event.class_id
INNER JOIN event ON event.id = class_event.event_id
ORDER BY 2;

-- How much students on each event
WITH student_class AS(
    SELECT users.first_name || ' ' || users.last_name AS "Student",
        student.class_id
    FROM users
    INNER JOIN student ON users.id = student.users_id
)
SELECT COUNT(student_class."Student"),
event.title AS "Event"
FROM class_event
INNER JOIN student_class ON student_class.class_id = class_event.class_id
INNER JOIN event ON event.id = class_event.event_id
GROUP BY 2;

-- Multiple condition
SELECT rate FROM review WHERE rate > 2 AND rate < 4;

-- Nested condition
SELECT rate 
FROM review 
WHERE rate > (
    SELECT AVG(rate)
    FROM review
    )


-- PARTITION BY LIST
CREATE TABLE salary_region (
    id SERIAL,
    amount INT,
    region VARCHAR(30),
    PRIMARY KEY (id, region)
    ) PARTITION BY LIST (region);
    --PARTITION BY RANGE (sale_date);
CREATE TABLE London PARTITION OF salary_region FOR VALUES IN ('London');
                                             --FOR VALUES FROM ('2019-10-01') TO ('2020-01-01');
CREATE TABLE Minsk PARTITION OF salary_region FOR VALUES IN ('Minsk');
CREATE TABLE Tokio PARTITION OF salary_region FOR VALUES IN ('Tokio');

SELECT product_name,
    price,
    group_name,
    AVG (price) OVER (
         PARTITION BY group_name 
         )
FROM products
INNER JOIN product_groups USING (group_id);


-- PARTITION BY
SELECT author_id, rate, date, ROW_NUMBER() OVER (PARTITION BY rate ORDER BY date DESC)
FROM review
ORDER BY 2 DESC;


-- teachers who teach 'Chemistry'
SELECT name
FROM class
WHERE EXISTS (
    SELECT teacher.id
    FROM teacher
    JOIN subject ON teacher.subject_id = subject.id 
    WHERE class.teacher_id = teacher.id AND subject.name = 'Chemistry'
);

-- INSERT INTO SELECT
CREATE TABLE attendence_list (
    StudentID int,
    StudentName VARCHAR(255)
    );

INSERT INTO attendence_list(StudentId,StudentName)
SELECT StudentId,StudentName
FROM students_info;
--WHERE students_info.studentid>2;
SELECT * FROM attendence_list;

-- CASE
SELECT rate, id
FROM review
ORDER BY
(CASE
    WHEN (SELECT AVG(rate) FROM review) > 4 THEN rate
    ELSE id
END);

SELECT rate, id,
    CASE
        WHEN rate = 5 THEN 'five'
        WHEN rate = 4 THEN 'four'
        WHEN rate = 3 THEN 'three'
        WHEN rate = 2 THEN 'two'
        WHEN rate = 1 THEN 'one'
        ELSE 'None' END AS word
FROM review;

--WHERE first_name contain letters are regardless the case.
SELECT first_name FROM users WHERE LOWER(first_name) LIKE '%con%';
