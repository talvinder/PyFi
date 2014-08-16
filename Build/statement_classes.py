from decimal import *
import csv
import os
import pickle
import datetime
import calendar

# TODO: complete specials creation

numDict = {}  # this helps us to keep track of how many of each transaction we have

account_list = [x.replace('.pkl', "") for x in os.listdir('core/accounts') if x.endswith('.pkl')]

specials_list = []

with open("special.csv", "r") as special_file:  # lets find what our specials are.
    special_types = csv.reader(special_file)
    for special in special_types:
        specials_list.append(special[0])


def date_sorter(date, order=0):
    """
    A function which takes a date in a specific format (year, month, day)
    returns the year month and day in seperate strings.

    An optional second parameter indicates how the date is originally organised.
     0 (default) = YYYY/MM/DD. 1 = DD/MM/YYYY. 2 = MM/DD/YYYY.

    The symbol separating the numbers is irrelevant,
    as long as there is a character (including whitespace) separating the values.

    (str, [int]) --->  tup

    >>> date_sorter("2014/06/12")
    ('12', '06', '2014')
    >>> date_sorter("12-06-2014", 1)
    ('12', '06', '2014')
    >>> date_sorter("06.12.2014", 2)
    ('12', '06', '2014')
    """
    if order == 0:
        day = datetime.date(int(date[:4]), int(date[5:7]), int(date[8:]))
    elif order == 1:
        day = datetime.date(int(date[6:]), int(date[3:5]), int(date[:2]))
    elif order == 2:
        day = datetime.date(int(date[6:]), int(date[:2]), int(date[3:5]))
    else:
        print(
            'Illegal parameter\n\nParameter 2 (order): {0} is an unspecified value.\n\n'.format(str(order))
            + 'Value must be between 0-2.\n\nNone returned.')
        day = None
    return day


