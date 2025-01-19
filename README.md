# Managing Olive Oil Production Datasets For A Blockchain

## Purpose of the project
This program will be used by database administrator for a company the uses a blockchain technology to monitor and manage olive oil production trends every half a decade. 

The main purpose of this project is the create a python program that that allows a user to interact and edit a dataset (in csv format) on olive oil production in portuguese regions. 

## Essential Components
### File: project.py

This file contains the python code for operating on the csv file *olive_oil_census2020*, it will read and write in the csv file according to the user's input allowing them to :

- Add new records
- Search for records according to there prod_ID or a combinations of other parameters
- Edit the quantities of the records
- Delete records
### File: olive_oil_census2020.csv

A comma-separated value file which contains the data that will be operated on. The data consists of olive production (ton), olive oil production (hl) and oil press units quantities, in accordance to:

- Year: years used consist of 1995, 2000, 2005, 2010, 2015 and 2020
- Region: with the geographical level of portuguese agrarian regions
- Type of oil press unit: Private, Cooperative and Industrial
- Method of extraction: Traditional, Continuous 2 or 3 phase and Other
### File: test_project.py
Test file for our *project.py* code, which allows us to run unit tests for the respective functions ensuring that the program is operating as it should. To avoid altering the data during these tests, a test_file was generated (*test_olive_oil_census2020.csv*)
### File: requirements.txt

A file which contains all the libraries used for the execution of this project, which can be downloaded by pip -install.
