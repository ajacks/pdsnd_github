import time
import pandas as pd
import numpy as np
import csv

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def convert_12hr(time):
    """
    Converts hours from 24hr to 12hr measure with AM or PM added to end
    
    Returns:
        (str) hours - inputed time converted to 12hr clock equivalent with AM or PM
    """       
    if time > 12:
        hours = time - 12
        hours = "{} PM".format(hours)
    elif time == 12:
        hours = "{} PM".format(time)
    elif time == 0:
        hours = time + 12
        hours = "{} AM".format(hours)
    else:
        hours = "{} AM".format(time)
        
    return hours

def convert(seconds):
    """ 
    Code found on: https://www.geeksforgeeks.org/python-program-to-convert-seconds-into-hours-minutes-and-seconds/
    
    Converts time represented in seconds into hours, minutes, and remaining seconds.
    
    Returns:
        (int) hours - total number of full hours
        (int) minutes - total number of full minutes after hours have been taken out
        (int) seconds - total number of remaining seconds after hours and minutes have been calculated
    """
    seconds = seconds % (24 * 3600)
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return int(hours), int(minutes), int(seconds)
        

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    cities = ['washington', 'new york city', 'chicago']
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    options = ['month', 'day', 'both', 'none']
    
    while True:
        city = str(input('Would you like to see information about Chicago, New York City, or Washington? ')).lower()
        if city not in cities:
            print('This is not a valid city input')
        else:
            break

    while True:
        month_day_filter = str(input('Would you like to filter the results by month, day, both, or neither? If neither please type "none":\n')).lower()
        if month_day_filter not in options:
            print('"{}" is not a valid selection. Please type month, day, both, or none\n'.format(month_day_filter))
        else:
            break
    month = 'all'
    day = 'all'
    if month_day_filter == 'month' or month_day_filter == 'both':
        while True:
            month = str(input('Choose a month from January to June:\n')).lower()
            if month not in months:
                print('"{}" is not a valid selection. Please type the full month name you would like to filter by or type "all" to remove the filter.')
            else:
                break
        
    if month_day_filter == 'day' or month_day_filter == 'both':
        while True:
            day = str(input('Choose a day of the week (e.g. "Sunday"):\n')).lower()
            if day not in days:
                print('"{}" is not a valid selection. Please type the full day name you would like to filter by or type "all" to remove the filter.')
            else:
                break

    print('-'*40)
    return city, month, day


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time']) 

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # Filters by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Filters by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
               
    return df
    

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
        
    # Display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    common_month = months[df['month'].mode()[0]-1]
    print('The most common month was:', common_month.title())

    # Display the most common day of week
    common_week = df['day_of_week'].mode()[0]
    print('The most common day of the week was:', common_week)
    
    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
        
    common_hour = convert_12hr(df['hour'].mode()[0])
    
    print('The most common start hour was:', common_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    start_station = df.groupby('Start Station').size()
    print('The most used start station was:', start_station.idxmax())
    

    # Display most commonly used end station
    end_station = df.groupby('End Station').size()
    print('The most used end station was:', end_station.idxmax())

    # Display most frequent combination of start station and end station trip
    combo_station = df.groupby(['Start Station','End Station']).size().idxmax()
    
    print('The most frequent route was: {} to {}'.format(combo_station[0], combo_station[1]))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    ## Trip Duration column in csv is listed in seconds
    total_travel = df['Trip Duration'].sum()
    
    hours, minutes, seconds = convert(total_travel)
    
    print('The total travel time of selection was {} hours, {} minutes, and {} seconds'.format(hours, minutes, seconds))

    # Display mean travel time
    mean_travel = df['Trip Duration'].mean()
    
    hours, minutes, seconds = convert(mean_travel)
    
    print('The mean travel time of selection was approximately {} hours, {} minutes, and {} seconds'.format(hours, minutes, seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    df['User Type'] = df['User Type'].fillna('Undefined')
    user_types = df.groupby('User Type').size()
    print('The number of each user type is as follows:\n', user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        df['Gender'] = df['Gender'].fillna('Undefined')
        gender_count = df.groupby('Gender').size()
        print('The number of users by gender for the selection are as follows:\n', gender_count)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth = int(df['Birth Year'].min())
        most_recent_birth = int(df['Birth Year'].max())
        most_common_birth = int(df['Birth Year'].mode()[0])
        
        print('The oldest user\'s birth year was:', earliest_birth)
        print('The youngest user\'s birth year was:', most_recent_birth)
        print('The most common birth year was:', most_common_birth)
        
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(city):
    """ Asks user if they would like to see raw data. 
    Shows 5 rows at a time and prompts user if they would like to see the next 5 rows before continuing. """
    
    with open(CITY_DATA[city]) as f:
        reader = csv.reader(f)
        more_data = str(input('Would you like to see 5 rows of raw data?\n'))
        # Prompts user if they would like to see first 5 rows and reprompts after each 5 rows. Stops if end of file is reached.
        while more_data == 'yes':
            try:
                if more_data == 'yes':
                    for x in range(5):
                        print(next(reader))
                    more_data = str(input('Would you like 5 more rows of data?\n'))
                else:
                    break
            except StopIteration:
                print('You have reached the end of the data set.')
                break
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
