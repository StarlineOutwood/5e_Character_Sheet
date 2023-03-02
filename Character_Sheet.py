from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
    if session["id"]:
        return redirect("/party")
    return render_template("frontPage.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/createUser",methods=["POST"])
def createUser():
    username = request.form["username"]
    password = request.form["password"]
    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    db.session.execute(text(sql), {"username": username, "password": password})
    db.session.commit()
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT id FROM users WHERE username = :username AND password = :password"
    tulos = db.session.execute(text(sql), {"username":username, "password": password}).fetchone()
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
    result = db.session.execute(text('SELECT id, character_name, class, race, lev FROM characters WHERE user_id = :id'), {"id": id})
    characters = result.fetchall()
    print(characters)
    return render_template("frontPage.html", hahmot = characters)

@app.route("/newC1")
def newC1():
    sql1 = 'SELECT id, class_name FROM classes'
    sql2 = 'SELECT id, race_name FROM races'
    result1 = db.session.execute(text(sql1)).fetchall()
    result2 = db.session.execute(text(sql2)).fetchall()
    return render_template("newC1.html", classes = result1, races = result2)

@app.route("/modifyAbilities/<int:character_id>")
def modifyAbilities(character_id):
    sql = "SELECT ability, score FROM ability_stats WHERE character_id = :id"
    current_stats = db.session.execute(text(sql), {"id": character_id}).fetchall()
    race = db.session.execute(text("SELECT race FROM characters WHERE id = :id"), {"id": character_id}).fetchone()
    print(race)
    print(character_id)
    print("TASSA ON RACE JA CHARACTER ID")
    sql2 = "SELECT score_increases FROM races WHERE id = :race"
    increases = db.session.execute(text(sql2), {"race":race[0]}).fetchall()
    if current_stats:
        return render_template("modifyAbilities.html", score_increase = increases[0][0], stats = current_stats, character_id = character_id)
    else:
        start = [("Wisdom", 10), ("Charisma", 10), ("Intelligence", 10), ("Dexterity", 10), ("Constitution", 10), ("Strenght", 10)]
        return render_template("modifyAbilities.html", score_increase = increases[0][0], stats = start, character_id = character_id)

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
    sql = "SELECT COUNT(*) FROM ability_stats WHERE character_id = :character_id"
    n = db.session.execute(text(sql), {"character_id": character_id}).fetchone()
    print(n)
    if n[0]>0:
        for i in range(6):
            mod = ability_scores[i] - 10
            if (mod%2 != 0):
                mod = mod - 1
            mod = mod/2
            sql = "UPDATE ability_stats SET score= :score, mod = :mod WHERE ability = :ability AND character_id = :character_id"
            db.session.execute(text(sql), {"score": ability_scores[i], "mod": mod, "ability": abilities[i], "character_id": character_id})
            db.session.commit()
            for j in range(18):
                sql = "UPDATE skill_stats SET mod = :mod WHERE ability = :ability AND character_id = :character_id"
                db.session.execute(text(sql), {"character_id": character_id, "ability": abilities[i], "mod": mod})
                db.session.commit()
    else:
        for i in range(6):
            mod = ability_scores[i] - 10
            if (mod%2 != 0):
                mod = mod - 1
            mod = mod/2
            sql = "INSERT INTO ability_stats (character_id, ability, score, mod) VALUES (:id, :ability, :score, :mod)"
            db.session.execute(text(sql), {"id":character_id, "ability":abilities[i], "score":ability_scores[i], "mod": mod})
            db.session.commit()
            for j in range(18):
                if (abilities[i] == skills[j][1]):
                    sql = "INSERT INTO skill_stats (character_id, is_prof, ability, skill, mod) VALUES (:character_id, 0, :ability, :skill, :mod)"
                    db.session.execute(text(sql), {"character_id": character_id, "ability": abilities[i], "skill": skills[j][0], "mod": mod})
                    db.session.commit()
    sql = "SELECT skill FROM skill_stats WHERE character_id = :character_id AND is_prof = 1"
    profs = db.session.execute(text(sql), {"character_id": character_id}).fetchall()
    sql = "SELECT skill FROM skill_stats WHERE character_id = :character_id AND is_prof = 0"
    non_profs = db.session.execute(text(sql), {"character_id": character_id}).fetchall()
    sql = "SELECT skills_choose FROM classes, characters WHERE classes.id = characters.class AND characters.id = :character_id"
    number = db.session.execute(text(sql), {"character_id":character_id}).fetchone()
    return render_template("modifySkills.html", profs = profs, non_profs= non_profs, character_id = character_id, n = number[0])

@app.route("/finishModifyingStats/<int:character_id>", methods=["POST"])
def finishModifyingStats(character_id):
    profs = request.form.getlist("skill")
    sql = "UPDATE skill_stats SET is_prof = 1 WHERE character_id = :character_id AND skill = :skill"
    for prof in profs:
        db.session.execute(text(sql), {"character_id": character_id, "skill":prof})
        db.session.commit()
    back = "/hahmo/" + str(character_id)
    return redirect(back)
    
        

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    race = request.form["race"]
    character_class = request.form["class"]
    level = request.form["level"]
    user_id = session["id"]
    sql = "SELECT hit_dice FROM classes WHERE id = :class_id"
    hit_dice = db.session.execute(text(sql), {"class_id":character_class}).fetchone()
    sql = "INSERT INTO characters (user_id, character_name, class, race, lev, max_hp, hp, temp_hp, hit_dice) VALUES (:id, :name, :class, :race, :level, 1, 1, 0, :hit_dice)"
    db.session.execute(text(sql), {"id": user_id, "name":name, "class":character_class, "race":race, "level":level, "hit_dice":hit_dice[0]})
    db.session.commit()
    return redirect ("/party")

