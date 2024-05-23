-- Create User Optibreed
CREATE USER IF NOT EXISTS 'optibreed'@'localhost' IDENTIFIED BY 'optibreed';
GRANT ALL PRIVILEGES ON *.* TO 'optibreed'@'localhost';

-- Create Database optibteed
CREATE DATABASE IF NOT EXISTS `optibreed`;
