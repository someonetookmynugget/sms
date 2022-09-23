create table attendance (
    id serial PRIMARY KEY NOT NULL,
    name varchar(30) NOT NULL,
    attendace varchar(20) NOT NULL,
    attendace_day date NOT NULL,
    subject_id int NOT NULL,
    
    FOREIGN KEY(name) 
    REFERENCES student(name)

    FOREIGN KEY(subject_id)
    REFERENCES subjects(id)
);