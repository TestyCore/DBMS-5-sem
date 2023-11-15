-- CREATE TABLE grade_journal (
--     id SERIAL PRIMARY KEY,
--     grade INT CHECK (grade >= 1 AND grade <= 10),
--     student_id INT REFERENCES student(id) ON DELETE CASCADE,
--     subject_id INT REFERENCES subject(id) ON DELETE SET NULL,
--     date DATE
-- );

insert into grade_journal (grade, student_id, subject_id, date) values (10, 1000, 4, '3/21/2023');
insert into grade_journal (grade, student_id, subject_id, date) values (8, 1000, 5, '3/27/2023');
insert into grade_journal (grade, student_id, subject_id, date) values (9, 1000, 6, '4/2/2023');
insert into grade_journal (grade, student_id, subject_id, date) values (6, 1000, 7, '3/6/2023');
insert into grade_journal (grade, student_id, subject_id, date) values (8, 1000, 8, '5/19/2023');