def date_cleaner(date_list):
    """
    A function which cleans out the datelist to hold every day 
    between the two days regardless of whether it exists within the file.

    (lst) ---> lst

    >>>date_cleaner(["2014-03-24", "2014-03-20"])
    ["2014-03-20", "2014-03-21", "2014-03-22", "2014-03-23", "2014-03-24"]
    """
    # declare variables to hold the individual parts of the min and max dates
    # use these to find all the inbetween dates and enter the new ones into new_dates
    years = []
    months = []
    days = []
    new_dates = []

    # grab max date

    date = date_list[0]
    day = date.day
    month = date.month
    year = date.year

    days.append(day)
    months.append(month)
    years.append(year)

    # grab min date

    date = date_list[len(date_list) - 1]
    day = date.day
    month = date.month
    year = date.year

    days.append(day)
    months.append(month)
    years.append(year)

    # then we've shifted a year
    if years[0] - years[1] == 1:

        # for those months in the first year which are relevant
        for month in range(months[1], 13):

            # we are at the beginning
            if month == months[1]:

                # for this month find the first day, and then the max number of days in this month
                for day in range(days[1], calendar.monthrange(years[1], month)[1] + 1):
                    new_dates.append(datetime.date(years[1], month, day))

            # we are past the beginning
            else:
                # for each following month go from 1 to the limit
                for day in range(1, calendar.monthrange(years[1], month)[1] + 1):
                    new_dates.append(datetime.date(years[1], month, day))

        # for the next year
        for month in range(1, months[0] + 1):

            # if we've reached the last month
            if month == months[0]:
                # then go to the limit of that month
                for day in range(1, days[0] + 1):
                    new_dates.append(datetime.date(years[0], month, day))

            # otherwise
            else:
                # do the whole of each preceding month.
                for day in range(1, calendar.monthrange(years[0], month)[1] + 1):
                    new_dates.append(datetime.date(years[0], month, day))

    # if greater than a years difference
    elif (years[0] - years[1]) > 1:

        for year in range(years[1], years[0] + 1):

            # if the first year
            if year == years[1]:

                # for those months in the first year which are relevant
                for month in range(months[1], 13):

                    # we are at the beginning
                    if month == months[1]:
                        # for this month find the first day, and then the max number of days in this month
                        for day in range(days[1], calendar.monthrange(years[1], month)[1] + 1):
                            new_dates.append(datetime.date(years[1], month, day))

                    else:  # we are past the beginning
                        # for each following month go from 1 to the limit
                        for day in range(1, calendar.monthrange(years[1], month)[1] + 1):
                            new_dates.append(datetime.date(years[1], month, day))

            # for all preceding years but the latest
            elif year == years[0]:

                # for the next year
                for month in range(1, months[0] + 1):

                    # if we've reached the last month
                    if month == months[0]:
                        # then go to the limit of that month
                        for day in range(1, days[0] + 1):
                            new_dates.append(datetime.date(years[0], month, day))

                    # otherwise
                    else:
                        #do the whole of each preceding month.
                        for day in range(1, calendar.monthrange(years[0], month)[1] + 1):
                            new_dates.append(datetime.date(years[0], month, day))

            # for the final year
            else:

                # for the next year
                for month in range(1, 13):

                    # if we've reached the last month
                    if month == months[0]:
                        #then go to the limit of that month
                        for day in range(1, days[0] + 1):
                            new_dates.append(datetime.date(year, month, day))

                    #otherwise
                    else:
                        #do the whole of each preceding month.
                        for day in range(1, calendar.monthrange(year, month)[1] + 1):
                            new_dates.append(datetime.date(year, month, day))

    # all in the same year
    else:

        # all in the same month
        if months[1] == months[0]:
            for day in range(days[1], days[0] + 1):
                new_dates.append(datetime.date(years[1], month, day))

        # multiple months
        else:

            # from first to last month
            for month in range(months[1], months[0] + 1):

                # if first month
                if month == months[1]:
                    for day in range(days[1], calendar.monthrange(years[1], month)[1] + 1):
                        new_dates.append(datetime.date(years[1], month, day))

                #if last month
                elif month == months[0]:
                    for day in range(1, days[0] + 1):
                        new_dates.append(datetime.date(years[0], month, day))

                #all the months in-between
                else:
                    for day in range(1, calendar.monthrange(years[1], month)[1] + 1):
                        new_dates.append(datetime.date(years[1], month, day))

    '''
    origin=0

    for date in range(len(new_dates)):
        new_datel = new_dates[date].split("-")
        new_datet = ""

        for part in range(len(new_datel)):
            if len(new_datel[part])<2:
               new_datel[part] = "0"+new_datel[part]
            if part>0:
                new_datet = new_datet+ "-" + new_datel[part]
            else:
                new_datet = new_datel[part]

        new_dates[date] = new_datet'''

    return new_dates


def get_all(everything, date1='Beginning', date2='End', types=list(numDict.keys()), accounts=account_list):
    """
    Function runs through all of the pickled dates in the referential directory.

    A boolean decides whether or not we find every single date in the directory.

    Otherwise two optional parameters provide boundaries for what we take.

    (bool, str, str) ---> dict
    :rtype : object
    :param everything:
    :param date1:
    :param date2:
    :param types:
    :param accounts:
    """
    all_dates = {}
    if everything:
        for root, dirs, files in os.walk("ref"):
            for ref_file in files:
                if ref_file.endswith(".pkl"):
                    parts = root.split("/")
                    date = datetime.date(int(parts[1]), int(parts[2]), int(ref_file.rstrip(".pkl")))
                    if not date in all_dates.keys():
                        all_dates[date] = []
                    try:
                        with open(root + "/" + ref_file, "rb") as to_load:
                            all_dates[date] = pickle.load(to_load)
                    except AttributeError:
                        #print(root, ref_file)
                        pass
    else:
        date_list = date_cleaner([date_sorter(date2), date_sorter(date1)])
        for root, dirs, files in os.walk("ref"):
            for ref_file in files:
                if ref_file.endswith(".pkl"):
                    parts = root.split("/")
                    date = datetime.date(int(parts[1]), int(parts[2]), int(ref_file.rstrip(".pkl")))
                    if date in date_list:
                        if not date in all_dates.keys():
                            all_dates[date] = []
                        with open(root + "/" + ref_file, "rb") as to_load:
                            date_check = pickle.load(to_load)
                            trans = []
                            for trans in date_check.transactions:
                                if trans.account in accounts and trans.type in types:
                                    trans.append(trans)

                            all_dates[date] = FullDate(trans, date)

    return all_dates


