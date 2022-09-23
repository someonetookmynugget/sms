create table scores (
    id serial NOT NULL PRIMARY KEY, 
    student_id int NOT NULL,
    subject_id int NOT NULL ,
    score int NOT NULL,
    test_day date NOT NULL,
    grader varchar(20) test_name NOT NULL,
    test_name varchar(20) NOT NULL
);