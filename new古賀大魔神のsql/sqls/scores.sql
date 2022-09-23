create table scores (
    id serial NOT NULL PRIMARY KEY, 
    student_id int NOT NULL,
    subject_id int NOT NULL ,
    score int NOT NULL,
    test_day date NOT NULL,
    test_name varchar(20) NOT NULL,

    FOREIGN KEY(student_id)
    REFERENCES student(id),

    FOREIGN KEY(subject_id)
    REFERENCES subjects(id)
);