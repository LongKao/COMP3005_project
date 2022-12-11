Create tables

CREATE TABLE users(
    id int PRIMARY KEY,
    name varchar(20) NOT NULL,
    username varchar(20) NOT NULL,
    password varchar(20) NOT NULL,
    shipping_address varchar(40),
    billing_address varchar(40)
)
    
CREATE TABLE book(
    ISBN varchar(13) PRIMARY KEY,
    author varchar(40),
    name varchar(40),
    genre varchar(20),
    publisher varchar(20),
    page_num int,
    price numeric(4,2),
    foreign key (publisher) references publisher(name)
);

CREATE TABLE orders(
    id int PRIMARY KEY,
    uid int,
    book_list varchar(100),
    shipping_address varchar(40),
    billing_address varchar(40),
    total_cost numeric(4,2),
    foreign key (uid) references users(id)
);

CREATE TABLE order_book(
    id int PRIMARY KEY,
    order_id int
    author varchar(40),
    name varchar(40),
    genre varchar(20),
    publisher varchar(20),
    price numeric(4,2),
    foreign key (order_id) references orders(id)
    	on delete cascade
);

CREATE TABLE owner(
    id int PRIMARY KEY,
    username varchar(20) NOT NULL,
    password varchar(20) NOT NULL
);

CREATE TABLE publisher(
    id int PRIMARY KEY,
    name varchar(20) unique,
    address varchar(20),
    email varchar(20),
    phone_num varchar(20),
    bank_account varchar(20)
);

create table stock(
    ISBN varchar(13) PRIMARY KEY,
    quantity int,
    foreign key (ISBN) references book(ISBN)
        on delete cascade
)
---------------
Insert values

insert into users values(1, 'Will Hohenzolern', 'WHohen', '123456', 'New Branswick');
insert into users values(2, 'John Doe', 'JDoe', 'imjohn', 'Ottawa');

insert into book values('9781560772316', 'Erich Maria Remarque', 'All Quiet on the Western Front', 'War novel', 'Propyläen Verlag', 200, 10.99);
insert into book values('0141180145', 'Mikhail Bulgakov', 'The Master and Margarita', 'Romance', 'YMCA Press', 372, 9.99);

insert into publisher values(1, 'Propyläen Verlag', 'Berlin, Germany', 'pverlag@gmail.com', '+13435443456', '4965633363956189');
insert into publisher values(2, 'YMCA Press', 'Paris, France', 'ymcap@gmail.com', '+13437653753', '4195140329068762');

insert into owner values(1, 'WH', 'mine');

insert into stock values('9781560772316', 20);
insert into stock values('0141180145', 20)