class Transaction:
    """
    Class to store each individual transaction with additional metadata.
    This enhances duplication checking as there is a high level of detail.
    It also allows for in depth analysis based on multiple factors (time, account, amounts, type).

    amount = Decimal(transaction amount).
    name = transaction name from CSV/specials list.
    true_name = transaction name from CSV.
    account = account transaction is from.
    date = date transaction was made.

    __init__():
        initiate class object construction. Turns amount into a decimal number,
        cycles through the specials list to assign the name to a special name or keep it as standard.
        Assigns a type using the now assigned name and the keylist. assigns the rest of the details.

    compare(self, other_trans):
        Takes a second transaction and compare every attribute in the transaction to each attribute in this transaction.
        Returns True if all attributes are the same, otherwise returns False.
        Used to check for duplications in the data.
    """

    def __init__(self, amount, name, account_name, date):

        global keylist  # we'll need this
        global specials_list
        self.amount = Decimal(amount)  # obvious

        for special_type in specials_list:  # compare each one (is there a cleaner way to do this?)
            if special_type.upper() in name.upper():  # is this special in the name?
                self.name = str(special_type)  # if yes then change then assign the name to this special
                break  # and exit the for loop - can we make specials more specific? think of a way...
            else:  # otherwise it's not special - so it's in the keylist
                self.name = name  # name is name

        # just in case we hit a special. Might be useful to keep original name of this transaction for comparisons etc.
        self.true_name = name

        for key in keylist.keys():  # need to assign the type so compare to the keys
            if self.name == key:  # if it matches the key.
                self.type = keylist[key][0]  # then assign it to the associated type/
        # the rest is obvious
        self.account = account_name
        self.date = date
        self.day = date.day
        self.month = date.month
        self.year = date.year

    def compare(self, other_trans):

        result = True  # assume each of these transactions are different

        # lets get every attribute from the transaction
        for attrib in other_trans.__dict__.keys():
            # and check if they are not equal to this transactions.
            if other_trans.__getattribute__(attrib) != self.__getattribute__(attrib):
                result = False  # if they're equal then this is not a duplicate
                break  # and we can exit the loop.

        return result

    def __repr__(self):
        return "Transaction: " + str(self.amount) + " " + str(self.type)


