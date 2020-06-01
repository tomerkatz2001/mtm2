

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
                    if(item["competitor id"]==int(data[2]) and item["competition name"]==data[1]):
                        cheater=True
                        database.remove(item)
                if(not cheater):
                    item={}
                    item["competition name"]=data[1]
                    item["competition type"]=data[3]
                    item["competitor id"]=int(data[2])
                    item["competitor country"]=id_to_country[data[2]]
                    item["result"]=int(data[4])
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
        if (size >= 3):
            sum_list.append([competition, type_dict[competition][0]["competitor country"],
                             type_dict[competition][1]["competitor country"],
                             type_dict[competition][2]["competitor country"]])
    return sum_list


def calcCompetitionsResults(competitors_in_competitions):
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


def printCompetitor(competitor):
    '''
    Given the data of a competitor, the function prints it in a specific format.
    Arguments:
        competitor: {'competition name': competition_name, 'competition type': competition_type,
                        'competitor id': competitor_id, 'competitor country': competitor_country,
                        'result': result}
    '''
    competition_name = competitor['competition name']
    competition_type = competitor['competition type']
    competitor_id = competitor['competitor id']
    competitor_country = competitor['competitor country']
    result = competitor['result']

    assert (isinstance(result, int))  # Updated. Safety check for the type of result

    print(f'Competitor {competitor_id} from {competitor_country} participated in {competition_name} ({competition_type}) and scored {result}')


def printCompetitionResults(competition_name, winning_gold_country, winning_silver_country, winning_bronze_country):
    '''
    Given a competition name and its champs countries, the function prints the winning countries
        in that competition in a specific format.
    Arguments:
        competition_name: the competition name
        winning_gold_country, winning_silver_country, winning_bronze_country: the champs countries
    '''
    undef_country = 'undef_country'
    countries = [country for country in [winning_gold_country, winning_silver_country, winning_bronze_country] if
                 country != undef_country]
    print(f'The winning competitors in {competition_name} are from: {countries}')


def key_sort_competitor(competitor):
    '''
    A helper function that creates a special key for sorting competitors.
    Arguments:
        competitor: a dictionary contains the data of a competitor in the following format:
                    {'competition name': competition_name, 'competition type': competition_type,
                        'competitor id': competitor_id, 'competitor country': competitor_country,
                        'result': result}
    '''
    competition_name = competitor['competition name']
    result = competitor['result']
    return (competition_name, result)






def partA(file_name='input.txt', allow_prints=True):
    # read and parse the input file
    competitors_in_competitions = readParseData(file_name)
    if allow_prints:
        # competitors_in_competitions are sorted by competition_name (string) and then by result (int)
        for competitor in sorted(competitors_in_competitions, key=key_sort_competitor):
            printCompetitor(competitor)

    # calculate competition results
    competitions_results = calcCompetitionsResults(competitors_in_competitions)
    if allow_prints:
        for competition_result_single in sorted(competitions_results):
            printCompetitionResults(*competition_result_single)

    return competitions_results

import Olympics
def partB(file_name='input.txt'):
    competitions_results = partA(file_name, allow_prints=False)
    olympic=Olympics.OlympicsCreate()
    for item in competitions_results:
        Olympics.OlympicsUpdateCompetitionResults(olympic,str(item[1]),str(item[2]),str(item[3]))
    Olympics.OlympicsWinningCountry(olympic)
    Olympics.OlympicsDestroy(olympic)
    # TODO Part B


if __name__ == "__main__":
    '''
    The main part of the script.
    __main__ is the name of the scope in which top-level code executes.

    To run only a single part, comment the line below which correspondes to the part you don't want to run.
    '''
    file_name = 'input.txt'

    partA("2020.txt")
    partB("2020.txt")


