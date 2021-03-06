import uuid
from flask import Flask
from datetime import date
from initializer import mysql
import json
import traceback


def present_date():
    """
    Utility method to return present date as a string in the format "YYYY-MM-DD"  
    """
    return str(date.today())


def otp():
    """
    Utility method to return a unique permutation of characters as a string
    """
    return uuid.uuid1()


def executeSQL(sqlQuery, fetchOne=True, *params):
    """
    Helper method to run any SQL query
    returns the result as a list
    """

    cur = mysql.connection.cursor()
    try:
        print("db:" + sqlQuery%params)
        cur.execute(sqlQuery % params)
        mysql.connection.commit()
    except Exception as e:
        ex = e
        print("db: failed")
        traceback_str = ''.join(traceback.format_tb(e.__traceback__))
        print(traceback_str)
        print(ex)
        mysql.connection.rollback()
        return "Failure"

    result=None
    try:
        if fetchOne:
            result=list(cur.fetchone())
        else:
            result=list(cur.fetchall())
        return result
    except:
        pass
    finally:
        cur.close()


def svalidate(token):
    """
    Validatation method to validate the user's login via the token
    returns uid, username and email as a list
    """
    return executeSQL('select sid,Semail from students where spin="%s"',True,str(token))


def tvalidate(token):
    """
    Validatation method to validate the user's login via the token
    returns uid, username and email as a list
    """
    return executeSQL('select tid,temail from teachers where tpin="%s"',True,str(token))


def rvalidate(token):
    """
    Validatation method to validate the user's login via the token
    returns uid, username and email as a list
    """
    return executeSQL('select rid,remail, rposition from resolvers where rpin="%s"',True,str(token))

