#!/usr/bin/env python3

"""
Logs Analysis project in the Udacity Full Stack Web Developer Nanodegree.
Running this python file will yield the results of the following queries: 
1.  What are the most popular three articles of all time?
2.  Who are the most popular article authors of all time?
3.  On which days did more than 1% of requests lead to errors?
"""
import sys
from datetime import date

import psycopg2 


def print_info(database_name, queries):
    """
    Creates database connection.  Prints info based on view queries.
    """
    database, cursor = database_connect(database_name=database_name) 
    
    for idx, query in enumerate(queries):
        print_query(cursor=cursor, query=query)
        if idx + 1 != len(queries): # Add line separator if not last item
            print('\n') 
    
    database_disconnect(database=database, cursor=cursor)


def database_connect(database_name):
    """
    Connects to PSQL database, returns connection.  
    """
    try:
        database = psycopg2.connect(database=database_name)
        cursor = database.cursor()
        return database, cursor
    except psycopg2.error as err:
        print("Unable to connect to database.  Exiting...")
        print(err)
        sys.exit(1)


def database_disconnect(database, cursor):
    """
    Closes the connections to the database.
    """
    if not cursor.closed:
        cursor.close()
    if database.closed != 0:
        database.close()


def fetch_query(cursor, view):
    """
    Opens connection to database and queries it with pre-defined view.
    Returns all database rows from the view query.
    """
    cursor.execute("SELECT * from " + view)
    posts = cursor.fetchall()
    return posts


def get_formatted_date(date_to_format):
    """
    Returns formatted date along with appropriate month suffix.
    """
    #Referenced following website for solution:
    #https://stackoverflow.com/questions/739241/date-ordinal-output
    day = date_to_format.day
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = 'th'
    else:
        suffix = ['st', 'nd', 'rd'][day % 10 - 1]
    
    return date_to_format.strftime('%B %d' + suffix + ', %Y')


def print_query(cursor, query):
    """
    Prints the results of the query.
    """
    print(query.headline())
    
    results = fetch_query(cursor=cursor, view=query.view)
    for result in results:
        title = result[0]
        value = result[1]
        
        if isinstance(title, date):
            title = get_formatted_date(title)
        
        print("%s -- %s %s" % (title, value, query.suffix))


class Query:
    """
    Creates a query object.
    """
    
    def __init__(self, question, view, suffix):
        self.question = question
        self.view = view
        self.suffix = suffix
    
    def headline(self):
        """
        Generates a rather ostentatious headline with a lot of asteriks.
        The purpose is to make the information stand out, but also to display
        my manipulation of the code as a learning tool for myself.
        """
        capitalized = self.question.upper()
        text = "** %s **" % capitalized
        top_and_bottom = "*" * len(text)
        headline = "%s\n%s\n%s" % (top_and_bottom, text, top_and_bottom)
        return headline
    

if __name__ == '__main__':
    DBNAME = "newsdata"
    QUERIES = [
        Query(
            question="What are the most popular three articles of all time?",
            view="pop_articles",
            suffix="views"
        ),
        Query(
            question="Prints the most popular article authors of all time",
            view="pop_authors",
            suffix="views"                    
        ),
        Query(
            question="On which days did more than 1% of requests " +
            "lead to errors?",
            view="one_percent_errors",
            suffix="% errors"                    
        )]

    print_info(database_name=DBNAME, queries=QUERIES)










































































#Lardass