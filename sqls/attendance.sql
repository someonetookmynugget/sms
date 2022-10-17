create table attendance (
    id serial PRIMARY KEY NOT NULL,
    student_id int NOT NULL,
    attendance_rate varchar(20) NOT NULL,
    attendance_day date NOT NULL,
    subject varchar(20) NOT NULL
);