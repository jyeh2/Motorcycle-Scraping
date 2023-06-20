#I think I scraped it so many times wiki blocked me Ok no they didnt
from urllib.request import urlopen
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


def findtable(type,keyword,input):
    '''filter out unneeded tables'''
    table = ""
    for caption in input.find_all(type):
        if caption.get_text().strip() == keyword:
            table = caption.find_parent('table', {'class': 'wikitable'})
    return table


##############################################Data Processing Part################################################

def table2list(data):
    '''Convert Table to List'''
    out = []
    trs = data.find_all('tr')
    hrow = [td.get_text(strip=True) for td in trs[0].find_all('th')]
    if hrow:
        out.append(hrow)
        trs = trs[1:]
    for row in trs:
        out.append([td.get_text(strip=True) for td in row.find_all('td')])
    return out

def processing(input):
    '''trimout out empty list elements'''
    for i in input:
        while ('' in i):
            i.remove('')
    input = [list for list in input if (len(list)) > 0]
    return input

def infoconversion(input):
    '''Sorts out all of the data handling from html to lists and tuples, and dictionaries to be used in Graphing'''
    manufacturer = {}
    makes = []
    championships = []
    #Gets rid of all empty spaces in list
    for x in input:
        makes.append(x[1])
    makes = set(makes)
    #Finds all the championships eeach bike won, compiles them into tuples to be stored in a larger list
    year = ''
    count = 0
    for x in makes:
        for i in input:
            if x in i:
                count += int(i[2]) + int(i[3]) + int(i[4])
                year = year + " " + i[0]
        championships.append((x,count,year.strip().split()))
        count = 0
        year = ''
    #Finds all the unique companies/Compile them in a set
    Company =[]
    for model in makes:
        model = "".join(model.split()[0])
        Company.append(model)
    Company = set(Company)
    #Combines both into a dictionary
    for name in Company:
        manufacturer[name] = []
        for wins in championships:
            if "".join(wins[0].split()[0]) == name:
                manufacturer[name].append(wins)
    return manufacturer

##############################################Visual Part################################################
def modelgraphify(input,name):
    '''Takes care of the bar graphing(Visually Representing the Code)'''
    #Change size of figure
    figure(figsize=(31, 10))
    left = []
    for x in range(18):
        left.append(10*x)
    height = []
    for key in input:
        for element in input[key]:
            height.append(int(element[1]))
    tick_label = []
    for key in input:
        for element in input[key]:
            tick_label.append(element[0])
    plt.bar(left, height, tick_label=tick_label, width=5, color=['Black'])
    plt.xlabel('Model')
    plt.ylabel('Total Podiums')
    plt.title('Race Model Wins')
    #Save as "name
    plt.savefig(f"{name}", dpi=100)
    plt.show()

def manufacturergraphify(input,name):
    '''Displays total manufactuere podiums in bar graph'''
    figure(figsize=(20, 10))
    # Change size of font
    plt.rcParams.update({'font.size': 22})
    left = []
    for x in range(len(input.keys())):
        left.append(10 * x)
    height = []
    for key in input:
        score = 0
        for element in input[key]:
            score += int(element[1])
        height.append(int(score))

    tick_label = [key for key in input]
    plt.bar(left, height, tick_label=tick_label, width=2, color=['Black'])
    plt.xlabel('Manufacturer')
    plt.ylabel('Total Podiums')
    plt.title('Manufacturer Podiums')
    #allows program to be saved as "name"
    plt.savefig(f'{name}', dpi=100)
    plt.show()

def totalwinspie(input, name):
    '''Displays manufacturer wins in bar graph'''
    labels = [key for key in input]
    sizes = []
    count = 0
    plt.rcParams.update({'font.size': 15})
    for key in input:
        for i in input[key]:
            count += len(i[2])
        sizes.append(count)
        count = 0

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
             )
    plt.savefig(f'{name}', dpi=100)
    plt.show()
#######################################################################Actual Code########################################################

'''Get Data from wiki'''
url = urlopen('https://en.wikipedia.org/wiki/List_of_Superbike_World_champions')
html_bytes = url.read()
html = html_bytes.decode("utf-8")
soups = BeautifulSoup(html, 'html.parser')
table = 'Bruh it didn\'t work'#Test if it failed later

name = infoconversion(processing(table2list(findtable('caption','By season',soups))[1:]))

print(name)

modelgraphify(name, "model")
manufacturergraphify(name, "company")#ducati sux, suzuki for life
totalwinspie(name, "bestcompany")
