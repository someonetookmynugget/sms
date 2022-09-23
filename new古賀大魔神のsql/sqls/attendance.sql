create table attendance (
    id serial PRIMARY KEY NOT NULL,
    student_id int NOT NULL,
    attendace varchar(20) NOT NULL,
    attendace_day date NOT NULL,
    subject_id int NOT NULL,
    
    FOREIGN KEY(student_id) 
    REFERENCES student(id),

    FOREIGN KEY(subject_id)
    REFERENCES subjects(id)
);