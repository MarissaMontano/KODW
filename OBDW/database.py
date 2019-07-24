#!/usr/bin/env Python3
import sqlite3 as DB
import numpy as np


class Database(object):

    def __init__(self, cxn_string=""):
        ''' Initialize the cxn and cursor'''
        self.cxn_string = cxn_string
        self.cxn = ''
        self.cursor = ''

    def openDatabase(self):
        ''' Method to create a connection to the database and set the cursor
                Input: None
                Output: None
        '''
        try:
            # Create a connection to the database
            self.cxn = DB.connect(self.cxn_string)
            # Create a cursor from the database connection
            self.cursor = self.cxn.cursor()

        except DB.Error as error:
            print("Error connecting to database. " + str(error))
            exit(225)

    def closeDatabase(self):
        ''' Method to close a connection to the database and cursor
                Input: None
                Output: True
        '''
        if self.cursor is not None:
            self.cxn.commit()
            self.cursor.close()
            # If the DB connection is valid, close it
        if self.cxn is not None:
            self.cxn.close()

        return True

    def commitWork(self):
        ''' Method to commit all work that has been done
                Input: None
                Output: True
        '''
        self.cxn.commit()
        return True
        

    # "CREATE TABLE IF NOT EXISTS UserInfo (userID INTEGER PRIMARY KEY, username text, password text);"
    def setupTables(self):
            ''' Method to create the tables needed for the recommender
                Input: None
                Output: True 
            '''
            # Write a SQL statement to create the table
            sql = "CREATE TABLE IF NOT EXISTS User (User_ID INTEGER PRIMARY KEY, User_Name text, User_Pass text);"
            # Execute and commit the sql
            self.cursor.execute(sql)

            sql = "CREATE TABLE IF NOT EXISTS User_Song (User_ID INTEGER, Song_ID INTEGER, Rating INTEGER);"
            self.cursor.execute(sql)
            
            #TODO: Make sure you have correct columns
            # dont neeed Duration INTEGER, Time_Signature INTEGER,
            #sql = "CREATE TABLE IF NOT EXISTS Song (Song_ID INTEGER PRIMARY KEY, Key INTEGER, Mode INTEGER, Acousticness INTEGER, Danceability INTEGER, Energy INTEGER, Instrumentalness INTEGER, Liveness INTEGER, Loudness INTEGER, Speechiness INTEGER, Valence INTEGER, Tempo INTEGER, Genre text, Popularity INTEGER, Year text, URL text);"
            #self.cursor.execute(sql)

            return self.commitWork()


    def isValidUser(self, username, password):
        ''' Method to check if the user trying to login is a valid user
                Input: username (string)
                       password (string)
                Output: True if valid, False otherwise
        '''
        self.cursor.execute("SELECT User_ID FROM User WHERE User_Name = ? AND User_Pass = ?;", (username, password, ))
        exist = self.cursor.fetchone()
        if exist:
                return True
        return False

    def createUser(self, username, password, password2):
        ''' Method to add a new user to the user table
                Input: username (string)
                       password (string)
                       password2 (string)
                Output: True if sucsessful, False otherwise
        '''
        # check if passwords match 
        # TODO: make more secure (need  caps, 8 characters, and symbol, etc...)
        if  password == password2:
            # check if it already exists first
            userExists = self.isValidUser(username, password)
            if userExists:
                return False
            else:
                # Execute and commit the insert query if it dosn't
                self.cursor.execute("INSERT INTO User (User_Name, User_Pass) VALUES(?, ?);",
                                    (username, password, ))
                return True
        else:
            return False


    def grabUserID(self, username, password):
        ''' Method to grab a user id for a specific user
                Input: username (string)
                       password (string)
                Output: UserID (string) or None if unsucsessful
        '''
        # check if it already exists first
        userExists = self.isValidUser(username, password)
        if userExists:
            # Execute query to retrieve the userID 
            self.cursor.execute(
                "SELECT User_ID FROM User WHERE User_Name= ? AND User_Pass = ? ;", (username, password, ))
            # Fetch the data from the cursor
            userID = self.cursor.fetchone()
            # Return the acronymID
            if userID:
                    return userID[0]
            # On an error None is returned
            else:
                return userID
        # Return None if password dosn't match username 
        else: 
            return None

    # delete current user with extra validate password
    def deleteUser(self, userID, password):
        ''' Method to delete the current user logged in
                Input: userID (string)
                       password (string)
                Output: True if sucsessful, False otherwise
        '''
        # check if password matches current user
        self.cursor.execute(
                "SELECT User_Name FROM User WHERE User_ID = ? AND User_Pass = ? ;", (userID, password, ))
        isValid = self.cursor.fetchone()
        if isValid:
            # Execute the delete command 
            self.cursor.execute("DELETE FROM User WHERE User_ID = ?;", (userID, ))
            return True
        else:
            return False

    def getUsersSongs(self, userID):
        ''' Method to get list of songs related to a specific user
                Input: userID (string)
                Output: 2D list of songs and ratings for specific user 
        '''
        self.cursor.execute(
                "SELECT Song_ID, Rating FROM User_Song WHERE User_ID = ? ;", (userID, ))
        songs = self.cursor.fetchone()
        songList = []
        while songs:
            songList.append([songs[0], songs[1]])
            songs = self.cursor.fetchone()
        return songList

    def getRandomSongs(self, userID, mood):
        ''' Method to random songs, filterd by mood for recomendation
                Input: userID (string), mood(string)
                Output: ND list of songs for recomendations for user 
        '''
        # get songs not in self.getUsersSongs() and filter by mood
        # Chill: low energy,  low tempo
        # Oldies: year filter
        # Hype: high energy, high dansability
        # Genere


    def cleanSongData(self, songList):
        ''' Method to format the song list data to use with the classifiers
                Input: songList (list)
                Output: clean list of song data
        '''
        
        for song in songList:
            self.cursor.execute(
                    "SELECT * FROM Song WHERE Song_ID = ? ;", (song, ))
            songs = self.cursor.fetchone()
            songList = []
            while songs:
                songList.append([songs[0], songs[1]])
                songs = self.cursor.fetchone()
            return songList 
            #np.append(npArray, [], axis=0)

