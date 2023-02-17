CREATE TABLE races2 (id SERIAL PRIMARY KEY, race_name TEXT, speed INTEGER, score_increases TEXT, proficiencies TEXT);
CREATE TABLE classes3 (id SERIAL PRIMARY KEY, class_name TEXT, hit_dice INTEGER, armor_prof TEXT, weapons_prof TEXT, tools_prof TEXT, saving_prof TEXT, skills_choose INTEGER, spell_mod TEXT);
CREATE TABLE languages (id SERIAL PRIMARY KEY, language_name TEXT);
CREATE TABLE skills (class_id INTEGER, skill TEXT);
CREATE TABLE spells_known (class_id INTEGER, class_level INTEGER, spells INTEGER, cantrips INTEGER, lev_1 INTEGER, lev_2 INTEGER, lev_3 INTEGER, lev_4 INTEGER, lev_5 INTEGER, lev_6 INTEGER, lev_7 INTEGER, lev_8 INTEGER, lev_9 INTEGER);
CREATE TABLE specialities2 (class_id INTEGER, class_level INTEGER, speciality TEXT, speciality_meter TEXT);
CREATE TABLE traits (race_id INTEGER, trait TEXT, desctiption TEXT);