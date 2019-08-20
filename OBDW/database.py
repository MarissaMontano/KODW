#!/usr/bin/env Python3
import sqlite3 as DB
import numpy as np
import pandas as pd
import ast


class Database(object):

    def __init__(self, cxn_string="", checkThread=''):
        ''' Initialize the cxn and cursor'''
        self.cxn_string = cxn_string
        self.cxn = ''
        self.cursor = ''
        self.checkThread = checkThread

    def openDatabase(self):
        ''' Method to create a connection to the database and set the cursor

                Input:  None
                Output: None
        '''
        try:
            # Create a connection to the database
            self.cxn = DB.connect(
                self.cxn_string, check_same_thread=bool(self.checkThread))
            # Create a cursor from the database connection
            self.cursor = self.cxn.cursor()

        except DB.Error as error:
            #print("Error connecting to database. " + str(error))
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

    def setupTables(self):
        ''' Method to create the tables needed for the recommender

            Input: None
            Output: True
        '''
        # Create User tabel (hold user pass and genres)
        sql = "CREATE TABLE IF NOT EXISTS User (User_ID INTEGER PRIMARY KEY, User_Name text, User_Pass text, Genres text);"
        self.cursor.execute(sql)
        # Create the user song table (holds what song the user rates, and what the ratings is)
        sql = "CREATE TABLE IF NOT EXISTS User_Song (User_ID INTEGER, Song_ID text, Rating INTEGER);"
        self.cursor.execute(sql)
        # Creates the songs table and what the songs data is like tempo etc..
        sql = "CREATE TABLE IF NOT EXISTS Song (Song_ID text PRIMARY KEY, Key INTEGER, Mode INTEGER, Acousticness INTEGER, Danceability INTEGER, Energy INTEGER, Instrumentalness INTEGER, Liveness INTEGER, Loudness INTEGER, Speechiness INTEGER, Valence INTEGER, Tempo INTEGER, Name text, Artist text, URL text);"
        self.cursor.execute(sql)

        # commit and return true
        return self.commitWork()

    def createUser(self, username, password, password2):
        ''' Method to add a new user to the user table

                Input: username (string)
                       password (string)
                       password2 (string)
                Output: uid (int) if sucsessful, None otherwise
        '''
        # check if passwords match
        # TODO: make more secure (need  caps, 8 characters, and symbol, etc...)
        if password == password2:
            # check if it already exists first by trying to grab their ID
            userExists = self.getUserID(username, password)
            if userExists is not None:
                return False
            else:
                # Execute and commit the insert query if they don't exist
                self.cursor.execute("INSERT INTO User (User_Name, User_Pass, Genres) VALUES(?, ?, ?);",
                                    (username, password, '[]'))
                self.commitWork()
                
                # Need one bad rating so classifier dosn't break
                uid = self.getUserID(username, password)
                # Bad hack... need lowest rating in data set for classifier to work, so default to hate justin bieber's Baby 
                self.setUserSongData([[uid, '6epn3r7S14KUqlReYr77hA', 1]])
                
                return uid
        else:
            return None

    def getUserID(self, username, password):
        ''' Method to get a user id for a specific user

                Input:  username (string)
                        password (string)
                Output: UserID (int) or None if unsucsessful
        '''
        # Execute query to retrieve the userID
        self.cursor.execute(
            "SELECT User_ID FROM User WHERE User_Name= ? AND User_Pass = ? ;", (username, password, ))
        userID = self.cursor.fetchone()
        # Return the acronymID if it exists
        if userID:
            return userID[0]
        # On an error None is returned
        else:
            return userID

    def deleteUser(self, userID, password):
        ''' Method to delete the current user logged in, both in the User table and the User_Song table

                Input:  userID (int)
                        password (string)
                Output: None if sucsessful, uid (int) otherwise
        '''
        # check if password matches current user
        self.cursor.execute(
            "SELECT User_Name FROM User WHERE User_ID = ? AND User_Pass = ? ;", (userID, password, ))
        isValid = self.cursor.fetchone()
        if isValid:
            # Execute the delete command
            self.cursor.execute(
                "DELETE FROM User WHERE User_ID = ?;", (userID, ))
            self.cursor.execute(
                "DELETE FROM User_Song WHERE User_ID = ?;", (userID, ))
            self.commitWork()
            return None
        else:
            return userID

    def getUsersSongData(self, userID):
        ''' Method to get list of songs and their ratings related to a specific user

                Input:  userID (int)
                Output: cleaned ND array of songs data (pandas dataframe), or None if there is no data
        '''
        # get song list and ratings
        self.cursor.execute(
            "SELECT Song_ID, Rating FROM User_Song WHERE User_ID = ? ;", (userID, ))
        songs = self.cursor.fetchone()
        songList = []
        # If they exist add them to a list
        while songs:
            songList.append([songs[0], songs[1]])
            songs = self.cursor.fetchone()

        # clean up basic user song data to be used in classifier (in specific pandas form)
        cleanData = {'Key': [], 'Mode': [], 'Acousticness': [], 'Danceability': [], 'Energy': [], 'Instrumentalness': [
            ], 'Liveness': [], 'Loudness': [], 'Speechiness': [], 'Valence': [], 'Tempo': [], 'Rating': []}
        for song in songList:
            self.cursor.execute(
                "SELECT * FROM Song WHERE Song_ID = ? ;", (song[0], ))
            data = self.cursor.fetchone()
            if data:
                # Key, Mode, Acousticness, Danceability, Energy, Instrumentalness, Liveness, Loudness, Speechiness, Valence, Tempo, Rating
                cleanData['Key'].append(data[1])
                cleanData['Mode'].append(data[2])
                cleanData['Acousticness'].append(data[3])
                cleanData['Danceability'].append(data[4])
                cleanData['Energy'].append(data[5])
                cleanData['Instrumentalness'].append(data[6])
                cleanData['Liveness'].append(data[7])
                cleanData['Loudness'].append(data[8])
                cleanData['Speechiness'].append(data[9])
                cleanData['Valence'].append(data[10])
                cleanData['Tempo'].append(data[11])
                cleanData['Rating'].append(song[1])

        if len(cleanData['Key']) == 0:
            return None

        clean = pd.DataFrame(cleanData)
        return clean

    def setUserSongData(self, ratedList):
        ''' Method to set a list of data in the table User_Song (uid, sid, and rating of songs)

                Input: ratedList (3D list)
                Output: None
        '''
        for uid, sid, rate in ratedList:
            # Check if its alredy rated
            self.cursor.execute(
                "SELECT Rating from User_Song WHERE User_ID = ? AND Song_ID = ?;", (uid, sid,))
            alreadyThere = self.cursor.fetchone()

            # update rating if its already there
            if alreadyThere:
                self.cursor.execute(
                    '''UPDATE User_Song SET Rating = ? WHERE User_ID = ? AND Song_ID = ?''', (rate, uid, sid))

             # insert into database if it hasn't been rated
            else:
                self.cursor.execute("INSERT INTO User_Song (User_ID, Song_ID, Rating) VALUES(?, ?, ?);",
                                    (uid, sid, rate))
        self.commitWork()

    def getUserGenres(self, userID):
        ''' Method to get the Users genres given their ID

                Input: userID (int)
                Output: genres (ND list of strings)
        '''
        self.cursor.execute(
            "SELECT Genres FROM User WHERE User_ID = ? ;", (userID, ))
        genres = self.cursor.fetchone()
        # return the literal of the generes because data is stored as "[blah, blah, ..]"
        return (ast.literal_eval(genres[0]))

    def getUserTracks(self, userID):
        ''' Method to get the Users 5 stared tracks given their ID
            TODO: use it for delete it.
                Input: userID (int)
                Output: trackIds (ND list of strings)
        '''
        trackIds = []
        # Get the song ids of all 5 stared songs
        self.cursor.execute(
            "SELECT Song_ID FROM User_Song WHERE User_ID = ? AND Rating >= 4;", (userID, ))
        track = self.cursor.fetchone()
        while track:
            trackIds.append(track[0])
            track = self.cursor.fetchone()
        return trackIds

                
    def updateUserGenres(self, userID, newGenreList):
        ''' Method to update the users Genres with a list that was passed in 

                Input:  userID (int)
                        newGenreList (list of strings)
                Output: True
        '''
        # Get genres from past selections
        oldGenreList = self.getUserGenres(userID)
        
        # Delete unselected genres
        for genre in oldGenreList:
            if genre not in newGenreList:
                oldGenreList.remove(genre)
        # Add newly selected ones 
        for genre in newGenreList:
            if genre not in oldGenreList:
                oldGenreList.append(genre)
        
                
        # update the genre list with new genres not already in the list
        print (oldGenreList)
        self.cursor.execute(
            '''UPDATE User SET Genres = ? WHERE User_ID = ? ''', (str(oldGenreList), userID))
        return True

    def songExists(self, song_id):
        ''' Method to check if the song is already in the database

                Input: songID (string)
                Output: True if it exists, False otherwise
        '''
        self.cursor.execute(
            "SELECT Song_ID FROM Song WHERE Song_ID = ?;", (song_id, ))
        exist = self.cursor.fetchone()
        if exist:
            return True
        return False

    def updateSongTable(self, musicData):
        ''' This method updates the Song table with new music 

            Input:  Music data (ND array) (array holds tempo, key, mode, etc..)
            Output: True
        '''
        for data in musicData:
            songExist = self.songExists(data[0])
            if songExist:
                pass
            else:
                # Execute and commit the insert query if it dosn't already exist
                self.cursor.execute("INSERT INTO Song (Song_ID, Key, Mode, Acousticness, Danceability, Energy, Instrumentalness, Liveness, Loudness, Speechiness, Valence, Tempo, Name, Artist, URL) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                                    (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], data[14]))
        return True



    def getRandomPredict(self, songList):
        ''' This method to randomly grab and format the songs in the database to be used in teh predect part of the classifier

            Input:  Songlist (3D list of id, name, and artist)
            Output: cleanData (pandas dataframe that holds tempo, key, mode, etc..)
        '''
         # clean up basic user song data to be used in classifier (in specific pandas form)
        cleanData = {'ID': [], 'Key':[], 'Mode':[], 'Acousticness':[], 'Danceability':[], 'Energy':[], 'Instrumentalness':[], 'Liveness':[], 'Loudness':[], 'Speechiness':[], 'Valence':[], 'Tempo':[]}
        for song in songList:
            self.cursor.execute(
                "SELECT * FROM Song WHERE Song_ID = ? ;", (song[0], ))
            data = self.cursor.fetchone()
            if data:
                # ID, Key, Mode, Acousticness, Danceability, Energy, Instrumentalness, Liveness, Loudness, Speechiness, Valence, Tempo
                cleanData['ID'].append(data[0])
                cleanData['Key'].append(data[1])
                cleanData['Mode'].append(data[2])
                cleanData['Acousticness'].append(data[3])
                cleanData['Danceability'].append(data[4])
                cleanData['Energy'].append(data[5])
                cleanData['Instrumentalness'].append(data[6])
                cleanData['Liveness'].append(data[7])
                cleanData['Loudness'].append(data[8])
                cleanData['Speechiness'].append(data[9])
                cleanData['Valence'].append(data[10])
                cleanData['Tempo'].append(data[11])
                
        clean = pd.DataFrame(cleanData)
        return clean


    def formatRecommendations(self, songIds, userId):
        ''' Method to format the recomendations to be useful for the web side table display

            Input:  songIds (list)
                    userId (int)
            Output: clean list of song data (ND array)
        '''
        cleanData = []
        for idx, song in enumerate(songIds):
            self.cursor.execute(
                "SELECT Name, Artist, URL FROM Song WHERE Song_ID = ?;", (song, ))
            data = self.cursor.fetchone()
            # if song data exists
            if data:
                self.cursor.execute(
                "SELECT Rating FROM User_Song WHERE User_ID = ? AND Song_ID = ?;", (userId, song, ))
                rating = self.cursor.fetchone()
                # if the song has previously been rated by that user
                if rating:
                    # Song id, name, artist, url, r#, pre_rating
                    cleanData.append(
                        [song, data[0], data[1], data[2], "r"+str(idx), rating[0]])
                else:
                    # Song id, name, artist, url, r#, pre_rating = 0
                    cleanData.append(
                        [song, data[0], data[1], data[2], "r"+str(idx), 0])
        return cleanData
