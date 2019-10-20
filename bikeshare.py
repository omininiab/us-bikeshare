import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June']

WEEK_DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    city, month, day = '', 'All', 'All'

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    
    while city not in CITY_DATA:
        input_msg = '\nWhich of these cities would you like to explore?:\n{}\n'
        options = [*CITY_DATA]
        city = input(input_msg.format(options)).lower()
        
    filter_month = input("\nWould you like to filter the data by month? (Y/N): ").title()
    if filter_month == 'Y':
        month = ''

    # get user input for month (january, february, ... , june)
    while month not in MONTHS and month != "All":
        input_msg = '\nWhich month would you like to explore?:\n{}\n'
        month = input(input_msg.format(MONTHS)).title()
        
    filter_day = input("\nWould you like to filter the data by day of the week? (Y/N): ").title()
    if filter_day == 'Y':
        day = ''

    # get user input for day of week (monday, tuesday, ... sunday)
    while day not in WEEK_DAYS and day != "All":
        input_msg = '\nWhich day of the week would you like to explore?:\n{}\n'
        day = input(input_msg.format(WEEK_DAYS)).title()


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

    # convert the Start and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['month'] = df['month'].map(lambda a: MONTHS[int(a-1)])
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'All':
        # filter by month to create the new dataframe
        df = df[df['month'] == month.title()]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df
    
def preview_data(df,city, month, day, i = 1):
    """Repeatedly asks user if they'd like to preview the raw data and acts accordingly"""

    message = "Would you like to preview a sample of the data (max: 25 lines)? (Y/N)"
    preview_data = input(message).title()

    while preview_data == 'Y' and i <= 20:
        i += 5
        print("\nSample data from {}\nMonth: {}; Day of week: {}\n".format(city.title(),month,day))
        print(df.iloc[:i])
        preview_data = input("See more? (Y/N)").title()

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month (check if month filter is applied)
    if df['month'].nunique() > 1:
        print("The most common month is: {}".format(df['month'].mode().values[0]))


    # display the most common day of week (check if day of week filter is applied)
    if df['day_of_week'].nunique() > 1:
        print("The most common day of the week is: {}".format(df['day_of_week'].mode().values[0]))


    # display the most common start hour
    print("The most common start hour is: {}".format(df['hour'].mode().values[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most common start station is: {}".format(df['Start Station'].mode().values[0]))


    # display most commonly used end station
    print("The most common end station is: {}".format(df['End Station'].mode().values[0]))



    # display most frequent combination of start station and end station trip
    df['Start and End Stn'] = df['Start Station'] + " // " + df['End Station']
    print("The most common combination of start // stop stations is: {}".format(df['Start and End Stn'].mode().values[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    # change Trip Duration column to float and replace NaNs with zeros
    df['Trip Duration'] = df['Trip Duration'].fillna(0).map(lambda a: float(a))
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time (days, hh:mm:ss): {}".format(timedelta(seconds = int(total_travel_time))))


    # display mean travel time
    mean_travel_time = df['Trip Duration'][df['Trip Duration'] > 0].mean()
    print("Average travel time (days, hh:mm:ss): {}".format(timedelta(seconds = int(mean_travel_time))))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Here is a breakdown of the types of bike riders:\n{}\n\n".format(df['User Type'].value_counts()))

    # Display counts of gender
    if 'Gender' in df:
        print("Here is a breakdown of the genders of bike riders:\n{}\n\n".format(df['Gender'].value_counts()))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        # change Birth Year column to int and replace NaNs with zeros
        df['Birth Year'] = df['Birth Year'].fillna(0).map(lambda a: int(float(a)))
        
        print("The earliest birth year of bike riders is: {}".format(df['Birth Year'][df['Birth Year'] > 0].min()))
        
        print("The most recent birth year of bike riders is: {}".format(df['Birth Year'][df['Birth Year'] > 0].max()))
        
        print("The most common birth year of bike riders is: {}".format(df['Birth Year'][df['Birth Year'] > 0].mode().values[0]))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        preview_data(df, city, month, day, 1)

        start_time = time.time()

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        print('-'*40)
        print("\nTotal time: %s seconds." % (time.time() - start_time))

        restart = input('\nWould you like to restart? (Y/N).\n').title()
        if restart != 'Y':
            break

if __name__ == "__main__":
	main()