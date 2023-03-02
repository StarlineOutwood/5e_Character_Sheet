# 5e_Character_Sheet
Character sheet based on 5th edition Dungeons and Dragons rules.

INSTALLATION
1. Clone this reprositio to your computer.
2. Create .env -file and write into it:

DATABASE_URL=<local adress>
SECRET_KEY=<secret key (hex16)>

3. Activate virtual environment and install requirements with these commands:

$ python3 -m venv venv
  
$ source venv/bin/activate
  
$ pip install -r ./requirements.txt

4. Add schemas of the database:

$ psql < Schema.sql
                   
$ psql < Base.sql

5. Launch the app:

$ flask run

.....

Submission 2

At the moment you are able to remove a character, and see the characters own page. I am currently expanding the character sheet to actually include all the stats, and it is nearly ready. after that, you will have a functioning character sheet. Next i will need to do signing in and out, then it should be functionally ready. After that i can add some nice things here and there, but then at least the basics will be covered

Submission 1

At the moment you can add a character with a name, race, class and level to a database. I am working on removing a character and adding a database with all the information about already excisting races and classes. I had a lot of technical problems to get started, so I am not exactly at where I would want to be, but im sure it will get better from here.

Plan

When this project is ready, you should be able to:

1. Create a character
2. Level up a character
3. Remove a character
4. Create a party
5. Remove a party
6. View your characters stats ( as a player ) or view your party's stats ( as a DM )
7. Add/remove objects, weapons and money
8. Keep track of max HP, current HP and temorary HP
9. Keep track of your spells and spellslots
10. Cast spells
11. Keep track of long- and shortrests
12. Roll for an ability, attack or a saving throw ( rolls d20 and adds your modifiers )
13. Keep track of conditions the character is under

Basically it should be able to do all the actions that require a good memory for fules (like remembering spell stats), so you as a player can focuse on the main thing: tricking old hags with magical blueberry cupcakes and terrifying everyone with your undead rat familiar.

(If I have time, it would be cool to have like a messaging system that the DM can for example attack a player with a monster and that attack shows up on the player's screen, saying a message like "Thow wizard is shooting a fireball at you, roll for a dexterity saving throw" or "Barbarian is hitting you, does 16 hit?" and then you can lick a button and it will do the check for you, and the same would be another way around when a player attacks an enemy. While playing there could be a board that has all the party memebrs and you can view them based on your status ( DM sees all, player sees their own, but can choose to have actions on other player's character) and when you are in combat, the DM can add new "players" there, as friendly NPC's or enemies.
