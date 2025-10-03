-- create database bank_info
use bank_info;

----- Admin Table ------
CREATE TABLE admin_info(name varchar(32),pin INT not null);    
insert into admin_info values("Madhu",4447);
select *from admin_info;

-- ---- User Table --------
create table user_bank_info(Name varchar(32), account_number INT not null primary key, account_type varchar(32), account_balance int default 0, 
account_pin int not null, date_of_create datetime default current_timestamp);  
select *from user_bank_info;

insert into user_bank_info(Name,account_number,account_type,account_balance,account_pin) values("vardhan",2345,"savings",2000,1234);
UPDATE user_bank_info
SET account_balance = account_balance + 5000
WHERE account_number = 2345;

-- ------Transaction table ------
create table transaction_details(transaction_no int not null,account_number INT not null, transaction_type varchar(32), amount int not null,
 date_of_transaction datetime default current_timestamp , foreign key (account_number) REFERENCES user_bank_info(account_number));
-- insert into transaction_details(transaction_no,account_number,transaction_type,amount) values(1,2345,"savings",10000);
select * from transaction_details;

desc transaction_details;
desc user_bank_info;