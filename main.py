import json
import datetime 
# TODO: Refactor to make it more generalised to get any website from browsing history
# TODO: README.md
# TODO: A function to filter out browser history by any available keys


def main(): pass


def get_browsing_data(file_name):
    """
    Parses the json file to return in format understandable by python

    :param file_name: name of the file with the browsing data
    :return: the parsed json format
    """
    with open(file_name, 'r') as browser_data_file:
        data = json.load(browser_data_file)

    return data['Browser History']


def get_sites_by_date(history, year, day, month):
    """
    Goes through the parsed json filtering out any links not matching the date parameters

    :param history: the parsed json return by get_browsing_data
    :param year: specification of the year to search for (int)
    :param day: specification of the day to search for (int)
    :param month: specification of the month to search for (int)
    :return: A list containing all the sites matching the date parameters
    """
    sites = []

    for i in range(len(history)):
        time_usec = history[i]['time_usec']
        timestamp = (time_usec / 1000000)

        date_obj = datetime.datetime.fromtimestamp(timestamp)
        date_obj_year = date_obj.year
        date_obj_month = date_obj.month
        date_obj_day = date_obj.day

        if year and day and month:
            if year == date_obj_year and day == date_obj_day and month == date_obj_month:
                sites.append(history[i])
        elif year and month:
            if year == date_obj_year and month == date_obj_month:
                sites.append(history[i])
        elif year and day:
            if year == date_obj_year and day == date_obj_day:
                sites.append(history[i])
        elif day and month:
            if day == date_obj_day and month == date_obj_month:
                sites.append(history[i])
        elif day:
            if day == date_obj_day:
                sites.append(history[i])
        elif year:
            if year == date_obj_year:
                sites.append(history[i])
        elif month:
            if month == date_obj_month:
                sites.append(history[i])
        else:
            sites.append(history[i])

    return sites


def get_sites_by_url(history, url, starts_with=True):
    """
    Goes through the parsed json filtering out any links not matching the url parameter

    :param starts_with: boolean whether the url specified be found at the start of the link (True) or anywhere in the link (False)
    :param history: the parsed json return by get_browsing_data
    :param url: the url being searched for in the history
    :return: A list containing all the sites matching the url parameter
    """
    sites = []

    for i in range(len(history)):
        link = history[i]['url']
        if starts_with and link.startswith(url):
            sites.append(history[i])
        elif (not starts_with) and (url in link):
            sites.append(history[i])

    return sites


def get_sites_by_date_and_url(history, url, year, day, month):
    """
    Goes through the parsed json filtering out any links not matching the date and url parameters

    :param month: specification of the month to search for (int)
    :param day: specification of the day to search for (int)
    :param year: specification of the year to search for (int)
    :param history: the parsed json return by get_browsing_data
    :param url: the url being searched for in the history
    :return: A list containing all the sites matching the url and date parameters
    """

    date_filtered_history = get_sites_by_date(history=history, year=year, day=day, month=month)
    url_filtered_history = get_sites_by_url(history=date_filtered_history, url=url)
    return url_filtered_history

    # for i in range(len(history)):
    #     time_usec = history[i]['time_usec']
    #     timestamp = (time_usec/1000000)
    #
    #     date_obj = datetime.datetime.fromtimestamp(timestamp)
    #     year = date_obj.year
    #     month = date_obj.month
    #     day = date_obj.day
    #     if year == 2020 and month == 3 and day == 10:
    #         url = history[i]['url']
    #         if url.startswith(url):
    #             test_string = f"{url}\n"
    #             file_data.append(test_string)


def get_filtered_sites(history, filter_type, filter_value):
    """
    Getting sites that match the filter_type and filter_value
    :param filter_value: the value to filter against
    :param filter_type: the key in the json data that is being targeted (supported once shown in available_filter_types)
    :param history: the parsed json return by get_browsing_data or the get_sites methods
    :return: a list of sites that match the filter_value
    """
    sites = []

    available_filter_types = ("favicon_url", "page_transition", "title", "client_id", "time_usec")
    if filter_type in available_filter_types:
        for i in range(len(history)):
            if history[i][filter_type] == filter_value:
                sites.append(history[i])
    else:
        return print("Filter specified is not supported")

    return sites


def write_to_file(file_data, file_name='output'):
    """
    It writes the file_data to a specified file
    :param file_data: a list of data to be written to the specified file
    :param file_name: name of file to export data to excluding extension as txt is assumed
    :return: nothing
    """
    with open(f"{file_name}.txt", 'w') as file:
        file.writelines(file_data)

test = 'https://www.youtube.com/watch?v='

