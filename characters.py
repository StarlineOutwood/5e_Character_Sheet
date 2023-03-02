from db import db
from sqlalchemy.sql import text

def get_characters(id):
    all = db.session.execute(text('SELECT id, character_name, class, race, lev FROM characters WHERE user_id = :id'), {"id": id}).fetchall()
    return all

def ability_stats(id):
    sql = "SELECT ability, score, mod FROM ability_stats WHERE character_id = :id"
    current_stats = db.session.execute(text(sql), {"id": id}).fetchall()
    return current_stats

def skill_stats(id):
    sql = "SELECT skill, mod, is_prof FROM skill_stats WHERE character_id = :id"
    current_stats = db.session.execute(text(sql), {"id": id}).fetchall()
    return current_stats

def hp_stats(id):
    sql = "SELECT hp, max_hp, temp_hp FROM characters WHERE id = :id"
    hp = db.session.execute(text(sql), {"id": id}).fetchone()
    return hp

def damage(id, hp, temp):
    sql = "UPDATE characters SET temp_hp = :temp, hp = :hp  WHERE id  = :id"
    db.session.execute(text(sql), {"temp":temp, "hp": hp, "id": id})
    db.session.commit()
    return

def healing(id, hp):
    sql = "UPDATE characters SET hp = :hp WHERE id  = :id"
    db.session.execute(text(sql), {"hp":hp, "id": id})
    db.session.commit() 
    return

def add_temp_hp(id, temp):
    sql = "UPDATE characters SET temp_hp = :hp WHERE id = :character_id"
    db.session.execute(text(sql), {"character_id": id, "hp": temp})
    db.session.commit()

def info(id):
    info = db.session.execute(text("SELECT * FROM characters WHERE id = :id"), {"id": id}).fetchone()
    return info

def has_scores(id):
    sql = "SELECT COUNT(*) FROM ability_stats WHERE character_id = :character_id"
    n = db.session.execute(text(sql), {"character_id": id}).fetchone()
    return n

def update_abilities(ability_scores, abilities, id):
        for i in range(6):
            mod = ability_scores[i] - 10
            if (mod%2 != 0):
                mod = mod - 1
            mod = mod/2
            sql = "UPDATE ability_stats SET score= :score, mod = :mod WHERE ability = :ability AND character_id = :character_id"
            db.session.execute(text(sql), {"score": ability_scores[i], "mod": mod, "ability": abilities[i], "character_id": id})
            db.session.commit()
            for j in range(18):
                sql = "UPDATE skill_stats SET mod = :mod WHERE ability = :ability AND character_id = :character_id"
                db.session.execute(text(sql), {"character_id": id, "ability": abilities[i], "mod": mod})
                db.session.commit()
        return

def create_abilities(ability_scores, abilities, id, skills):
        for i in range(6):
            mod = ability_scores[i] - 10
            if (mod%2 != 0):
                mod = mod - 1
            mod = mod/2
            sql = "INSERT INTO ability_stats (character_id, ability, score, mod) VALUES (:id, :ability, :score, :mod)"
            db.session.execute(text(sql), {"id":id, "ability":abilities[i], "score":ability_scores[i], "mod": mod})
            db.session.commit()
            for j in range(18):
                if (abilities[i] == skills[j][1]):
                    sql = "INSERT INTO skill_stats (character_id, is_prof, ability, skill, mod) VALUES (:character_id, 0, :ability, :skill, :mod)"
                    db.session.execute(text(sql), {"character_id": id, "ability": abilities[i], "skill": skills[j][0], "mod": mod})
                    db.session.commit()
        return

def is_prof(id, is_prof):
    sql = "SELECT skill FROM skill_stats WHERE character_id = :character_id AND is_prof = :is_prof"
    profs = db.session.execute(text(sql), {"character_id": id, "is_prof":is_prof}).fetchall()
    return profs

def skill_increase(id):
    sql = "SELECT skills_choose FROM classes, characters WHERE classes.id = characters.class AND characters.id = :character_id"
    number = db.session.execute(text(sql), {"character_id":id}).fetchone()
    return number

def update_profs(id, profs):
    sql = "UPDATE skill_stats SET is_prof = 1 WHERE character_id = :character_id AND skill = :skill"
    for prof in profs:
        db.session.execute(text(sql), {"character_id": id, "skill":prof})
        db.session.commit()
    return

def add_character(name, race, character_class, level, user_id):
    sql = "SELECT hit_dice FROM classes WHERE id = :class_id"
    hit_dice = db.session.execute(text(sql), {"class_id":character_class}).fetchone()
    sql = "INSERT INTO characters (user_id, character_name, class, race, lev, max_hp, hp, temp_hp, hit_dice) VALUES (:id, :name, :class, :race, :level, 1, 1, 0, :hit_dice)"
    db.session.execute(text(sql), {"id": user_id, "name":name, "class":character_class, "race":race, "level":level, "hit_dice":hit_dice[0]})
    db.session.commit()
    return

def remove(ids):
    for id in ids:
        sql = "DELETE FROM characters WHERE id = :poistettava"
        db.session.execute(text(sql), {"poistettava":id})
        db.session.commit()
    return

def update_basics(character_id, name, lev, max_hp):
    sql = "UPDATE characters SET character_name = :name, lev = :lev, max_hp = :max_hp WHERE id = :character_id"
    db.session.execute(text(sql), {"name":name, "lev":lev, "max_hp":max_hp, "character_id":character_id})
    db.session.commit()
    return