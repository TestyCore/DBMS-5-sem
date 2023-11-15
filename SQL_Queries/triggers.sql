-- log actions
CREATE OR REPLACE PROCEDURE journal_log_proc(id INT, action_id INT)
LANGUAGE 'plpgsql' AS 
$$
BEGIN
  INSERT INTO journal (users_id, date, action_type_id)
  VALUES (id, current_timestamp, action_id); 
END;
$$;



-- insert new teacher to "teacher" table
CREATE OR REPLACE PROCEDURE teacher_insert_proc(new_id INT)
LANGUAGE 'plpgsql' AS 
$$
BEGIN
    INSERT INTO teacher (users_id, subject_id)
    VALUES (new_id, 1); -- Belarusian language by default
END;
$$;



-- insert new student to "student" table
CREATE OR REPLACE PROCEDURE student_insert_proc(new_id INT)
LANGUAGE 'plpgsql' AS 
$$
BEGIN
    INSERT INTO student (users_id, class_id)
    VALUES (new_id, 1); -- 1"A" class by default
END;
$$;




CREATE OR REPLACE FUNCTION users_insert_trigger_fnc()
RETURNS TRIGGER AS
$$
BEGIN

    IF NEW.is_staff = false AND NEW.is_superuser = false THEN
        CALL student_insert_proc(NEW.id);
        CALL journal_log_proc(NEW.id, 4); -- action_type_id: 4 ('New student has been registered')
    ELSIF NEW.is_staff = true AND NEW.is_superuser = false THEN
        CALL teacher_insert_proc(NEW.id);
        CALL journal_log_proc(NEW.id, 8); -- action_type_id: 8 ('New staff has been registered')
    ELSE
        CALL journal_log_proc(NEW.id, 5); -- action_type_id: 5 ('New superuser has been registered')
    END IF;

    RETURN NEW;

END;
$$
LANGUAGE 'plpgsql';


CREATE TRIGGER users_insert_trigger
AFTER INSERT
ON "users"
FOR EACH ROW
EXECUTE PROCEDURE users_insert_trigger_fnc();





CREATE OR REPLACE FUNCTION users_forbidden_insert_trigger_fnc()
RETURNS TRIGGER AS
$$
BEGIN

    IF NEW.is_staff = true AND NEW.is_superuser = true THEN
        RAISE EXCEPTION 'Insertion is not allowed for is_staff = true and is_superuser = true';
    END IF;

    RETURN NEW;

END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER users_forbidden_insert_trigger
BEFORE INSERT
ON "users"
FOR EACH ROW
EXECUTE PROCEDURE users_forbidden_insert_trigger_fnc();



