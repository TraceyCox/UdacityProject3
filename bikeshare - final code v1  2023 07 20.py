import time
import calendar as cal
from datetime import datetime, timedelta as td
import pandas as pd
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt


CITY_DATA = { 'chicago': 'chicago.csv',
             'chi': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'nyc': 'new_york_city.csv',
              'washington': 'washington.csv',
               'dc': 'washington.csv' }

my_path = 'c:/Users/cox16/OneDrive - Bertelsmann SE & Co. KGaA/Reference File/Tools for Analysis/Python & SQL/Udacity - Python for Data Science/Python/Project'


# define our functions, get_filters, load_data and time_statistics

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\n\nHello! Let\'s explore some US bikeshare data!')


    # 1. Test all features for the initial function 'get_filters()
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # Use the dictionary keys to create a list for possible city input
    cities = list(CITY_DATA.keys())

    # Set city value 
    city = ''
    

    # While loop to handle data that is not as expected for city
    while city == '':
        city = input(str("Enter a city: Chicago, New York City, or Washington: ")).lower()
        
        if city not in cities:
                print("Answer is not in the list of options. Please enter a city: Chicago, New York City, or Washington: \n")
                city = ''
        else:
                city = city.lower()


    # TO DO: get user input for month (all, january, february, ... , june)
    # Set possible month values as list from calendar and add the option for all
    months = [cal.month_name[i] for i in range(1,7)]
    months.append('All')
   
    month = ''


    # While loop to handle data that is not as expected for months
    while month == '':
        month = input("Enter a month from January to June, or All: ").title()
        if month not in months:
            print("Answer is not in the list of options. Please enter ALL, or a month from January to June inclusive: \n")
            month = ''
        else:
            month = month.title()


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    # Set possible weekday values as list from calendar and add the option for all
    days = [cal.day_name[i] for i in range(0,7)]
    days.append('All')

    day = ''


    # While loop to handle data that is not as expected for days
    while day == '':
        day = input("Enter a day of the week, or All: ").title()
        if day not in days:
            print("Answer is not in the list of options. Please enter All, or a day from Monday to Sunday inclusive: \n")
            day = ''
        else:
                day = day.title()

    print("\nFetching data for {}, {}, {}:".format(city.title(), month, day))

    print('-'*40)
    return city, month, day


# 2. Test all features for the second function 'load_data'

