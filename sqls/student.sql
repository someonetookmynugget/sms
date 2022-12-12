create table student (
    id serial NOT NULL PRIMARY KEY, 
    student_id varchar(10) NOT NULL,
    name varchar(20) NOT NULL,
    name_sub varchar(20) NOT NULL,
    gender varchar(5) NOT NULL,
    age int NOT NULL,
    department_id int NOT NULL,
    major_id int NOT NULL,
    class_id int default 1,
    subject_id int,
    grade int NOT NULL,
    rate varchar(2) default '',
    note varchar (255) default '',
    total_unit int default 0,
    total_attend int default 0,
    total_absence int default 0,
    tardy int default 0,
    leave_early int default 0,
    official_absence int default 0,
    total_lessons int default 0,

    FOREIGN KEY(department_id) 
    REFERENCES departments(id),

    FOREIGN KEY(major_id) 
    REFERENCES majors(id),

    FOREIGN KEY(class_id) 
    REFERENCES classes(id),

    FOREIGN KEY(subject_id) 
    REFERENCES subjects(id)
);
insert into student (
    student_id,
    name,
    name_sub,
    gender,
    age,
    department_id,
    major_id,
    class_id,
    subject_id,
    grade,
    total_unit
    )
values(
    '2004230006',
    '古賀慶次郎',
    'コガケイジロウ',
    '男性',
    21,
    1,
    2,
    7,
    3,
    3,
    2
);

insert into student (
    student_id,
    name,
    name_sub,
    gender,
    age,
    department_id,
    major_id,
    class_id,
    subject_id,
    grade,
    total_unit
    
    )
values(
    '2004230011',
    '西結都',
    'ニシユイト',
    '男性',
    21,
    1,
    2,
    7,
    3,
    3,
    2
);
insert into student (
    student_id,
    name,
    name_sub,
    gender,
    age,
    department_id,
    major_id,
    class_id,
    subject_id,
    grade,
    total_unit
    )
values(
    '2004240012',
    '中村太一',
    'ナカムラタイチ',
    '男性',
    20,
    1,
    1,
    5,
    1,
    3,
    2
);
insert into student (
    student_id,
    name,
    name_sub,
    gender,
    age,
    department_id,
    major_id,
    class_id,
    subject_id,
    grade,
    total_unit
    )
values(
    '2004230006',
    '古賀慶次郎',
    'コガケイジロウ',
    '男性',
    21,
    1,
    2,
    7,
    4,
    3,
    2
);
insert into student (
    student_id,
    name,
    name_sub,
    gender,
    age,
    department_id,
    major_id,
    class_id,
    subject_id,
    grade,
    total_unit
    )
values(
    '2004230011',
    '西結都',
    'ニシユイト',
    '男性',
    21,
    1,
    2,
    7,
    4,
    3,
    2
);
insert into student (
    student_id,
    name,
    name_sub,
    gender,
    age,
    department_id,
    major_id,
    class_id,
    subject_id,
    grade,
    total_unit
    )
values(
    '2004230006',
    '古賀慶次郎',
    'コガケイジロウ',
    '男性',
    21,
    1,
    2,
    7,
    5,
    3,
    2
);
insert into student (
    student_id,
    name,
    name_sub,
    gender,
    age,
    department_id,
    major_id,
    class_id,
    subject_id,
    grade,
    total_unit
    )
values(
    '2004230011',
    '西結都',
    'ニシユイト',
    '男性',
    21,
    1,
    2,
    7,
    5,
    3,
    2
);
insert into student (
    student_id,
    name,
    name_sub,
    gender,
    age,
    department_id,
    major_id,
    class_id,
    subject_id,
    grade,
    total_unit
    )
values(
    '2004240012',
    '中村太一',
    'ナカムラタイチ',
    '男性',
    20,
    1,
    1,
    5,
    9,
    3,
    2
);
insert into student (
    student_id,
    name,
    name_sub,
    gender,
    age,
    department_id,
    major_id,
    class_id,
    subject_id,
    grade,
    total_unit
    )
