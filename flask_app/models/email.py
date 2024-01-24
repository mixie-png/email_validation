# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

import re	# the regex module
# create a regular expression object that we'll use later
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# model the class after the email table from our database
class Email:
    DB = "email_validation_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.email_address = data['email_address']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Now we use class methods to query our database
    # READ
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM emails;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('email_validation_schema').query_db(query)
        # Create an empty list to append our instances of emails
        emails = []
        # Iterate over the db results and create instances of emails with cls.
        for email in results:
            emails.append( cls(email) )
        return emails

    # READ
    # show one record
    @classmethod
    def show_one(cls, id):
        query = """SELECT * FROM emails WHERE id = %(id)s;"""
        result = connectToMySQL(cls.DB).query_db(query, {"id" : id})

        # Check if result is not empty before accessing the first element
        if result:
            one_email = cls(result[0])
            return one_email
        else:
            return None  # or handle the case where the email with the given id is not found

    # CREATE
    @classmethod
    def add(cls, data):
        query = """
            INSERT INTO emails (email_address)
    	    VALUES (%(email_address)s);
        """
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result

    # DELETE
    @classmethod
    def delete(cls, email_id):
        query = """
            DELETE FROM emails
            WHERE id = %(id)s;
        """
        result = connectToMySQL(cls.DB).query_db(query, {"id" : email_id})
        return result

    #VALIDATE
    @staticmethod
    def validate_email( email ):
        is_valid = True
        # test whether a field matches the pattern
        # ['email_address'] is the name in form input
        if not EMAIL_REGEX.match( email['email_address'] ):
            flash("Email cannot be blank!", 'email')
            is_valid = False
        return is_valid
