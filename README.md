USG Election Parsing
====================================

About
------------------------------------
USG requires custom logic in voting that CollegiateLink doesn't support. It used
to be two things:
1. An easy way to tally the votes
2. Votes from undecided majors in *multiple constituencies* should be voided.

CollegiateLink has (generously) already implemented #1. However, until there is
an adequate solution for the second problem, elections will always require a
large amount of manual data manipulations.

This script will accomplish #1 and #2 given the output of a CollegiateLink
election. In the Spring 2012 elections, it made tallying the votes take about 5
minutes!

Using this Script
------------------------------------
First, download the CSV of Election Results from CollegiateLink. This is the
"Export All Votes" button on the Election's "Results" tab.

You can run the script by executing `python parse_results.py
ElectionResults.csv`

It will automatically detect anyone who is running for a Representative position
(because their names will be the only ones in their respective columns) and ask
you to group them into constituencies manually. It doesn't matter how you do
this, just make sure that you **copy+paste the same, exact string** into people
of the same constituency.

Automatic Constituency Input
------------------------------------
Assuming you're running this on a Mac/Linux machine, you can use the power of
Unix to make life easier! Simply create a file constituencies.txt with lines like

    Arts & Sciences Representative
    Arts & Sciences Representative
    Arts & Sciences Representative
    Arts & Sciences Representative
    Arts & Sciences Representative
    Engineering Representative
    Engineering Representative
    Engineering Representative
    Engineering Representative
    Engineering Representative

for each of the input boxes. Then, you can run the script like

    cat constituencies.txt | python parse_results.py ElectionResults.csv

TODO
------------------------------------
* This script does not have any logical organization to it. I wish it used more advanced organizational principles.
* The script outputs a lot of extraneous text. Ideally it shouldn't, but it would still be nice to output verifying information to somewhere.
