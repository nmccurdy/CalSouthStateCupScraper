'''
Created on Mar 10, 2019

@author: mccurdy
'''

import io


'''
Created on Feb 18, 2019

@author: mccurdy
'''
import csv
from operator import itemgetter


# using webscraper.io
# 
# {"_id":"calsouth","startUrl":["https://cysa.affinitysoccer.com/tour/public/info/schedule_results2.asp?sessionguid=&flightguid=1E4603F8-107D-44D6-BE95-B79909C0A411&RoundType=1&sortby=Group&tournamentguid=736CB8A4-29BA-4CF3-9EEB-EC74F7E94383&BeginDate=&EndDate="],"selectors":[{"id":"groups","type":"SelectorElement","parentSelectors":["_root"],"selector":"table:nth-of-type(5) table table tbody","multiple":true,"delay":0},{"id":"teams","type":"SelectorElement","parentSelectors":["groups"],"selector":"tr:nth-of-type(n+5)","multiple":true,"delay":0},{"id":"teamname","type":"SelectorText","parentSelectors":["teams"],"selector":"nobr a","multiple":false,"regex":"","delay":0},{"id":"points","type":"SelectorText","parentSelectors":["teams"],"selector":"td.theadb","multiple":false,"regex":"","delay":0},{"id":"groupname","type":"SelectorText","parentSelectors":["groups"],"selector":"tr.theadb:nth-of-type(2) td.tbodyb:nth-of-type(2)","multiple":false,"regex":"","delay":0},{"id":"goaldiff","type":"SelectorText","parentSelectors":["teams"],"selector":"td.tbody:nth-of-type(7) nobr","multiple":false,"regex":"","delay":0},{"id":"goalsagainst","type":"SelectorText","parentSelectors":["teams"],"selector":"td.tbody:nth-of-type(8) nobr","multiple":false,"regex":"","delay":0},{"id":"goalsfor","type":"SelectorText","parentSelectors":["teams"],"selector":"td.tbody:nth-of-type(9) nobr","multiple":false,"regex":"","delay":0},{"id":"shutouts","type":"SelectorText","parentSelectors":["teams"],"selector":"td.tbody:nth-of-type(10) nobr","multiple":false,"regex":"","delay":0},{"id":"game1","type":"SelectorText","parentSelectors":["teams"],"selector":"td.tbody:nth-of-type(3)","multiple":false,"regex":"","delay":0},{"id":"game2","type":"SelectorText","parentSelectors":["teams"],"selector":"td.tbody:nth-of-type(4)","multiple":false,"regex":"","delay":0},{"id":"game3","type":"SelectorText","parentSelectors":["teams"],"selector":"td.tbody:nth-of-type(5)","multiple":false,"regex":"","delay":0}]}

class FileWithUniversalNewLine(object):

    def __init__(self, file_obj):
        self.file = file_obj

    def lines(self):
        buff = ""  # In case of reading incomplete line, buff will temporarly keep the incomplete line
        while True:
            line = self.file.read(2048)
            if not line:
                if buff:
                    yield buff
                raise StopIteration

            # Convert all new lines into linux new line
            line = buff + line.replace("\r\n", "\n").replace("\r", "\n")
            lines = line.split("\n")
            buff = lines.pop()
            for sline in lines:
                yield sline

    def close(self):
        self.file.close()

    def __exit__(self, *args, **kwargs):
        return self.file.__exit__(*args, **kwargs)

    def __enter__(self, *args, **kwargs):
        return self

    def __iter__(self):
        return self.lines()



file = open("f://downloads/calsouth (3).csv")
fileFixed = FileWithUniversalNewLine(file)


dialect='excel'

data = csv.DictReader(fileFixed, dialect=dialect)

data = list(data)

data = sorted(data, key=lambda x: int(x['shutouts']), reverse=True)
data = sorted(data, key=lambda x: int(x['goalsfor']), reverse=True)
data = sorted(data, key=lambda x: int(x['goalsagainst']))
data = sorted(data, key=lambda x: int(x['goaldiff']), reverse=True)
data = sorted(data, key=lambda x: int(x['points']), reverse=True)

print(",".join(["rank", "team", "points", "goaldiff", "goalsagainst", "goalsfor", "shutouts"]))
for i, d in enumerate(data):
    complete=""
    if d["game1"] == "" or d['game2'] == "" or d['game3'] == "":
        complete="*"
    print(",".join([str(i+1), complete+d["teamname"], d["points"], d["goaldiff"], d["goalsagainst"], d["goalsfor"], d["shutouts"]]))
