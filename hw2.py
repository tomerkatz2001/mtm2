


def readParseData(file_name):
        file=open(file_name,'r')
        line=file.readline()
        id_to_country={}
        database=[]
        cheater=False
        while line:
            data=line.split()
            if(data[0]=="competitor"):
                id_to_country[data[1]]=data[2]
            line=file.readline()
        file.close()
        file=open(file_name,'r')
        line=file.readline()
        while line:
            data=line.split()
            if(data[0]=="competition"):
                for item in database:
                    if(item["competitor id"]==data[2] and item["competition name"]==data[1]):
                        cheater=True
                        database.remove(item)
                if(not cheater):
                    item={}
                    item["competition name"]=data[1]
                    item["competition type"]=data[3]
                    item["competitor id"]=data[2]
                    item["competitor country"]=id_to_country[data[2]]
                    item["result"]=data[4]
                    database.append(item)
            cheater=False
            line = file.readline()

        return database



def getNameOfCompetition(parameter_dict):
    return parameter_dict["competition name"]


def getScoreOfCompetition(dict):
    return dict["result"]


def sumAllUp(type_set, type_dict):
    sum_list = []
    for competition in type_set:
        size = len(type_dict[competition])
        if (size == 0):
            continue
        if (size == 1):
            sum_list.append(
                [competition, type_dict[competition][0]["competitor country"], 'undef_country', 'undef_contry'])
        if (size == 2):
            sum_list.append([competition, type_dict[competition][0]["competitor country"],
                             type_dict[competition][1]["competitor country"], 'undef_country'])
        if (size == 3):
            sum_list.append([competition, type_dict[competition][0]["competitor country"],
                             type_dict[competition][1]["competitor country"],
                             type_dict[competition][2]["competitor country"]])
    return sum_list


def calcCompetitionResults(competitors_in_competitions):
    timed_list = []
    untimed_list = []
    knockout_list = []
    competitions_set = set()
    for element in competitors_in_competitions:
        competitions_set.add(element["competition name"])
        if (element["competition type"] == "timed"):
            timed_list.append(element)
        if (element["competition type"] == "untimed"):
            untimed_list.append(element)
        if (element["competition type"] == "knockout"):
            knockout_list.append(element)

    timed_set = set()
    untimed_set = set()
    knockout_set = set()

    new_list1 = sorted(timed_list, key=getNameOfCompetition)
    timed_list = new_list1
    for competiton in timed_list:
        timed_set.add(competiton["competition name"])

    new_list2 = sorted(untimed_list, key=getNameOfCompetition)
    untimed_list = new_list2
    for competiton in untimed_list:
        untimed_set.add(competiton["competition name"])

    new_list3 = sorted(knockout_list, key=getNameOfCompetition)
    knockout_list = new_list3
    for competiton in knockout_list:
        knockout_set.add(competiton["competition name"])

    timed_dict = {}
    untimed_dict = {}
    knockout_dict = {}

    for competiton in timed_set:
        timed_dict[competiton] = []
        for competetor in timed_list:
            if (competetor["competition name"] == competiton):
                timed_dict[competiton].append(competetor)

    for competiton in untimed_set:
        untimed_dict[competiton] = []
        for competetor in untimed_list:
            if (competetor["competition name"] == competiton):
                untimed_dict[competiton].append(competetor)

    for competiton in knockout_set:
        knockout_dict[competiton] = []
        for competetor in knockout_list:
            if (competetor["competition name"] == competiton):
                knockout_dict[competiton].append(competetor)

    for competiton in timed_set:
        new_list4 = sorted(timed_dict[competiton], key=getScoreOfCompetition)
        timed_dict[competiton] = new_list4

    for competiton in untimed_set:
        new_list5 = sorted(untimed_dict[competiton], key=getScoreOfCompetition, reverse=True)
        untimed_dict[competiton] = new_list5

    for competiton in knockout_set:
        new_list6 = sorted(knockout_dict[competiton], key=getScoreOfCompetition)
        knockout_dict[competiton] = new_list6

    returned_list = (sumAllUp(timed_set, timed_dict)) + (sumAllUp(untimed_set, untimed_dict)) + (
    sumAllUp(knockout_set, knockout_dict))

    return returned_list


print(readParseData("2020.txt"))
print(calcCompetitionResults(readParseData("2020.txt")))
