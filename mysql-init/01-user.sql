DROP USER IF EXISTS 'judicia'@'%';
CREATE USER 'judicia'@'%' IDENTIFIED BY 'Judicia%402025';
GRANT ALL PRIVILEGES ON judiciadb.* TO 'judicia'@'%';
FLUSH PRIVILEGES;