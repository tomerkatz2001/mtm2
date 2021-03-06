

def readParseData(file_name):
    '''
    Reads a olympics database from a file
    Arguments:
        file_name- then name of the file to read the DB from.
    Return:
        The database- a list of dictionaries in this format: {'competition name': competition_name, 'competition type': competition_type,
                        'competitor id': competitor_id, 'competitor country': competitor_country,
                        'result': result}
    '''
    file=open(file_name,'r')#Open the file for reading
    line=file.readline()#Read the first line
    id_to_country={}#This is a dictionary that will be used to map competitor ids to their countries
    database=[]#The list that will contain the database
    while line:#Loop through each line, fine the lines that start with competitor and map the competitora ids to their country in the dictionary we created.
        data=line.split()
        if(data[0]=="competitor"):
            id_to_country[data[1]]=data[2]
        line=file.readline()
    file.close()#Close and reopen the file
    file=open(file_name,'r')
    line=file.readline()
    while line:#Loop through the file again, This time for each line that starts with competition add the data to the DB
        data=line.split()
        if(data[0]=="competition"):
            item={}
            item["competition name"]=data[1]
            item["competition type"]=data[3]
            item["competitor id"]=int(data[2])
            item["competitor country"]=id_to_country[data[2]]
            item["result"]=int(data[4])
            database.append(item)
        line = file.readline()
    file.close()
    return database#Return the DB



def getNameOfCompetition(parameter_dict):
    '''
    This function gets a dictionary from the olympics DB list and returns the competition name
    '''
    return parameter_dict["competition name"]


def getScoreOfCompetition(dict):
    '''
    This function gets a dictionary from the olympics DB list and returns the result
    '''
    return dict["result"]


def sumAllUp(type_set, type_dict):
    '''
    This method gets a dict and returns the results of the competitions(a list of the top 3 countries)
    Arguments:
        type_set- A set of all of the competitions from this type.
        type_dict- A dictionary of this competition type, mapping each competition to the competitors, sorted by results.
    '''
    sum_list = []
    for competition in type_set:#For each competition, add a list of the top 3 countries to the list, if there is less the 3 countries, add undef_country as countries.
        size = len(type_dict[competition])
        if (size == 0):
            continue
        if (size == 1):
            sum_list.append(
                [competition, type_dict[competition][0]["competitor country"], 'undef_country', 'undef_country'])
        if (size == 2):
            sum_list.append([competition, type_dict[competition][0]["competitor country"],
                             type_dict[competition][1]["competitor country"], 'undef_country'])
        if (size >= 3):
            sum_list.append([competition, type_dict[competition][0]["competitor country"],
                             type_dict[competition][1]["competitor country"],
                             type_dict[competition][2]["competitor country"]])
    return sum_list#Return the final list


def calcCompetitionsResults(competitors_in_competitions):
    '''
    This function sorts and calculates the results in a competition database
    Arguments:
        competitors_in_competitions- The database.
    Return:
        returned_list- The results list.
    '''
    need_to_remove=[]#A list that will contain all of the cheaters items from the DB.
    for item1 in competitors_in_competitions:#Go through all of the items.
        cheater=False#Reset the cheater flag
        for item2 in competitors_in_competitions:#For each item go through all of the OTHER items
            if( (not(item1 ==item2)) and item1["competitor id"]==item2["competitor id"] and item1["competition name"]==item2["competition name"]):#Check if they have the same competition name and competitor id
                if(not (item2 in need_to_remove)):#If they do it means that a competitor is cheating, add the item to the list and set the cheater flag to True
                    need_to_remove.append(item2)
                cheater=True
        if(cheater):#If the cheater flag is on then this item should also be removed.
            if(not(item1 in need_to_remove)):
                need_to_remove.append(item1)
    for item in need_to_remove:#Remove all of the items that we marked to be removed.
        competitors_in_competitions.remove(item)

    timed_list = []#A list for the timed competitions
    untimed_list = []#A list for untimed competitions
    knockout_list = []#A list for knockout competitions
    competitions_set = set()
    for element in competitors_in_competitions:#Sort the elements into the list they fit into
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

    # Sort the lists by name and insert them into the sets, creating sets of the competitions.
    new_list1 = sorted(timed_list, key=getNameOfCompetition)
    timed_list = new_list1
    for competition in timed_list:
        timed_set.add(competition["competition name"])

    new_list2 = sorted(untimed_list, key=getNameOfCompetition)
    untimed_list = new_list2
    for competition in untimed_list:
        untimed_set.add(competition["competition name"])

    new_list3 = sorted(knockout_list, key=getNameOfCompetition)
    knockout_list = new_list3
    for competition in knockout_list:
        knockout_set.add(competition["competition name"])

    timed_dict = {}
    untimed_dict = {}
    knockout_dict = {}

    #For each dictionary, use the competitions as keys and a list of competitors as values
    for competition in timed_set:
        timed_dict[competition] = []
        for competitor in timed_list:
            if (competitor["competition name"] == competition):
                timed_dict[competition].append(competitor)

    for competition in untimed_set:
        untimed_dict[competition] = []
        for competitor in untimed_list:
            if (competitor["competition name"] == competition):
                untimed_dict[competition].append(competitor)

    for competition in knockout_set:
        knockout_dict[competition] = []
        for competitor in knockout_list:
            if (competitor["competition name"] == competition):
                knockout_dict[competition].append(competitor)

    #For each list, sort it by the results according to its type.
    for competition in timed_set:
        new_list4 = sorted(timed_dict[competition], key=getScoreOfCompetition)
        timed_dict[competition] = new_list4

    for competition in untimed_set:
        new_list5 = sorted(untimed_dict[competition], key=getScoreOfCompetition, reverse=True)
        untimed_dict[competition] = new_list5

    for competition in knockout_set:
        new_list6 = sorted(knockout_dict[competition], key=getScoreOfCompetition)
        knockout_dict[competition] = new_list6

    returned_list = (sumAllUp(timed_set, timed_dict)) + (sumAllUp(untimed_set, untimed_dict)) + (
    sumAllUp(knockout_set, knockout_dict))#Call the sumAllUp fucntion to sum up the results.

    return returned_list#Return the final list


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

    print(
        f'Competitor {competitor_id} from {competitor_country} participated in {competition_name} ({competition_type}) and scored {result}')


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

def partB(file_name='input.txt'):
    import Olympics
    competitions_results = partA(file_name, allow_prints=False)#Get the results from PART A
    olympic=Olympics.OlympicsCreate()#Create an olympics structure
    for item in competitions_results:#Insert the items from the results list to the olympics struct
        Olympics.OlympicsUpdateCompetitionResults(olympic,str(item[1]),str(item[2]),str(item[3]))
    Olympics.OlympicsWinningCountry(olympic)#Calculate the olympics results
    Olympics.OlympicsDestroy(olympic)#Delete the olympics structure
    # TODO Part B


if __name__ == "__main__":
    '''
    The main part of the script.
    __main__ is the name of the scope in which top-level code executes.

    To run only a single part, comment the line below which correspondes to the part you don't want to run.
    '''
    file_name = 'input.txt'

    partA(file_name)
    partB(file_name)


