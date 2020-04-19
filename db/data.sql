--
-- ���� ������������ � ������� SQLiteStudio v3.2.1 � �� ��� 16 17:45:38 2020
--
-- �������������� ��������� ������: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- �������: products
CREATE TABLE products (
	id INTEGER NOT NULL, 
	name VARCHAR, 
	seller INTEGER, 
	price INTEGER, 
	address VARCHAR, 
	PRIMARY KEY (id), 
	UNIQUE (name), 
	FOREIGN KEY(seller) REFERENCES users (id)
);
INSERT INTO products (id, name, seller, price, address) VALUES (1, '��������� �����', 1, 1000, '��. ������� ������ 31/1');
INSERT INTO products (id, name, seller, price, address) VALUES (2, '����� �����', 1, 1000, '������� �������');
INSERT INTO products (id, name, seller, price, address) VALUES (3, '������������ �����', 1, 1000, '�������');
INSERT INTO products (id, name, seller, price, address) VALUES (4, '�����', 1, 1000, '�������');

-- �������: sales
CREATE TABLE sales (
	id INTEGER NOT NULL, 
	seller INTEGER, 
	item INTEGER, 
	sold_status BOOLEAN, 
	modified_date DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(seller) REFERENCES users (id), 
	FOREIGN KEY(item) REFERENCES products (id), 
	CHECK (sold_status IN (0, 1))
);

-- �������: users
CREATE TABLE users (
	id INTEGER NOT NULL, 
	surname VARCHAR, 
	name VARCHAR, 
	email VARCHAR, 
	privileges BOOLEAN, 
	hashed_password VARCHAR, 
	modified_date DATETIME, 
	PRIMARY KEY (id), 
	CHECK (privileges IN (0, 1))
);
INSERT INTO users (id, surname, name, email, privileges, hashed_password, modified_date) VALUES (1, '������', '�����', 'ahatov@mail.ru', 1, 'pbkdf2:sha256:150000$xBphkQss$4a9198548cc0a4901df2a17dd448fdcb9dff026279800c595eafd9920fcf91dc', '2020-04-11 11:40:58.000000');
INSERT INTO users (id, surname, name, email, privileges, hashed_password, modified_date) VALUES (2, 'Kulikov', 'Vlad', 'test@test.com', 1, 'pbkdf2:sha256:150000$MOh8y4eJ$1d1296f39b40f6eb941e77b32368aea66ee95c0fa0f1b440c682075702e2e5e1', '2020-04-11 22:10:52.000000');

-- ������: ix_users_email
CREATE UNIQUE INDEX ix_users_email ON users (email);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
