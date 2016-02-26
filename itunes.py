#!/usr/bin/python -tt

import xml.etree.ElementTree as ET
import sqlite3

def main():

  #create sqlite connection
  #create DATABSE
  conn = sqlite3.connect('itunes.sqlite')
  c = conn.cursor()

  c.executescript('''
      DROP TABLE IF EXISTS Artist;
      DROP TABLE IF EXISTS Album;
      DROP TABLE IF EXISTS Track;''')


  #create TABLE - Track
  c.execute('''CREATE TABLE IF NOT EXISTS "Track"
  ("title" TEXT UNIQUE, "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "genre_id" INTEGER,
  "album_id" INTEGER, "len" INTEGER, "rating" INTEGER, "count" INTEGER)''')

  #create TABLE - Artist
  c.execute('''CREATE TABLE IF NOT EXISTS "Artist" ("name" TEXT UNIQUE, "id" INTEGER
  NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE)''')

  #create TABLE - Album
  c.execute('''CREATE TABLE IF NOT EXISTS "Album" ("title" TEXT UNIQUE, "id" INTEGER
  NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "artist_id" INTEGER)''')

  #create TABLE - Genre
  c.execute('''CREATE TABLE IF NOT EXISTS "Genre" ("name" TEXT UNIQUE, "ID" INTEGER NOT
  NULL PRIMARY KEY AUTOINCREMENT UNIQUE)''')

  #open XML file
  xml = raw_input("Enter XML file:")
  if len(xml) < 1: xml = "Library.xml"
  fxml = open(xml)

  #read the XML data
  tree = ET.parse(fxml)
  dic = tree.findall('dict/dict/dict')

  def lookup(d, key):
    found = False
    for child in d:
      if found : return child.text
      if child.tag=="key" and child.text == key :
        found = True
    return None

  for entry in dic:
    track_title = lookup(entry, 'Name')
    artist_name = lookup(entry, 'Artist')
    album_title = lookup(entry, 'Album')
    genre_name = lookup(entry, 'Genre')
    count = lookup(entry, 'Play Count')
    rating = lookup(entry, 'Rating')
    length = lookup(entry, 'Total Time')

    if track_title is None or artist_name is None or album_title is None or genre_name is None: 
      continue

    print "Track = ",track_title
    print "Album = ",album_title
    print "Artist = ",artist_name
    print "Genre = ",genre_name

    #INSERT SQL tables. first Artist and Genre, then album and the last track
    c.execute("INSERT OR IGNORE INTO Artist (name) VALUES (?)",(artist_name,))
    c.execute("INSERT OR IGNORE INTO Genre (name) VALUES (?)",(genre_name,))
    #to update Album table we need to know artist_id from Artist table
    artist_id = c.execute("SELECT id FROM Artist WHERE name=?",(artist_name,))
    c.execute("INSERT OR IGNORE INTO Album (title,artist_id) VALUES (?,?)",(album_title,artist_id.fetchone()[0]))
    #to update Track table we need to know album_id from Album and genre_id from Genre tables
    album_id = c.execute("SELECT id FROM Album WHERE title=?",(album_title,))
    album_id = album_id.fetchone()[0]
    genre_id = c.execute("SELECT id FROM Genre WHERE name=?",(genre_name,))
    genre_id = genre_id.fetchone()[0]

    c.execute("INSERT OR IGNORE INTO Track (title,album_id,genre_id,len,rating,count) VALUES (?,?,?,?,?,?)",(track_title,album_id,genre_id,length,rating,count))






  #conn.commit()
  conn.commit()

  conn.close()


if __name__ == '__main__': 
  main()