class FullDate:
    """
    Class to store all the transactions on a particular date.
    Useful for day by day analysis.
    Also improves the system of writing out transactions to CSVs as well as the reference directory.

    __init__(self, lst, date):
        Initiates the object. Takes a list of transactions and the date the object represents.

        Runs through the given list and appends each transaction with the given date to transactions (an internal list).

        Once all relevant transactions have been appended it runs
        through each appended transactions to check for duplicates.

        Once duplicates have been deleted it creates 3 dictionaries containing all the types,
        accounts and names in the transactions and sums the total spent on that day
        - allowing an easy comparison between these 3 standards.
    """

    def __init__(self, lst, date):  # initiate the date class - bit complicated
        self.transactions = []
        for trans in lst:  # for each transaction in the list passed to the object
            if trans.date == date:  # the transactions must have the correct date specified when passed to the object.
                self.transactions.append(trans)  # if they do then add to the internal list
        self.date = date  # set the date
        self.month = date.month
        self.year = date.year
        true_list = self.transactions[:]  # copy the list of transactions to be cleaned
        duplicate = True  # flag to break a loop
        indexer = 0  # starting from the beginning

        while duplicate:  # while we have found duplicate transactions
            duplicate = False  # assume there are none

            # run through the list of transactions starting from where we last cycled back to the top of the while loop
            for trans2 in self.transactions[indexer:]:
                # worries to settle: we will start from the same transaction
                # so once one duplicate is cleaned out it will check for another
                # Thus will only move on when all have been cleaned.

                indexer = self.transactions.index(
                    trans2)  # reset the index to show that this is the latest transaction we checked for duplicates of
                testlist = self.transactions[:]  # copy list for deletions

                del testlist[testlist.index(trans2)]  # delete the transaction being compared against from the list

                for point in testlist:  # grab each transaction from the testlist to compare against

                    if point.compare(trans2):  # compare it to the current transaction
                        duplicate = True  # yep there was a duplicate

                        del true_list[true_list.index(point)]  # so delete it
                        break  # and leave the for loop.

                    else:
                        duplicate = False  # otherwise there are no duplicates left!

                if duplicate:
                    break  # we need to leave this outer for loop as well to cycle without incrementing
                    # as there may be another duplicate of this transaction.

            self.transactions = true_list  # re-assign the transaction list.

        self.type_totals = {}
        self.account_totals = {}
        self.name_totals = {}
        self.total = 0
        for trans3 in self.transactions:  # now to make some easy comparisons between dates.
            if not trans3.type in self.type_totals:  # adding stuff to the above dictionaries
                self.type_totals[trans3.type] = Decimal(0)
            if not trans3.name in self.name_totals:
                self.name_totals[trans3.name] = Decimal(0)
            if not trans3.account in self.account_totals:
                self.account_totals[trans3.account] = Decimal(0)

            # sum the transaction types, names and accounts to find the totals each spent/made on the day.
            self.type_totals[trans3.type] += trans3.amount

            self.name_totals[trans3.name] += trans3.amount

            self.account_totals[trans3.account] += trans3.amount
            self.total += trans3.amount

    def __repr__(self):
        return "Date object. Number of transactions: " + str(len(self.transactions)) + " Totalling: " + str(self.total)


class QifItem:
    def __init__(self, qif):
        self.order = {'num': None, 'payee': None, 'amountInSplit': None, 'memoInSplit': None, 'memo': None,
                      'date': None, 'category': None, 'amount': None, 'cleared': None, 'address': None,
                      'categoryInSplit': None}
        for part in qif:
            if len(part) > 0:
                if part[0] == "!":
                    pass
                elif part[0] == "D":
                    date = part[1:]
                    date_parts = date.split("/")
                    if len(date_parts[0]) == 1:
                        date_parts[0] = "0" + date_parts[0]
                    if len(date_parts[1]) == 1:
                        date_parts[1] = "0" + date_parts[1]
                    self.order["date"] = datetime.date(int(date_parts[2]), int(date_parts[1]), int(date_parts[0]))
                    self.textdate = date_parts[2] + "-" + date_parts[1] + "-" + date_parts[0]
                elif part[0] == "T":
                    self.order["amount"] = part[1:]
                elif part[0] == "C":
                    self.order["cleared"] = part[1:]
                elif part[0] == "P":
                    self.order["payee"] = part[1:]
                elif part[0] == "M":
                    self.order["memo"] = part[1:]
                elif part[0] == "A":
                    self.order["address"] = part[1:]
                elif part[0] == "L":
                    self.order["category"] = part[1:]
                elif part[0] == "S":
                    try:
                        self.order["categoryInSplit"].append(";" + part[1:])
                    except AttributeError:
                        self.order["categoryInSplit"] = [part[1:]]
                elif part[0] == "E":
                    try:
                        self.order["memoInSplit"].append(";" + part[1:])
                    except AttributeError:
                        self.order["memoInSplit"] = [part[1:]]
                elif part[0] == "$":
                    try:
                        self.order["amountInSplit"].append(";" + part[1:])
                    except AttributeError:
                        self.order["amountInSplit"] = [part[1:]]
                else:
                    pass

    def __repr__(self):
        keys = [thingy for thingy in self.order.keys() if thingy not in ["memoInSplit",
                                                                         "categoryInSplit",
                                                                         "amountInSplit"]]
        items = []
        for key in keys:
            items.append(self.order[key])

        keys = str(keys)
        keys.rstrip("]")
        keys.lstrip("[")
        items = str(items)
        items.rstrip("]")
        items.lstrip("[")
        return keys + "\n" + items


