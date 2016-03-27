# Full-Stack-Web-Developer-Nanodegree-P2

Understand the purpose of each file

-tournament.sql  - this file is used to set up your database schema (the table representation of your data structure).
-tournament.py - this file is used to provide access to your database via a library of functions which can add, delete or query data in your database to another python program (a client program). Remember that when you define a function, it does not execute, it simply means the function is defined to run a specific set of instructions when called.
-tournament_test.py - this is a client program which will use your functions written in the tournament.py module. We've written this client program to test your implementation of functions in tournament.py

To create the database:
vagrant@trusty32: psql => \i tournament.sql 

To run the series of tests defined in this test suite, run the program from the command line $ python tournament_test.py
