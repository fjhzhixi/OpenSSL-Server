CREATE DATABASE netdisk;
USE netdisk;

CREATE TABLE User(
    UserId varchar(32) NOT NULL,
    Password varchar(32) NOT NULL,
    UserName varchar (32),
    PRIMARY KEY (UserId)
);

CREATE TABLE File(
    FileId INT AUTO_INCREMENT NOT NULL,
    FileName varchar(128) NOT NULL,
    FilePath varchar(128) NOT NULL,
    UserId varchar(32) NOT NULL,
    UploadDate timestamp NOT NULL,
    PRIMARY KEY (FileId)
)