@app.route("/removeC")
def removeC():
    user_id = session["id"]
    sql = "SELECT id, character_name FROM characters WHERE user_id = :id"
    names = db.session.execute(text(sql), {"id": user_id})
    return render_template("removeC.html", names = names)

@app.route("/remove", methods=["POST"])
def remove():
    ids = request.form.getlist["poistettava"]
    for id in ids:
        sql = "DELETE FROM characters WHERE id = :poistettava"
        db.session.execute(text(sql), {"poistettava":id})
        db.session.commit()
    return redirect ("/party")

@app.route("/hahmo/<int:character_id>")
def character(character_id):
    sql = "SELECT character_name, race, class, lev, hp, max_hp, temp_hp, hit_dice FROM characters WHERE id = :id"
    info = db.session.execute((text(sql)), {"id":character_id}).fetchall()
    name = info[0][0]
    race_id = info[0][1]
    character_class_id = info[0][2]
    level = info[0][3]
    hp = info[0][4]
    max_hp = info[0][5]
    temp_hp = info[0][6]
    hit_dice = info[0][7]
    message = ""
    if (hp < 1):
        message = "Your character is rolling death savingthrows."
    character_class = db.session.execute((text("SELECT class_name FROM classes WHERE id = :class_id")), {"class_id":character_class_id}).fetchone()
    race = db.session.execute((text("SELECT race_name FROM races WHERE id = :race_id")), {"race_id":race_id}).fetchone()
    sql = "SELECT score, mod, ability FROM ability_stats WHERE character_id = :character_id"
    abilities = db.session.execute(text(sql), {"character_id": character_id}).fetchall()
    sql = "SELECT skill, mod, is_prof, ability FROM skill_stats WHERE character_id = :character_id"
    skills = db.session.execute(text(sql), {"character_id": character_id})
    return render_template("hahmo.html", name = name, race = race[0], character_class= character_class[0], level = level, character_id = character_id, 
                           abilities = abilities, skills = skills, hp = hp, max_hp = max_hp, temp_hp = temp_hp, hit_dice = hit_dice, message=message)

@app.route("/changeHP/<int:character_id>", methods=["POST"])
def changeHP(character_id):
    sql = "SELECT hp, max_hp, temp_hp FROM characters WHERE id = :id"
    hp = db.session.execute(text(sql), {"id": character_id}).fetchone()
    change = int(request.form["change"])
    if (change < 0 and change*(-1) <= hp[2]): #if damage but smaller than temp hp
        sql = "UPDATE characters SET temp_hp = :temp + :change WHERE id  = :id"
        db.session.execute(text(sql), {"temp":hp[2], "change": change, "id": character_id})
        db.session.commit()
    else:
        if (change < 0 and change*(-1) > hp[2]): #if damage and greater than temp hp
            change += hp[2]
            if (hp[0] + change <= 0): #if goes to dst
                sql = "UPDATE characters SET hp = 0, temp_hp = 0 WHERE id  = :id"
                db.session.execute(text(sql), {"id": character_id})
                db.session.commit()
            else: #if just damage
                sql = "UPDATE characters SET hp = :now + :change, temp_hp = 0 WHERE id = :character_id"
                db.session.execute(text(sql), {"character_id": character_id, "change": change, "now": hp[0]})
                db.session.commit()
        else: #if healing
            if (hp[0] + change >= hp[1]):
                sql = "UPDATE characters SET hp = :max WHERE id  = :id"
                db.session.execute(text(sql), {"max":hp[1], "id": character_id})
                db.session.commit()
            else:
                sql = "UPDATE characters SET hp = (SELECT hp FROM characters WHERE id = :character_id) + :hp WHERE id = :character_id"
                db.session.execute(text(sql), {"character_id": character_id, "hp": change})
                db.session.commit()
    back = "/hahmo/"+str(character_id)
    return redirect(back)

@app.route("/addTempHP/<int:character_id>", methods=["POST"])
def addTempHP(character_id):
    sql = "UPDATE characters SET temp_hp = :hp WHERE id = :character_id"
    change = request.form["change"]
    db.session.execute(text(sql), {"character_id": character_id, "hp": change})
    db.session.commit()
    back = "/hahmo/"+str(character_id)
    return redirect(back)

@app.route("/modifyCharacter/<int:character_id>")
def modifyCharacter(character_id):
    sql = "SELECT character_name, lev, max_hp FROM characters WHERE id = :character_id"
    info = db.session.execute(text(sql), {"character_id":character_id}).fetchall()
    return render_template("modifyCharacter.html", info = info, character_id = character_id)

@app.route("/modifyC/<int:character_id>", methods = ["POST"])
def modifyC(character_id):
    name = request.form["name"]
    lev = int(request.form["lev"])
    max_hp = int(request.form["max_hp"])
    sql = "UPDATE characters SET character_name = :name, lev = :lev, max_hp = :max_hp WHERE id = :character_id"
    db.session.execute(text(sql), {"name":name, "lev":lev, "max_hp":max_hp, "character_id":character_id})
    db.session.commit()
    back = "/hahmo/"+str(character_id)
    return redirect(back)