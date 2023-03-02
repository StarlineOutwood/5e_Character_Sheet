CREATE TABLE races (id SERIAL PRIMARY KEY, race_name TEXT, speed INTEGER, score_increases TEXT, proficiencies TEXT);
CREATE TABLE classes (id SERIAL PRIMARY KEY, class_name TEXT, hit_dice INTEGER, armor_prof TEXT, weapons_prof TEXT, tools_prof TEXT, saving_prof TEXT, skills_choose INTEGER, spell_mod TEXT);
CREATE TABLE characters (id SERIAL PRIMARY KEY, user_id INTEGER, character_name TEXT UNIQUE, race INTEGER, class INTEGER, lev INTEGER, max_hp INTEGER, hp INTEGER, hit_dice INTEGER, temp_hp INTEGER);
CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT);
CREATE TABLE ability_stats(character_id INTEGER, is_prof INTEGER, ability TEXT, score INTEGER, mod INTEGER, saving_throw INTEGER);
CREATE TABLE skill_stats(character_id INTEGER, is_prof INTEGER, ability TEXT, skill TEXT, mod INTEGER);


CREATE TABLE languages (id SERIAL PRIMARY KEY, language_name TEXT);
CREATE TABLE spells_known (class_id INTEGER, class_level INTEGER, spells INTEGER, cantrips INTEGER, lev_1 INTEGER, lev_2 INTEGER, lev_3 INTEGER, lev_4 INTEGER, lev_5 INTEGER, lev_6 INTEGER, lev_7 INTEGER, lev_8 INTEGER, lev_9 INTEGER);
CREATE TABLE specialities (class_id INTEGER, class_level INTEGER, speciality TEXT, speciality_meter TEXT);
CREATE TABLE traits (race_id INTEGER, trait TEXT, desctiption TEXT);