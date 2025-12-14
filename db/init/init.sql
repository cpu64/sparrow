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
    ('Default Sparrow', 'https://github.githubassets.com/assets/pull-shark-default-498c279a747d.png'),
    ('Sky Wanderer', 'https://github.githubassets.com/assets/pair-extraordinaire-default-579438a20e01.png'),
    ('Night Owl', 'https://raw.githubusercontent.com/drknzz/GitHub-Achievements/main/Media/Badges/Heart-on-your-sleeve/PNG/HeartOnYourSleeve.png'),
    ('Crimson Hawk', 'https://raw.githubusercontent.com/drknzz/GitHub-Achievements/main/Media/Badges/Quick-Draw/PNG/Skin-Tones/QuickDraw_SkinTone1.png'),
    ('Golden Finch', 'https://raw.githubusercontent.com/drknzz/GitHub-Achievements/main/Media/Badges/Galaxy-Brain/PNG/GalaxyBrain.png');

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

CREATE TABLE IF NOT EXISTS posts (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    content VARCHAR(500) NOT NULL,
    text_color VARCHAR(7) NOT NULL DEFAULT '#ffffff',
    text_font INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2'),
    views INT NOT NULL DEFAULT 0,
    user_id INT NOT NULL REFERENCES users(id)
);
INSERT INTO posts (content, text_color, text_font, user_id, created_at)
VALUES
('Just finished a great book on web development. Highly recommend it!', '#7a7a7a', 1, 2, (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2') - INTERVAL '1 minutes'),
('Exploring the city today!', '#ff5733', 2, 3, (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2') - INTERVAL '2 minutes'),
('Welcome to Sparrow! This is my first post.', '#33ff57', 1, 2, (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2') - INTERVAL '3 minutes'),
('TEST1', '#ffffff', 1, 1, (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2') - INTERVAL '4 minutes'),
('TEST2', '#ffffff', 1, 1, (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2') - INTERVAL '5 minutes'),
('TEST3', '#ffffff', 1, 1, (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2') - INTERVAL '6 minutes'),
('TEST4', '#ffffff', 1, 1, (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2') - INTERVAL '7 minutes'),
('TEST5', '#ffffff', 1, 1, (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2') - INTERVAL '8 minutes'),
('TEST6', '#ffffff', 1, 1, (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2') - INTERVAL '9 minutes'),
('TEST7', '#ffffff', 1, 1, (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2') - INTERVAL '10 minutes'),
('TEST8', '#ffffff', 1, 1, (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2') - INTERVAL '11 minutes'),
('TEST9', '#ffffff', 1, 1, (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2') - INTERVAL '12 minutes'),
('TEST10', '#ffffff', 1, 1, (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2') - INTERVAL '13 minutes'),
('TEST11', '#ffffff', 1, 1, (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2') - INTERVAL '14 minutes'),
('TEST12', '#ffffff', 1, 1, (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2') - INTERVAL '15 minutes'),
('TEST13', '#ffffff', 1, 1, (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2') - INTERVAL '16 minutes'),
('TEST14', '#ffffff', 1, 1, (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2') - INTERVAL '17 minutes'),
('TEST15', '#ffffff', 1, 1, (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2') - INTERVAL '18 minutes'),
('TEST16', '#ffffff', 1, 1, (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2') - INTERVAL '19 minutes'),
('TEST17', '#ffffff', 1, 1, (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2') - INTERVAL '20 minutes'),
('TEST18', '#ffffff', 1, 1, (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2') - INTERVAL '21 minutes'),
('TEST19', '#ffffff', 1, 1, (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2') - INTERVAL '22 minutes'),
('TEST20', '#ffffff', 1, 1, (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2') - INTERVAL '23 minutes');


CREATE TABLE IF NOT EXISTS comments (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    content VARCHAR(500) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2'),
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    post_id INT NOT NULL REFERENCES posts(id) ON DELETE CASCADE
);
INSERT INTO comments (content, user_id, post_id, created_at)
VALUES
('Great to be here!', 3, 1, (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2') - INTERVAL '30 seconds'),
('Welcome aboard!', 2, 1, (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2') - INTERVAL '20 seconds'),
('Enjoy your time exploring the city!', 2, 2, (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2') - INTERVAL '25 seconds');

CREATE TABLE IF NOT EXISTS tags (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(63) UNIQUE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2')
);
INSERT INTO tags (name)
VALUES
('Travel'),
('Photography'),
('Books'),
('Technology');

CREATE TABLE IF NOT EXISTS post_tags (
    post_id INT REFERENCES posts(id) ON DELETE CASCADE,
    tag_id INT REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, tag_id)
);
INSERT INTO post_tags (post_id, tag_id)
VALUES
((SELECT id FROM posts WHERE content = 'Exploring the city today!'), (SELECT id FROM tags WHERE name = 'Travel')),
((SELECT id FROM posts WHERE content = 'Exploring the city today!'), (SELECT id FROM tags WHERE name = 'Photography')),
((SELECT id FROM posts WHERE content = 'Just finished a great book on web development. Highly recommend it!'), (SELECT id FROM tags WHERE name = 'Books')),
((SELECT id FROM posts WHERE content = 'Just finished a great book on web development. Highly recommend it!'), (SELECT id FROM tags WHERE name = 'Technology')),
((SELECT id FROM posts WHERE content = 'Welcome to Sparrow! This is my first post.'), (SELECT id FROM tags WHERE name = 'Technology'));

CREATE TABLE IF NOT EXISTS text_fonts(
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO text_fonts (name)
VALUES
('Roboto'),
('Pacifico'),
('Monoton')
ON CONFLICT (name) DO NOTHING;
