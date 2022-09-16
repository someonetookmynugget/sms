create table student (
    id int NOT NULL PRIMARY KEY, 
    subject varchar(30) NOT NULL ,
    attendance int NOT NULL,
    score int NOT NULL,
    test_day date NOT NULL,
    grader varchar(30) NOT NULL,
    test_name varchar(30) NOT NULL
);