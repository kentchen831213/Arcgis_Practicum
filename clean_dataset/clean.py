import csv


def deal_with_initial(instring):
    res = instring[:2]
    return "".join(res.upper())

def deal_with_date(datestring):
    res = datestring.split(" ")
    return res[0]

def deal_with_windspeed(speedstring):
    res = speedstring.split("_")
    if res[-1] == "calm" or len(res)==1:
        return res[-1].title()
    else:
        return res[-2].title()+" "+res[-1].title()

# open the original data csv file
file = open('DragPts_eDNA28May21_OriginalExport.csv')
csvreader = csv.reader(file)

# create an output file
writer = csv.writer(open('output.csv','w',newline=''))
head = ["ObjectID",	"GlobalID",	"Initials",	"CollDate",	"FieldCrew", "SiteName", "County", "Comment_OpenText", "WindSpeed",	"CloudCover",
        "HabitatType",	"eDNA_Smpl", "RandomNum_ID", "Number of ticks found",	"SampleID",	"eDNA_SmplID",	"Coord_X",	"Coord_Y",	"RecCheck"]
writer.writerow(head)

# 1	6622b5e3-7f68-4c8e-9f87-a0cee224fd26	JT	6/1/2021	Lee, Tinoco, Kopsco, UruchimaLamczykProperty	Jefferson
# Its on & on drizzling 	Calm	OVC	Gr			0			-88.9756348	38.3032935
rows = []
i = 0
for idx, row in enumerate(csvreader):
    if idx == 0 or idx == 1: continue
    currow = []
    currow.append(row[0])
    currow.append(row[1])
    currow.append(deal_with_initial(row[3]))
    currow.append(deal_with_date(row[2]))
    currow.append(row[7])
    currow.append(" ")
    currow.append(row[11])
    currow.append(row[20])
    currow.append(deal_with_windspeed(row[21]))
    writer.writerow(currow)

