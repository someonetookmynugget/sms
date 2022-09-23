create table majors (
    id serial PRIMARY KEY NOT NULL,
    major varchar(20) NOT NULL,
    department_id int NOT null,

    FOREIGN KEY(department_id)
    REFERENCES departments(id)
);