values(
    '2004240012',
    '中村太一',
    'ナカムラタイチ',
    '男性',
    20,
    1,
    1,
    5,
    10,
    3,
    2
);
insert into student (
    student_id,
    name,
    name_sub,
    gender,
    age,
    department_id,
    major_id,
    class_id,
    subject_id,
    grade,
    total_unit
    )
values(
    '2004240012',
    '中村太一',
    'ナカムラタイチ',
    '男性',
    20,
    1,
    1,
    5,
    11,
    3,
    2
);
insert into student (
    student_id,
    name,
    name_sub,
    gender,
    age,
    department_id,
    major_id,
    class_id,
    subject_id,
    grade,
    total_unit
    )
values(
    '2004230011',
    '西結都',
    'ニシユイト',
    '男性',
    21,
    1,
    2,
    7,
    6,
    3,
    2
);
insert into student (
    student_id,
    name,
    name_sub,
    gender,
    age,
    department_id,
    major_id,
    class_id,
    subject_id,
    grade,
    total_unit
    )
values(
    '2004230011',
    '西結都',
    'ニシユイト',
    '男性',
    21,
    1,
    2,
    7,
    7,
    3,
    2
);
insert into student (
    student_id,
    name,
    name_sub,
    gender,
    age,
    department_id,
    major_id,
    class_id,
    subject_id,
    grade,
    total_unit
    )
values(
    '2004230011',
    '西結都',
    'ニシユイト',
    '男性',
    21,
    1,
    2,
    7,
    8,
    3,
    2
);
insert into student (
    student_id,
    name,
    name_sub,
    gender,
    age,
    department_id,
    major_id,
    class_id,
    subject_id,
    grade,
    total_unit
    )
values(
    '2004230006',
    '古賀慶次郎',
    'コガケイジロウ',
    '男性',
    21,
    1,
    2,
    7,
    6,
    3,
    2
);
insert into student (
    student_id,
    name,
    name_sub,
    gender,
    age,
    department_id,
    major_id,
    class_id,
    subject_id,
    grade,
    total_unit
    )
values(
    '2004230006',
    '古賀慶次郎',
    'コガケイジロウ',
    '男性',
    21,
    1,
    2,
    7,
    7,
    3,
    2
);
insert into student (
    student_id,
    name,
    name_sub,
    gender,
    age,
    department_id,
    major_id,
    class_id,
    subject_id,
    grade,
    total_unit
    )
values(
    '2004230006',
    '古賀慶次郎',
    'コガケイジロウ',
    '男性',
    21,
    1,
    2,
    7,
    8,
    3,
    2
);
insert into student (
    student_id,
    name,
    name_sub,
    gender,
    age,
    department_id,
    major_id,
    class_id,
    subject_id,
    grade,
    total_unit
    )
values(
    '2004230006',
    '古賀慶次郎',
    'コガケイジロウ',
    '男性',
    21,
    1,
    2,
    7,
    12,
    3,
    2
);
insert into student (
    student_id,
    name,
    name_sub,
    gender,
    age,
    department_id,
    major_id,
    class_id,
    subject_id,
    grade,
    total_unit
    )
values(
    '2004230006',
    '古賀慶次郎',
    'コガケイジロウ',
    '男性',
    21,
    1,
    2,
    7,
    13,
    3,
    2
);
insert into student (
    student_id,
    name,
    name_sub,
    gender,
    age,
    department_id,
    major_id,
    class_id,
    subject_id,
    grade,
    total_unit
    )
values(
    '2004230011',
    '西結都',
    'ニシユイト',
    '男性',
    21,
    1,
    2,
    7,
    13,
    3,
    2
);
insert into student (
    student_id,
    name,
    name_sub,
    gender,
    age,
    department_id,
    major_id,
    class_id,
    subject_id,
    grade,
    total_unit
    )
values(
    '2004230011',
    '西結都',
    'ニシユイト',
    '男性',
    21,
    1,
    2,
    7,
    12,
    3,
    2
);
### こがと俺のじゃヴぁ中級追加