def load_data(city, month, day):
    """
        Loads data for the specified city and filters by month and day if applicable.

            Args:
            (str) city - name of the city to analyze
            (str) month - name of the month to filter by, or "all" to apply no month filter
            (str) day - name of the day of week to filter by, or "all" to apply no day filter
        Returns:
            df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(my_path + '/' + CITY_DATA[city], parse_dates = True)
    
    # convert the Start and End dates to datetime format
    df[['Start Time', 'End Time']] = df[['Start Time', 'End Time']].apply(pd.to_datetime)
    
    # extract month, day of week and hour from the Start Time as new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()
    df['Start Hour'] = df['Start Time'].dt.hour
    
    return df


# 3. time statistics

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    # filter by month, if applicable
    month_counts = df['Month'].value_counts().to_dict()
    
    if len(month_counts) > 1:
        #print(month_counts)
        top_month = max(month_counts, key = month_counts.get)
        top_month = cal.month_name[top_month]
        print("The most popular month for travel is {}".format(top_month))
    

    # TO DO: display the most common day of week
    day_counts = df['Day of Week'].value_counts().to_dict()

    if len(day_counts) > 1:
        top_day = max(day_counts, key = day_counts.get)
        print("The most popular day for travel is {}".format(top_day))

    # TO DO: display the most common start hour
    hour_counts = df['Start Hour'].value_counts().to_dict()
    #print(hour_counts)
    top_hour = max(hour_counts, key = hour_counts.get)
    top_hour = pd.to_datetime(top_hour, format = '%H')

    print("The most common start hour is {}:00".format(top_hour.hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# 4. Station stats
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_stations = df['Start Station'].value_counts().to_dict()
    top_start_station, numS = max(start_stations, key = start_stations.get), max(start_stations.values())
    
    print("The most frequently used starting station is {}, which was used {} times".format(top_start_station, numS))

    # TO DO: display most commonly used end station
    end_stations = df['End Station'].value_counts().to_dict()
    top_end_station, numE = max(end_stations, key = end_stations.get), max(end_stations.values())
    
    print("The most frequent journeys end at station {}, which was used {} times".format(top_end_station, numE))

    # TO DO: display most frequent combination of start station and end station trip
    # Use groupby to find the most common combination of stations and the number of occurrences, save to a dictionary
    station_comb = df.groupby(['Start Station', 'End Station'])['Start Station'].count().to_dict()
    
    # save the most common occurrence as a tuple and a value
    top_comb, numC = max(station_comb, key = station_comb.get), max(station_comb.values())
    
    # To check value type, use print(type(top_comb) is tuple), then split the tuple back to start and end variables in order to print these in a sensible way
    start1, fin1 = top_comb
    print("The most popular journey occurred {} times, it began at {}, and ended at {}".format(numC, start1, fin1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# 5. Trip_durations
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display max total travel time (total travel time doesnt make a lot of sense...)
    max_travel_time = td(seconds = max(df['Trip Duration']))
    
    i = df.loc[df['Trip Duration'] == max(df['Trip Duration'])]
    
    #print("The longest journey (hire) time in h:m:s was {} with the following information: \n{}\n".format(max_travel_time, i.iloc[:,1:].to_string(index = False)))
    print("The longest journey (hire) time in h:m:s was {} with the following information: \n\n{}\n".format(max_travel_time, tabulate(i.iloc[:,1:], headers = i.columns[1:], showindex = False)))
    # TO DO: display mean travel time
    ave_travel_time = df['Trip Duration'].mean()
    ave_travel_time = td(seconds = ave_travel_time)
    ave_travel_time = ave_travel_time - td(microseconds=ave_travel_time.microseconds)

    print("The average hire time in h:m:s was {}".format(ave_travel_time))
    plt.plot(df['Trip Duration'])
    plt.show(); plt.show()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# 6. user_stats
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    mem_types = df['User Type'].value_counts().apply(lambda x: "{:,}".format(x))
    print("The breakdown of user types is: \n{}\n".format(mem_types))

    # TO DO: Display counts of gender
    # Not all datasets have gender, need to amend reporting accordingly
    while True:
        try:
            genders = df['Gender'].value_counts().apply(lambda x: "{:,}".format(x))

            # we need to add an 'unknown' quantity too as we seem only to have gener data for subscribers
            unknowns = max(df.count()) - df['Gender'].count()
            print("The gender split of the users is: \n{}\n".format(genders))
            print("There were also {} users for which we hold no gender data\n".format(f"{unknowns:,d}"))
            break
        except KeyError:
            print("There is no gender information in this dataset")
        finally:
             break
    
    # TO DO: Display earliest, most recent, and most common year of birth
    # Not all datasets have Birth Year, need to amend reporting accordingly
    # Correct Birth Year format to int, casting astype(int, errors = 'ignore') does not work. Try convert_dtypes()

    while True:
        try:
            df['Birth Year'] = df['Birth Year'].convert_dtypes(int)
            yobmin = df['Birth Year'].min()
            yobmax = df['Birth Year'].max()
            yobmedian = df['Birth Year'].median()
            print("The oldest user was born in {}, the youngest was born in {}. The most common year of birth is {}".format(yobmin, yobmax, yobmedian.astype(int)))
            break
        except KeyError:
            print("There is no birth year information in this dataset")
        finally:
             break
             #print(df.head())
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# 7. Raw data
# def Chunker function

def chunker(dataframe, start, chunk_size):
    for line in range(start, dataframe.shape[0], chunk_size):
        end = min(start + chunk_size, dataframe.shape[0])
        print("\n",tabulate(dataframe.iloc[start:end, 1:], headers = dataframe.columns[1:], numalign = "decimal", stralign = "left", missingval = "", showindex = False))
        print("\n")
        break

def chunk_print(df):
    raw_output = ''
    start = 0
    chunk_size = 5
    while True:
        raw_output =  input(str("Would you like to see 5 rows of the raw data? "))
        if raw_output.lower() not in ('y', 'yes'):
            break  
        else:
            chunker(df, start, 5)
            start += chunk_size



# main function
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)


        # filter by month, if applicable
        if month != 'All':
          month = datetime.strptime(month, '%B').month
          df = df[df['Month'] == month]

        # filter by day, if applicable
        if day != 'All':
          #print(day)
          df = df[df['Day of Week'] == day]        

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        chunk_print(df)

        #print(df.head())

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() not in ('yes', 'y'):
            print("\n\n")
            break


if __name__ == "__main__":
	main()