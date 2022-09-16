create table student (
    id serial NOT NULL PRIMARY KEY, 
    name varchar(30) NOT NULL ,
    name_sub varchar(30) NOT NULL,
    class varchar(3) NOT NULL,
    grade int(3) NOT NULL,
    department varchar(30) NOT NULL,
    major varchar(30) NOT NULL
);