def make_qifs(filepath):
    qifs = []
    qif_count = 0
    with open(filepath, "r") as qif_file:
        readin = qif_file.read()
        readin.rstrip("\n")
        readin.rstrip("^")
        splitqifs = readin.split("^")
        if len(splitqifs[-1]) < 5:
            del splitqifs[-1]
        for qif in splitqifs:
            qif_count += 1
            qifs.append(QifItem(qif.split("\n")))

    return qifs


class TypeObject:
    def __init__(self, typ):
        self.type = typ
        self.total = 0
        self.summarise()

    def summarise(self):
        all_dates = get_all(1)
        for date in all_dates:
            if self.type in all_dates[date].type_totals:
                self.total = all_dates[date].type_totals[self.type]
            else:
                self.total = 0

    def __repr__(self):
        self.summarise()
        return "Total spent through this type: " + str(self.total)


class Account:
    def __init__(self, name, bank, savings=False):
        self.name = name
        self.bank = bank
        self.savings = savings


def create_account():
    global account_list

    name = input("What would you like to name this account? ")
    bank = input("And what bank holds this account? ")

    if bank.upper() not in ["HSBC", "HALIFAX"]:
        banks = True
        while banks:
            bank = input("That bank is currently unsupported by this programme, please enter either HSBC or Halifax ")
            if bank.upper() in ["HSBC", "HALIFAX"]:
                banks = False

    savings = input("Is this a savings account? ")
    new_account = Account(name, bank, savings)

    if new_account.name + ".pkl" in os.listdir("core/accounts"):
        namex = False
        while not namex:
            new_account.name = input("That name has already been taken, please pick a different name. ")
            if new_account.name + ".pkl" in os.listdir("core/accounts"):
                namex = True

    with open("core/accounts/" + new_account.name + ".pkl", "wb") as account_obj:
        pickle.dump(new_account, account_obj, protocol=pickle.HIGHEST_PROTOCOL)

    account_list.append(name)
    return name


while len(os.listdir("core/accounts")) == 0:
    print("There are currently no accounts on this system. Please make a new account to get started")
    create_account()


def create_type():
    global numDict

    typ = input("What do you want this type of transaction to be called? ")
    typ2 = typ
    if typ + ".pkl" in os.listdir("core/types"):
        typer = False
        while not typer:
            typ = typ2
            typ2 = input("That type already exists, do you want to create a different type or use the current type? ")
            if not typ2:
                return typ
            elif not (typ2 + ".pkl" in os.listdir("core/types")):
                typer = True
    typical = TypeObject(typ)
    with open("core/types/" + typ + ".pkl", "wb") as new_type:
        pickle.dump(typical, new_type, protocol=pickle.HIGHEST_PROTOCOL)
    numDict[typ] = 0
    return typ


while len(os.listdir("core/types")) == 0:
    print("There are currently no types of transaction on this system. Please create a type to get started")
    create_type()

for y in os.listdir("core/types"):
    if y.endswith(".pkl"):
        numDict[y.replace(".pkl", "")] = 0


