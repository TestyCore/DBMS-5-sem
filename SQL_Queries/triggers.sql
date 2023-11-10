-- func to log registration of new user when new user is inserted to "users" table
CREATE OR REPLACE FUNCTION users_insert_journal_fnc(new_id INT)
RETURNS VOID AS 
$$
BEGIN
  INSERT INTO journal (users_id, date, action_type_id)
  VALUES (new_id, current_timestamp, 4); -- action_type_id: 4 ('New user registered')
END;
$$
LANGUAGE 'plpgsql';



-- func to log registration of new user when new user is inserted to "users" table
CREATE OR REPLACE FUNCTION users_add_superuser_journal_fnc(new_id INT)
RETURNS VOID AS 
$$
BEGIN
  INSERT INTO journal (users_id, date, action_type_id)
  VALUES (new_id, current_timestamp, 5); -- action_type_id: 5 ('New superuser added')
END;
$$
LANGUAGE 'plpgsql';

 -- (clock_timestamp()::text, 'YYYY-MM-DD HH24:MI:SS.MS')



-- func to insert new user from "users" table to "teacher" table
-- with 'is_staff' = true and 'is_superuser' = false fields. 
CREATE OR REPLACE FUNCTION users_insert_teacher_fnc(new_id INT)
RETURNS VOID AS 
$$
BEGIN
    INSERT INTO teacher (users_id, subject_id)
    VALUES (new_id, 1); -- Belarusian language by default
END;
$$
LANGUAGE 'plpgsql';


CREATE OR REPLACE FUNCTION users_insert_teacher_fnc_wrapper()
RETURNS TRIGGER AS
$$
BEGIN
    PERFORM users_insert_teacher_fnc(NEW.id);
    PERFORM users_insert_journal_fnc(NEW.id);
    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';


-- trigger to insert new teacher to "teacher" table when new user is added to "users" table
CREATE TRIGGER users_insert_teacher_trigger
AFTER INSERT
ON "users"
FOR EACH ROW
WHEN (NEW.is_staff = true AND NEW.is_superuser = false)
EXECUTE PROCEDURE users_insert_teacher_fnc_wrapper();

-- Insert example: insert into users (first_name, last_name, username, password, email, is_staff, is_superuser) values ('Sasha', 'Sviridov', 'Andreevich', 'uO1(!ssu6&e84\', 'sviridov6@gmail.com', true, false);
-- ************************************************************************************************************************************************************************************************************************************************





-- func to insert new user from "users" table to "student" table
-- with 'is_staff' = false and 'is_superuser' = false fields. 
CREATE OR REPLACE FUNCTION users_insert_student_fnc(new_id INT)
RETURNS VOID AS 
$$
BEGIN
    INSERT INTO student (users_id, class_id)
    VALUES (new_id, 1); -- 1"A" class by default
END;
$$
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION users_insert_student_fnc_wrapper()
RETURNS TRIGGER AS
$$
BEGIN
    PERFORM users_insert_student_fnc(NEW.id);
    PERFORM users_insert_journal_fnc(NEW.id);
    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

-- trigger to insert new student to "student" table when new user is added to "users" table
CREATE TRIGGER users_insert_student_trigger
AFTER INSERT
ON "users"
FOR EACH ROW
WHEN (NEW.is_staff = false AND NEW.is_superuser = false)
EXECUTE PROCEDURE insert_student_trigger_wrapper_fnc();

-- Insert example: insert into users (first_name, last_name, username, password, email, is_staff, is_superuser) values ('Anton', 'Vorontsov', 'Andreevich', 'uO1(!ssu6&e84\', 'sviridov6@gmail.com', false, false);
-- ************************************************************************************************************************************************************************************************************************************************





CREATE OR REPLACE FUNCTION users_add_superuser_fnc()
RETURNS TRIGGER AS
$$
BEGIN
    NEW.is_staff = false;
    PERFORM users_add_superuser_journal_fnc(NEW.id);
    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';


CREATE TRIGGER users_add_superuser_trigger
BEFORE UPDATE
ON "users"
FOR EACH ROW
WHEN (OLD.is_staff = true AND OLD.is_superuser = false AND NEW.is_staff = true AND NEW.is_superuser = true)
EXECUTE FUNCTION users_add_superuser_fnc();




-- update users set is_superuser = true where id = 1060;
-- select * from users ORDER BY id DESC LIMIT 10;
-- delete from journal where id = 10;
-- drop trigger if exists users_add_superuser_trigger on users;