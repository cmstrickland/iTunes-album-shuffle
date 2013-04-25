# iTunes album shuffle by rating

Do you have an iTunes library on your mac that is many times bigger
than the capacity of your iPod, but you'd like to sync music to it,
and are old fashioned enough to want your music to sync in complete
albums? This utility may be for you.

This script builds a playlist in itunes that consists of entire albums
randomly across a few buckets by 'album' rating

It is intended for populating a low-capacity iPod or iPhone. Just set
up the device to always sync the target playlist, and then
periodically run shuffle to populate the playlist with albums from
your collection.

The shuffling recipe is hard coded

iTunes confusingly uses a 20 points to 1 star rating score internally

the default recipe assignment from main

    recipe = { '2 star' : ( 40, 5 ) , '3 star' : ( 60, 15 ), '4 star' : ( 80, 30 ) }

therefore means , pick 5 x 2 star albums, 15 x 3 star albums, and 30 4
star albums.

typically I also keep a smart playlist with all my 5 star albums on,
and sync all of these.

It would be a relatively straightforward matter to pass these
arguments from a config file, or on the command line, but I haven't
yet bothered, even though I've been using the script for several
years, without problem. I just edit the ratios in main if I want to
rebalance.

## requirements

The script manipulates iTunes via apple events, and it uses the lovely
[appscript pythonmodule](http://appscript.sourceforge.net/py-appscript/index.html) to
do so. Unfortunately appscript is deprecated and the author
discourages it's use for any new programs. At the time of writing,
appscript and this script work fine on the latest iTunes 11 and OS X
Mountain Lion.

Obviously, you also need iTunes, python, and probably an iPod to sync
to, although that isn't a strict dependency

The utility is hardcoded to use a playlist called 'Album Shuffle'. It
probably expects this to already be created.

## running the script

Create the playlist, edit the settings, and then run `./shuffle.py`.
The script will produce diagnostic messages as it goes. Playlist
creation is a little slow, but should run to completion in a couple
of seconds.