def list_grabber():
    """
    This function opens a standardised file to read the types of transactions into a dictionary,
    storing the worksheet, column and row for each kind of transaction.

    (csv) --> dict
    """

    global numDict

    file1 = 'keys.csv'  # filepath

    keys1 = {}  # stores the keys

    with open(file1, 'r') as keys:
        reader = csv.reader(keys)  # set up the reading function

        for row in reader:  # start reading

            keys1[row[0]] = [row[1], int(row[2])]  # Create a key for the transaction with a list
            # holding the type of transaction and the column number.
            numDict[row[1]] += 1

    return keys1  # return key dictionary


def special_maker(new_type, list_of_keys, specials, payee):

    global numDict

    type_list = list(numDict.keys())

    special_key = input("What common phrase or word can be seen in all transactions within this group? ")

    if not special_key.upper() in new_type.upper():
        is_keyable = False
        while not is_keyable:
            special_key = input(
                special_key + " isn't in this transaction, " + new_type +
                ". Please pick a group of characters which will always be found within this " +
                "transaction and not in any other transaction. ")
            if special_key.upper() in payee.upper():
                is_keyable = True

    exclude = []
    include = []
    conflict = []
    key_count = 0
    for key in list_of_keys:

        if special_key in key:
            key_count += 1
            conflict.append(key)

    if key_count > 1:
        ignore_conflicts = input("There are " + str(key_count) +
                                 " transaction names that will be affected by this change." +
                                 " do you want to exclude any of them?")
    elif key_count > 0:
        ignore_conflicts = input("There is " + str(key_count) +
                                 " transaction name that will be affected by this change." +
                                 " do you want to exclude any of them?")
    else:
        ignore_conflicts = False

    if ignore_conflicts:
        for key in conflict:
            choice = input(
                "Key: " + key + " is affected by this change, do you want to exclude it from this special type? ")
            if choice:
                exclude.append(key)
            else:
                include.append(key)

    removal_count = 0

    for removal in include:
        del list_of_keys[removal]
        removal_count += 1

    special_type = input("And what type of transaction does this group fall into? ")

    if not special_type in type_list:
        vals = False
        while not vals:
            special_type = input(
                "That is not a valid type of transaction, please enter either {0}.".format(str(type_list)) +
                " Capitalisation is important: ")
            if special_type in type_list:
                vals = True

    numDict[special_type] += (1 - removal_count)
    list_of_keys[special_key] = [special_type, numDict[special_type] - 1]
    over = []
    under = []
    for key in list_of_keys:

        if list_of_keys[key][0] == special_type:

            if list_of_keys[key][1] > numDict[special_type]:
                over.append((key, list_of_keys[key][1]))

            elif list_of_keys[key][1] <= numDict[special_type]:
                under.append(list_of_keys[key][1])

    allowed = []

    for possible in range(0, numDict[special_type]):
        if not possible in under:
            allowed.append(possible)

    for paired in enumerate(over):
        list_of_keys[paired[1][0]][1] = allowed.pop(paired[0])

    specials.append(special_key)

    return list_of_keys, specials


# Grab the keylist. Needs to be done here otherwise undefined variable in functions
keylist = list_grabber()


def switch_column():
    global keylist, numDict

    key_change = input("Which key do you want to change the column of " + str(list(keylist.keys())) + "?")

    if not key_change in keylist.keys():
        good_key = False
        while not good_key:
            key_change = input("That key doesn't exist, please choose another from " + str(list(keylist.keys())) + "?")
            if key_change in keylist.keys():
                good_key = True

    current_col = keylist[key_change]

    new_col = input("Which column do you want " + key_change + " to be moved to?")

    if int(new_col) > numDict[keylist[key_change][0]]:
        big_number = False
        while not big_number:
            new_col = input("That number is too big, please pick a number between 0 and " +
                            str(numDict[keylist[key_change][1]]) + ".")
            if int(new_col) <= numDict[keylist[key_change][1]]:
                big_number = True

    for key in keylist:
        if keylist[key][0] == keylist[key_change][0] and keylist[key][1] == new_col:
            keylist[key][1] = current_col
            keylist[key_change][1] = new_col