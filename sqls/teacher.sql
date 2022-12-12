create table teacher (
    id serial PRIMARY KEY NOT NULL,
    teacher_id varchar(6) NOT NULL,
    name varchar(30) NOT NULL,
    name_sub varchar(30) NOT NULL,
    age int NOT NULL,
    gender varchar(5) NOT NULL,
    subject_id int,
    major_id int,
    password  varchar(255) NOT NULL,
    FOREIGN KEY(subject_id) 
    REFERENCES subjects(id),

    FOREIGN KEY(major_id)
    REFERENCES majors(id)
);
insert into teacher(
	teacher_id,
    name,
    name_sub,
    age,
    gender,
    subject_id,
	major_id,
    password
    )
values(
	'000713',
    '織田美代子',
    'オリタミヨコ',
    18,
    '女性',
    1,
	1,
	'$2b$12$pZ4VjLKzarfyLMxkROAu2.k5axzw..e2HhcS1MO5Ew9ApKjUMcZ3K'
);

insert into teacher(
	teacher_id,
    name,
    name_sub,
    age,
    gender,
    subject_id,
	major_id,
    password
    )
values(
	'000713',
    '織田美代子',
    'オリタミヨコ',
    18,
    '女性',
    2,
	2,
	'$2b$12$pZ4VjLKzarfyLMxkROAu2.k5axzw..e2HhcS1MO5Ew9ApKjUMcZ3K'
);

insert into teacher(
	teacher_id,
    name,
    name_sub,
    age,
    gender,
    password
    )

values(
	'000000',
    '丸山克樹',
    'マルヤマカツキ',
    30,
    '男性',
	'$2b$12$rZEeJQx9lJc0TS/uLnbsSOm0pw90FtP97tcb61EvBMXpVBh/kjEwi'
);

insert into teacher(
	teacher_id,
    name,
    name_sub,
    age,
    gender,
    password
    )
values(
	'000713',
    '織田美代子',
    'オリタミヨコ',
    18,
    '女性',
	'$2b$12$pZ4VjLKzarfyLMxkROAu2.k5axzw..e2HhcS1MO5Ew9ApKjUMcZ3K'
);
