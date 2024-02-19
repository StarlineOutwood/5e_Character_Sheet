from app import app
import users
import characters
import default_data
from flask import Flask
from flask import redirect, render_template, request, session
from sqlalchemy.sql import text

@app.route("/")
def index():
    if session.get("id"):
        return redirect("/party")
    return render_template("frontPage.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/createUser",methods=["POST"])
def createUser():
    username = request.form["username"]
    password = request.form["password"]
    users.add_user(username, password)
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    tulos = users.log_in(username, password)
    if tulos:
        session["username"] = username
        session["id"] = tulos[0]
        return redirect("/party")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/party")
def party():
    id = session["id"]
    all = characters.get_characters(id)
    return render_template("frontPage.html", hahmot = all)

@app.route("/newC")
def newC1():
    classes = default_data.get_classes()
    races = default_data.get_races()
    return render_template("newC.html", classes = classes, races = races)

@app.route("/modifyAbilities/<int:character_id>")
def modifyAbilities(character_id):
    current_stats = characters.ability_stats(character_id)
    info = characters.info(character_id)
    race = info[3]
    increases = default_data.race(race)
    if current_stats:
        return render_template("modifyAbilities.html", score_increase = increases[3], stats = current_stats, character_id = character_id)
    else:
        start = [("Wisdom", 10), ("Charisma", 10), ("Intelligence", 10), ("Dexterity", 10), ("Constitution", 10), ("Strenght", 10)]
        return render_template("modifyAbilities.html", score_increase = increases[3], stats = start, character_id = character_id)

@app.route("/modifySkills/<int:character_id>", methods=["POST"])
def modifySkills(character_id):
    skills = [("Acrobatics", "Dexterity", [1, 4, 6]),
                 ("Sleight of hand", "Dexterity", [1, 4, 6]),
                 ("Stealth", "Dexterity", [1, 4, 6]),
                 ("Insight", "Wisdom", [1, 4, 6]),
                 ("Animal handling", "Wisdom", [1, 4, 6]),
                 ("Medicine", "Wisdom", [1, 4, 6]),
                 ("Perception", "Wisdom", [1, 4, 6]),
                 ("Survival", "Wisdom", [1, 4, 6]),
                 ("Arcana", "Intelligence", [1, 4, 6]),
                 ("History", "Intelligence", [1, 4, 6]),
                 ("Investigation", "Intelligence", [1, 4, 6]),
                 ("Nature", "Intelligence", [1, 4, 6]),
                 ("Religion", "Intelligence", [1, 4, 6]),
                 ("Athletics", "Strenght", [1, 4, 6]),
                 ("Deception", "Charisma", [1, 4, 6]),
                 ("Intimidation", "Charisma", [1, 4, 6]),
                 ("Performance", "Charisma", [1, 4, 6]),
                 ("Persuation", "Charisma", [1, 4, 6]),]
    wis = int(request.form["Wisdom"])
    cha = int(request.form["Charisma"])
    intelligence = int(request.form["Intelligence"])
    dex = int(request.form["Dexterity"])
    con = int(request.form["Constitution"])
    str = int(request.form["Strenght"])
    ability_scores = [wis, cha, intelligence, dex, con, str]
    abilities = ['Wisdom', 'Charisma', 'Intelligence', 'Dexterity', 'Constitution', 'Strenght']
    n = characters.has_scores(character_id)
    if n[0]>0:
        characters.update_abilities(ability_scores, abilities, character_id)
    else:
        characters.create_abilities(ability_scores, abilities, character_id, skills)
    profs = characters.is_prof(character_id, 1)
    non_profs = characters.is_prof(character_id, 0)
    number = characters.skill_increase(character_id)
    return render_template("modifySkills.html", profs = profs, non_profs= non_profs, character_id = character_id, n = number[0])

@app.route("/finishModifyingStats/<int:character_id>", methods=["POST"])
def finishModifyingStats(character_id):
    profs = request.form.getlist("skill")
    characters.update_profs(character_id, profs)
    back = "/hahmo/" + str(character_id)
    return redirect(back)

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    race = request.form["race"]
    character_class = request.form["class"]
    level = request.form["level"]
    user_id = session["id"]
    characters.add_character(name, race, character_class, level, user_id)
    return redirect ("/party")

@app.route("/removeC")
def removeC():
    user_id = session["id"]
    all = characters.get_characters(user_id)
    return render_template("removeC.html", names = all)

@app.route("/remove", methods=["POST"])
def remove():
    ids = request.form.getlist("poistettava")
    characters.remove(ids)
    return redirect ("/party")

@app.route("/hahmo/<int:character_id>")
def character(character_id):
    info = characters.info(character_id)
    name = info[2]
    race_id = info[3]
    character_class_id = info[4]
    level = info[5]
    hp = info[7]
    max_hp = info[6]
    temp_hp = info[9]
    hit_dice = info[8]
    message = ""
    if (hp < 1):
        message = "Your character is rolling death savingthrows."
    character_class = default_data.get_class(character_class_id)
    race = default_data.race(race_id)
    abilities = characters.ability_stats(character_id)
    skills = characters.skill_stats(character_id)
    return render_template("hahmo.html", name = name, race = race[1], character_class= character_class[1], level = level, character_id = character_id, 
                           abilities = abilities, skills = skills, hp = hp, max_hp = max_hp, temp_hp = temp_hp, hit_dice = hit_dice, message=message)

@app.route("/changeHP/<int:character_id>", methods=["POST"])
def changeHP(character_id):
    hp_stats = characters.hp_stats(character_id)
    change = int(request.form["change"])
    if (change < 0 and change*(-1) <= hp_stats[2]): #if damage but smaller than temp hp
        characters.damage(character_id, hp_stats[0], hp_stats[2]+change)
    else:
        if (change < 0 and change*(-1) > hp_stats[2]): #if damage and greater than temp hp
            change += hp_stats[2]
            if (hp_stats[0] + change <= 0): #if goes to dst
                characters.damage(character_id, 0, 0)
            else: #if just damage
                characters.damage(character_id, hp_stats[0]+change, 0)
        else: #if healing
            if (hp_stats[0] + change >= hp_stats[1]):
                characters.healing(character_id, hp_stats[1])
            else:
                characters.healing(character_id, hp_stats[0] + change)
    back = "/hahmo/"+str(character_id)
    return redirect(back)

@app.route("/addTempHP/<int:character_id>", methods=["POST"])
def addTempHP(character_id):
    change = request.form["change"]
    characters.add_temp_hp(character_id, change)
    back = "/hahmo/"+str(character_id)
    return redirect(back)

@app.route("/modifyCharacter/<int:character_id>")
def modifyCharacter(character_id):
    info = characters.info(character_id)
    print(info)
    return render_template("modifyCharacter.html", info = info, character_id = character_id)

@app.route("/modifyC/<int:character_id>", methods = ["POST"])
def modifyC(character_id):
    name = request.form["name"]
    lev = int(request.form["lev"])
    max_hp = int(request.form["max_hp"])
    characters.update_basics(character_id, name, lev, max_hp)
    back = "/hahmo/"+str(character_id)
    return redirect(back)
