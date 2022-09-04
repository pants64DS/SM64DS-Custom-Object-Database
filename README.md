# SM64DS Custom Object Database

The goal of this project was to create a web-based database app for documenting custom objects added to Super Mario 64 DS by means of [ROM hacking](https://en.wikipedia.org/wiki/ROM_hacking). Among other things, the app supports viewing a list of objects, searching them and sorting them. The user may also click on an objects name to open a page with the full description of the object. This page may also contain a screenshot of the object in game, and there's an option to edit each property of the object.

On the front page, the user can see a table of all objects in the database. The table can be sorted by different properties such as the name of the object, the name of the creator or the name of the ROM hack the object is from. There is also a search feature that matches information stored in the table with a string provided by the user. The user can control whether the search is case-sensitive or not, and whether regular expression is used. Any cells in the table with matching strings are highlighted, and objects with no matches are filtered out.

The user can see the whole database without logging in, but editing the database is only possible when logged in with an account. However, since anyone can make an account, there isn't much protecting the database from malicious actions. In the initial plan, each time a user makes an edit to an entry, the previous state of the entry was supposed to be saved to the database. This would have allowed showing the change history of each entry, which would have made destructive or malicious edits easier to revert. Unfortunately, this feature never came to be due to time constraints.

The app can be tested [here](https://sm64ds-custom-object-database.herokuapp.com) on Heroku.
