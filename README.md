# IC_Cache_Coding_Exercise
## Project Details:
The project consists of two python programs:
generate.py : Generates the logs for one day(today) for n(1000) servers, where each server has 2 CPUs, and writes the data to CSV file in the provided directory path.
query.py : Implements a command line tool which takes a directory of data files as a parameter and lets you query CPU usage for a specific CPU in a given time period. It is an interactive command line tool which read a user’s commands from stdin.

And two shell scripts:
generate.sh : Runs generate.py program
query.sh : Runs query.py program

## Required Tools: 
Python 3.7

## How to run and sample output:
### To run generate.sh in Linux:
> ./generate.sh [DATA_PATH]

### Sample Output:
Generating logs for 1000 servers at DATA_PATH=[DATA_PATH] for date: 2021-06-24
Done.

### To run query.sh in Linux:
> ./query.sh [DATA_PATH]

### Sample Output:
> >QUERY 192.168.1.10 1 2021-06-23 01:05 2021-06-23 01:10

CPU1 usage on 192.168.1.10:

(2021-06-23 01:05:00, 12%),(2021-06-23 01:06:00, 49%),(2021-06-23 01:07:00, 55%),(2021-06-23 01:08:00, 46%),(2021-06-23 01:09:00, 94%)

> >EXIT
