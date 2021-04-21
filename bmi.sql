drop table if exists bmi;
drop database if exists bmidb;
create database if not exists bmidb;
use bmidb;
create table if not exists bmi(
pid int primary key AUTO_INCREMENT,
name varchar(50) not null,  
age int(3) unsigned not null,
phone bigint unsigned not null UNIQUE,
gender enum('Male','Female') not null,
height float(4,2) not null,
weight float(5,2) not null,
result float(5,2),
currentDate date default (NOW())
);
