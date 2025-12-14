CREATE SCHEMA IF NOT EXISTS sparrow;
SET search_path TO sparrow;

CREATE TABLE IF NOT EXISTS avatars (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(30) UNIQUE NOT NULL,
    url TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC')
);

INSERT INTO avatars (name, url)
VALUES
    ('Default Sparrow', 'https://avatar.iran.liara.run/public/6'),
    ('Sky Wanderer', 'https://avatar.iran.liara.run/public/17'),
    ('Night Owl', 'https://avatar.iran.liara.run/public/9'),
    ('Crimson Hawk', 'https://avatar.iran.liara.run/public/23'),
    ('Golden Finch', 'https://avatar.iran.liara.run/public/48');

CREATE TABLE IF NOT EXISTS users (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username VARCHAR(30) UNIQUE NOT NULL,
    password VARCHAR(60) NOT NULL,
    twofa_secret VARCHAR(40),
    name VARCHAR(30),
    surname VARCHAR(30),
    email VARCHAR(60),
    description VARCHAR(1000),
    date_of_birth DATE,
    phone_number VARCHAR(20),
    pronouns VARCHAR(30),
    sex BOOLEAN,
    gender VARCHAR(30),
    country VARCHAR(30),
    created_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
    updated_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
    last_login TIMESTAMP,
    last_login_attempt TIMESTAMP,
    banned BOOLEAN NOT NULL DEFAULT FALSE,
    admin BOOLEAN NOT NULL DEFAULT FALSE,
    avatar_id INT NOT NULL DEFAULT 1 REFERENCES avatars(id)
);

INSERT INTO users (
    username, password, twofa_secret, name, surname, email, description,
    date_of_birth, phone_number, pronouns, sex, gender, country,
    last_login, last_login_attempt, banned, admin, avatar_id
) VALUES
    (
        'admin',
        '$2b$12$VEUlGiag6gJv.S6i51/i3Ov00lICVZsK37xVwA/1wC5KBVvJItgUK', --admin
        NULL,
        'Avery',
        'Stone',
        'luna.admin@example.com',
        'System administrator and founder of the Sparrow platform.',
        '1990-05-14',
        '+12025550111',
        'they/them',
        NULL,
        'nonbinary',
        'United States',
        (CURRENT_TIMESTAMP AT TIME ZONE 'UTC') - INTERVAL '1 day',
        (CURRENT_TIMESTAMP AT TIME ZONE 'UTC') - INTERVAL '1 day',
        FALSE,
        TRUE,
        1
    ),
    (
        'aaa',
        '$2b$12$o9GVcvT8VfmBN6BA.PVWb.zudArlfr5T6AL2V03uAYLKXmr/ez6aS', --aaa
        NULL,
        'Luna',
        'Martinez',
        'luna.martinez@example.com',
        'Photographer and traveler. Loves capturing sunsets.',
        '1995-08-22',
        '+34911222333',
        'she/her',
        TRUE,
        'female',
        'Spain',
        (CURRENT_TIMESTAMP AT TIME ZONE 'UTC') - INTERVAL '3 hours',
        (CURRENT_TIMESTAMP AT TIME ZONE 'UTC') - INTERVAL '2 hours',
        FALSE,
        FALSE,
        2
    ),
    (
        'bbb',
        '$2b$12$gZWy1JhHy.SaMjVBlgs0zOz2AT.h8AI8ekaYyVlu1OVGZ.j28ZMA2', --bbb
        'G62SY3MV3MUS3F3ZT2BGAPTG7LGAR7TP',
        'Noah',
        'Kim',
        'noah.kim@example.com',
        'Software engineer and gamer.',
        '1998-03-10',
        '+821012345678',
        'he/him',
        TRUE,
        'male',
        'South Korea',
        (CURRENT_TIMESTAMP AT TIME ZONE 'UTC') - INTERVAL '5 days',
        (CURRENT_TIMESTAMP AT TIME ZONE 'UTC') - INTERVAL '5 days',
        FALSE,
        FALSE,
        3
    );
