# SM64DS Custom Object Database 

The goal of this project is to be a web-based database app for documenting custom objects added to Super Mario 64 DS by means of [ROM hacking](https://en.wikipedia.org/wiki/ROM_hacking). The user should be able to see a list of all objects in the database and search them by name and possibly other properties. The entry for each object should contain the name of the object, its object ID and actor ID, what ROM hack the object is from, and optionally a screenshot of the object in-game. Parameters for the object should also be documented if possible. 


The user should be able to see the whole database without logging in, but editing the database should only be possible while logged in with an account. Each account should naturally have a username and password. Each time a user makes an edit to an entry, the previous state of the entry should be saved to the database. This allows showing the change history for each entry, which makes destructive or malicious edits easy to revert.













