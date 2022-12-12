create table majors (
    id serial PRIMARY KEY NOT NULL,
    major varchar(20) NOT NULL,
    department_id int NOT null,
    grade int not null,

    FOREIGN KEY(department_id)
    REFERENCES departments(id)
);
insert into majors(
    major,
	department_id,
    grade
    )
values(
    'ホワイトハッカー',
	1,
    3
);

insert into majors(
    major,
	department_id,
    grade
    )
values(
    'AIクリエーター',
	1,
    
    3
);
insert into majors(
    major,
	department_id,
    grade
    )
values(
    'ホワイトハッカー',
	1,
    2
);

insert into majors(
    major,
	department_id,
    grade
    )
values(
    'AIクリエーター',
	1,
    2
);
insert into majors(
    major,
	department_id,
    grade
    )
values(
    'ホワイトハッカー',
	1,
    1
);

insert into majors(
    major,
	department_id,
    grade
    )
values(
    'AIクリエーター',
	1,
    1
);
insert into majors(
    major,
	department_id,
    grade
    )
values(
    'ホワイトハッカー',
	1,
    4
);

insert into majors(
    major,
	department_id,
    grade
    )
values(
    'AIクリエーター',
	1,
    4
);