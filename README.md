Details:
======

This Script takes VPC IDs as the input (in the constants.py file).

The Script then takes the user input for the CIDR blocks to search for (to Delete from the above VPC IDs), looks into the Route Tables for the VPCs and deletes the relevant Routes

Output:
=====

1. It will print out the details of the matching routes and check with you if you would like to make route changes. If yes, it will Delete the routes
2. If not, it will exit the Loop
3. Once the Routes are Deleted, it will check if you would like to revert the changes. If yes, it will revert all the changes. If not, the program will exit

