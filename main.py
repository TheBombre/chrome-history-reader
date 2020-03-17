import json
import datetime 

available_filter_types = ("favicon_url", "page_transition", "title", "url", "client_id", "time_usec")


def main(file_name, year, day, month, url):
    """

    :param file_name: name of the file with the browsing data
    :param year: specification of the year to search for (int)
    :param day: specification of the day to search for (int)
    :param month: specification of the month to search for (int)
    :param url: the url being searched for in the history
    :return: nothing
    """
    browser_history = get_browsing_data(file_name)
    sites = get_sites_by_date_and_url(history=browser_history, url=url,
                                      year=year, month=month, day=day)
    write_to_file(history=sites, filter_type="url")


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


def get_filtered_sites(history, filter_type, filter_value):
    """
    Getting sites that match the filter_type and filter_value
    :param filter_value: the value to filter against
    :param filter_type: the key in the json data that is being targeted (supported once shown in available_filter_types)
    :param history: the parsed json return by get_browsing_data or the get_sites methods
    :return: a list of sites that match the filter_value
    """
    sites = []

    if filter_type in available_filter_types:
        for i in range(len(history)):
            if history[i][filter_type] == filter_value:
                sites.append(history[i])
    else:
        raise Exception("Filter specified is not supported")

    return sites


def write_to_file(history, filter_type, file_name='output'):
    """
    It writes the all elements in history or a certain key of the elements to a specified file
    :param filter_type: the key in the json data that is being targeted (supported once shown in available_filter_types)
    :param history: a list of data to be written to the specified file
    :param file_name: name of file to export data to excluding extension as txt is assumed
    :return: nothing
    """
    if not filter_type:
        with open(f"{file_name}.txt", 'w') as file:
            file.writelines(history)
    elif filter_type in available_filter_types:
        with open(f"{file_name}.txt", 'w') as file:
            for x in range(len(history)):
                file.write(f"{history[x][filter_type]}\n")
    else:
        raise Exception("Filter specified is not supported")


if __name__ == '__main__':
    main('browser-history.json', year=2020, month=3, day=10, url='https://www.youtube.com/watch?v=')