-- Insert example: insert into users (first_name, last_name, username, password, email, is_staff, is_superuser) values ('Anton', 'Vorontsov', 'Andreevich', 'uO1(!ssu6&e84\', 'sviridov6@gmail.com', false, false);
-- ************************************************************************************************************************************************************************************************************************************************



CREATE OR REPLACE PROCEDURE teacher_delete_proc(old_id INT)
LANGUAGE 'plpgsql' AS 
$$
BEGIN
    DELETE FROM teacher WHERE users_id = old_id;
END;
$$;

CREATE OR REPLACE FUNCTION users_update_to_add_superuser_fnc()
RETURNS TRIGGER AS
$$
BEGIN
    NEW.is_staff = false;
    CALL journal_log_proc(NEW.id, 5); -- action_type_id: 5 ('New superuser added')
    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';


CREATE TRIGGER users_update_to_add_superuser_trigger
BEFORE UPDATE
ON "users"
FOR EACH ROW
WHEN (OLD.is_staff = true AND OLD.is_superuser = false AND NEW.is_staff = true AND NEW.is_superuser = true)
EXECUTE FUNCTION users_update_to_add_superuser_fnc();

-- ************************************************************************************************************************************************************************************************************************************************





-- remove user from "users" table when corresponding student been removed from "student" table.
CREATE OR REPLACE PROCEDURE users_delete_proc(old_id INT)
LANGUAGE 'plpgsql' AS 
$$
BEGIN
    DELETE FROM users WHERE id = old_id;
END;
$$;


CREATE OR REPLACE PROCEDURE archive_student_proc(old_id INT)
LANGUAGE 'plpgsql' AS 
$$
DECLARE
    first_name_cp VARCHAR(50);
    last_name_cp VARCHAR(50);
    email_cp VARCHAR(150);
    journal_id_cp INT;
BEGIN
    SELECT first_name, last_name, email INTO first_name_cp, last_name_cp, email_cp
    FROM users
    WHERE id = old_id;


    SELECT id INTO journal_id_cp
    FROM journal
    WHERE users_id = old_id;


    INSERT INTO student_archive (first_name, last_name, email, journal_id)
    VALUES (first_name_cp, last_name_cp, email_cp, journal_id_cp); 

END;
$$;


CREATE OR REPLACE FUNCTION student_delete_proc_wrapper()
RETURNS TRIGGER AS
$$
BEGIN
    CALL journal_log_proc(OLD.users_id, 7); -- action_type_id: 7 ('Student has been deleted')
    CALL archive_student_proc(OLD.users_id);
    CALL users_delete_proc(OLD.users_id);
    RETURN OLD;
END;
$$
LANGUAGE 'plpgsql';


CREATE TRIGGER student_delete_trigger
AFTER DELETE
ON "student"
FOR EACH ROW
EXECUTE PROCEDURE student_delete_proc_wrapper();








CREATE OR REPLACE PROCEDURE archive_teacher_proc(old_id INT)
LANGUAGE 'plpgsql' AS 
$$
DECLARE
    first_name_cp VARCHAR(50);
    last_name_cp VARCHAR(50);
    email_cp VARCHAR(150);
    journal_id_cp INT;
BEGIN
    SELECT first_name, last_name, email INTO first_name_cp, last_name_cp, email_cp
    FROM users
    WHERE id = old_id;


    SELECT id INTO journal_id_cp
    FROM journal
    WHERE users_id = old_id;


    INSERT INTO staff_archive (first_name, last_name, email, journal_id)
    VALUES (first_name_cp, last_name_cp, email_cp, journal_id_cp); 

END;
$$;


CREATE OR REPLACE FUNCTION teacher_delete_proc_wrapper()
RETURNS TRIGGER AS
$$
BEGIN

    CALL journal_log_proc(OLD.users_id, 9); -- action_type_id: 9 ('Staff has been deleted')
    CALL archive_teacher_proc(OLD.users_id);
    CALL users_delete_proc(OLD.users_id);

    RETURN OLD;
END;
$$
LANGUAGE 'plpgsql';


CREATE TRIGGER teacher_delete_trigger
AFTER DELETE
ON "teacher"
FOR EACH ROW
EXECUTE PROCEDURE teacher_delete_proc_wrapper();






-- update users set is_superuser = true where id = 1060;
-- select * from users ORDER BY id DESC LIMIT 10;
-- select * from student ORDER BY id DESC LIMIT 10;
-- select * from teacher ORDER BY id DESC LIMIT 10;
-- select * from journal ORDER BY id DESC LIMIT 10;
-- select * from staff_archive ORDER BY id DESC LIMIT 10;
-- select * from student_archive ORDER BY id DESC LIMIT 10;
-- select * from article ORDER BY id DESC LIMIT 10;
-- select * from review ORDER BY id DESC LIMIT 10;
-- delete from journal where id = 10;
-- drop trigger if exists users_add_superuser_trigger on users;







-- DROP TRIGGER student_delete_trigger on student;
-- DROP TRIGGER users_add_superuser_trigger on users;
-- DROP TRIGGER users_insert_student_trigger on users;
-- DROP TRIGGER users_insert_teacher_trigger on users;




-- DROP FUNCTION teacher_insert_fnc(new_id INT);
-- DROP FUNCTION teacher_insert_fnc_wrapper();
-- DROP FUNCTION student_insert_proc_wrapper();
-- DROP FUNCTION users_add_superuser_fnc();
-- DROP FUNCTION student_delete_proc_wrapper();




-- DROP PROCEDURE journal_log_proc(id INT, action_id INT);
-- DROP PROCEDURE student_insert_proc(new_id INT);
-- DROP PROCEDURE users_delete_proc(old_id INT);
-- DROP PROCEDURE archive_proc(old_id INT);




-- SELECT tgname AS trigger_name
-- FROM pg_trigger
-- WHERE tgrelid = 'public.teacher'::regclass;


-- ALTER TABLE review
-- ALTER COLUMN author_id DROP NOT NULL;


-- SELECT setval('review_id_seq', 1, false);


-- ALTER TABLE review
-- DROP CONSTRAINT review_author_id_fkey;


-- ALTER TABLE review
-- ADD CONSTRAINT review_author_id_fkey
-- FOREIGN KEY (author_id) REFERENCES users(id)
-- ON DELETE SET NULL;


-- DELETE FROM review;