#!/usr/bin/env python

import random
from appscript import *

class Album(object):
    "model an album from iTunes, with a collection of tracks and a rating"
    def __init__(self,name,rating=None):
        self.tracks = []
        self.set_rating(rating)
        self.set_name(name) 

    def append_track(self,track):
        self.tracks.append(track)

    def set_rating(self,rating=None):
        self.rating = rating

    def get_rating(self):
        return self.rating

    def set_name(self,name):
        self.name = name

    def get_name(self):
        return self.name
    

class iTunes(object):
    """A wrapper around iTunes via appscript
       supply an argument of a playlist name to restrict master album pool to only albums
       from that playlist"""
    def __init__(self,root_list=None):
        self.app = app('iTunes')
        self.lib = self.app.sources[its.kind == k.library]
        #    seems like python requires the attribute to be defined before we can 
        #    just assign dictionary keys to it
        self.playlists = {}
        self.albums = {}
        # library playlists is a list with a single item, a list of all playlists
        for playlist in self.lib.playlists()[0] :
            self.playlists[playlist.name()] = playlist # remember all the playlists 
        # if we were initialised with a playlist name, use this as the source of albums 
        if root_list is None:
            # otherwise use the whole library - library tracks is a 
            #  list containing a single item, a list of all tracks
            root_list = self.lib.tracks()[0]
        else: 
            root_list = self.playlists[root_list].file_tracks()
        for trk in root_list:
            album_name = trk.album()
            if not self.albums.has_key(album_name):
                self.albums[album_name] = Album(album_name,trk.album_rating())
            self.albums[album_name].append_track( trk )

    def list_albums(self):
        """returns a list of album names"""
        the_list = self.albums.keys()
        the_list.sort()
        return the_list

    def by_rating(self,rating):
        """returns a list of album objects that match the specified rating
           itunes represents album ratings as percents, *=20 **=40 ***=60 ****=80 *****=100"""
        the_list = [ album for album in self.albums.keys() \
                         if self.albums[album].get_rating() == rating ]
        return the_list

    def n_random_albums(self,count=1,rating=0):
        """returns a randomized list of count albums of the specified rating"""
        the_list = self.by_rating(rating)
        random.shuffle(the_list)
        if count == '*':
            count = len(the_list)
        return the_list[:count]

    def albums_to_tracklist(self,albums):
        "convert a list of album names to a list of tracks"
        tracks = []
        for album in albums:
            tracks = tracks + self.albums[album].tracks
        return tracks

    def clear_playlist(self,playlist):
        "delete all tracks from the specified playlist"
        playlist.tracks.delete()

    def add_tracks_to_playlist(self,playlist,tracks):
        "add the list of tracks to the specified playlist"
        for track in tracks:
            self.app.duplicate(track,to=playlist)
    

def main():
    root = 'All music albums'
    target = 'Album shuffle'
    
    print "parsing iTunes - %s" % root
    i = iTunes(root)
    print "done"
    target = i.playlists[target]

    i.clear_playlist(target)

    recipe = { '2 star' : ( 40, 5 ) , '3 star' : ( 60, 15 ), '4 star' : ( 80, 30 ) }
    for label,ratio in recipe.iteritems():
        rating,count = ratio
        print "**** selecting %d %s albums by shuffling" % (count, label)
        albums = i.n_random_albums(count,rating)
        for a in albums :
            print "        %s" % a
        tracks = i.albums_to_tracklist(albums)
        i.add_tracks_to_playlist(target,tracks)

        
        
    # now we have a playlist with all our candidate tracks

if __name__ == "__main__":
    main()
