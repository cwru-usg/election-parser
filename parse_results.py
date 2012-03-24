# ARG1:   Election Results CSV from CollegiateLink.
import sys
import re
from operator import itemgetter
from collections import Counter

columns = {}
headers = []
qc_lines = 0
qc_votes = 0
qc_invalid_lines = 0
qc_valid_lines = 0
qc_multiple_constituencies = 0
f = open(sys.argv[1], "r")
for i in f:
    qc_lines += 1
    j = i.strip().split('","')
    # Check if this is the header line:
    if j[0][0:13] == "SubmissionId,":
        headers = j
    # If this is a valid vote then it will begin like
    #  "99999
    if re.match('"[0-9]*', j[0]) == None:
        print "Found invalid line... (%s)" % (j[0])
        qc_invalid_lines += 1
        continue
    for col_id,one_column in enumerate(j):
        if col_id == 0:
            continue
        # Initialize if necessary:
        if col_id not in columns:
            columns[col_id] = []
        # Append this result to that column...
        # ...if there is actually a result
        if one_column != "" and one_column != '"':
            columns[col_id].append(one_column)
    qc_valid_lines += 1
f.close()

################################################
# Parse the representatives first, removing bad entries.
################################################
# Categorize the names of people who are all alone in their column. These are
# the checkbox lists for schools.
constituencies = {}
for col,votes in columns.items():
    different_things = {}
    for x in votes:
        different_things[x] = 1
    if len(different_things.keys()) == 1:
        constituencies[col] = raw_input("Enter the constituency of %s: " % (different_things.keys()[0]))

# Now, reparse the files, removing all people who voted in multiple
# constituencies.

f = open(sys.argv[1], "r")
discarded = []
count_votes = []
for i in f:
    j = i.strip().split('","')
    # Check if this is the header line:
    if j[0][0:13] == "SubmissionId,":
        continue
    if re.match('"[0-9]*', j[0]) == None:
        continue
    votes = {}
    vote_constituencies = set()
    for col_id,one_column in enumerate(j):
        if col_id == 0:
            continue
        # Append this result to that column...
        # ...if there is actually a result
        if one_column != "" and one_column != '"':
            votes[col_id] = one_column
            if col_id in constituencies:
                vote_constituencies = vote_constituencies.union(
                        (constituencies[col_id],) )
    if len(vote_constituencies) > 1:
        qc_multiple_constituencies += 1
        # Remove the votes from all constituencies, then.
        print "Discarded ID: %s" % (j[0],)
        for constituency_id in constituencies.keys():
            if constituency_id in votes:
                discarded.append(votes[constituency_id])
                del votes[constituency_id]
    qc_votes += 1
    count_votes.append(votes)
f.close()

# count votes is an array of votes, like
# [{1: 'Navein Arumugasaamy', 2: 'Sharif Sabe', 3: 'Ellen Schloff' ...}, {1:
# ...}]

################################################
# Now that the bad votes are removed, let's count the votes.
################################################
tally = {}
for vote in count_votes:
    for col_id, decision in vote.items():
        if col_id not in tally:
            tally[col_id] = {}
        if decision not in tally[col_id]:
            tally[col_id][decision] = 0
        tally[col_id][decision] += 1

################################################
# Votes are counted, now to display them.
# tally = {2: {'Sarah Catherine Pfister': 19, 'Nitya Sivakumar': 9, 'Sean
#         McCarthy': 7}, 4: {'Laura Payne': 23, 'Abstain': 1}
################################################
f = open("output.txt", "w")

# First, display the votes by constituency:
constituency_names = set(constituencies.values())
for one_contituency_name in constituency_names:
    print "Constituency: %s" % (one_contituency_name,)
    temp_people_in_constituency = {}
    for col_id, target_constituency_name in constituencies.items():
        if target_constituency_name == one_contituency_name:
            person = tally[col_id].keys()[0] # Only one key in each.
            temp_people_in_constituency[person] = tally[col_id][person]
            del tally[col_id]
    for person, votes in reversed(sorted(temp_people_in_constituency.items(),
            key=itemgetter(1))):
        print "\t%s: %s" % (person.ljust(25,"_"), votes)

# Next, display the other votes.
for col_id, results in tally.items():
    if col_id <= len(headers): # It looks like the columns get off by one in the beginning
        print "Vote Item %s: %s" % (col_id,headers[col_id-1][0:min(len(headers[col_id-1])-2,30)],)
        for person, votes in reversed(sorted(results.items(),
                key=itemgetter(1))):
            print "\t%s: %s" % (person.ljust(25,"_"), votes)

######################################
# All done! Print the quality control information.
######################################
print "======QUALITY CONTROL======"
print "  File has %s lines (%s valid, %s invalid)." % (qc_lines, qc_valid_lines, qc_invalid_lines)
print "  Undecided voters who voted in multiple constituencies: %s" % (qc_multiple_constituencies,)
print "  Sum of votes is %s" % (qc_votes)
print "  Discarded votes for: %s " % (dict(Counter(discarded)),)

"""
# Okay, so now we have parsed the election results into a table. Now
# let's iterate through it and print the results.
qc_votes = 0
for col,votes in columns.items():
    if len(votes) == 0:
        continue
    options = {}
    for j in votes:
        if j not in options:
            options[j] = 0
        options[j] += 1
    print "============"
    for candidate,votes in sorted(options.items(), key=lambda (k,v): (v,k), reverse=True):
        print "    %s   -> %s votes" % (candidate, votes)
        qc_votes += votes
    print "============"

# Print some quality control information
print "======QUALITY CONTROL======"
print "  File has %s lines (%s valid, %s invalid)." % (qc_lines, qc_valid_lines, qc_invalid_lines)
print "  Sum of votes is %s" % (qc_votes)
"""
