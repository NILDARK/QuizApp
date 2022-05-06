-- run these queries in your work bench sql file

-- create database
create database quiz;
use quiz;
-- create tables for database
create table questions (qid int primary key,que text,ans_id int,opt_id1 int,opt1 text,opt2 text,opt_id2 int,opt3 text,opt_id3 int,opt4 text,opt_id4 int);
create table registeredclients (username varchar(12) primary key,client_name varchar(100),client_password varchar(16),client_email varchar(50),client_age int, dateofregistration date);
create table logtable (serialno int auto_increment primary key,username varchar(12),datetimeoflogin timestamp,datetimeofsigningout timestamp);
create table student_scores (sr_no int auto_increment key,username varchar(12),score int,timestampofattempt timestamp);

-- query to insert questions
insert into questions values(1,'que text',2,1,'opt1',2,'opt2',3,'opt3',4,'opt4'); -- add values in same format