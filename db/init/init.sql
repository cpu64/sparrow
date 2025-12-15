--
-- PostgreSQL database dump
--

\restrict 2X9mNdntIRpv86hSxJ7zWDpNO9NZiAl3rysy76VBqEd7FoppGTpGXsdLY5SNCl0

-- Dumped from database version 15.14 (Debian 15.14-0+deb12u1)
-- Dumped by pg_dump version 15.14 (Debian 15.14-0+deb12u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: sparrow; Type: SCHEMA; Schema: -; Owner: sparrow
--

CREATE SCHEMA sparrow;


ALTER SCHEMA sparrow OWNER TO sparrow;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: avatars; Type: TABLE; Schema: sparrow; Owner: sparrow
--

CREATE TABLE sparrow.avatars (
    id integer NOT NULL,
    name character varying(30) NOT NULL,
    url text NOT NULL,
    created_at timestamp without time zone DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'::text) NOT NULL
);


ALTER TABLE sparrow.avatars OWNER TO sparrow;

--
-- Name: avatars_id_seq; Type: SEQUENCE; Schema: sparrow; Owner: sparrow
--

ALTER TABLE sparrow.avatars ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME sparrow.avatars_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: chat_members; Type: TABLE; Schema: sparrow; Owner: sparrow
--

CREATE TABLE sparrow.chat_members (
    member_id integer NOT NULL,
    chat_id integer NOT NULL
);


ALTER TABLE sparrow.chat_members OWNER TO sparrow;

--
-- Name: chats; Type: TABLE; Schema: sparrow; Owner: sparrow
--

CREATE TABLE sparrow.chats (
    id integer NOT NULL,
    name character varying(60) NOT NULL,
    created_at timestamp without time zone DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'::text) NOT NULL,
    updated_at timestamp without time zone DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'::text) NOT NULL
);


ALTER TABLE sparrow.chats OWNER TO sparrow;

--
-- Name: chats_id_seq; Type: SEQUENCE; Schema: sparrow; Owner: sparrow
--

ALTER TABLE sparrow.chats ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME sparrow.chats_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: galleries; Type: TABLE; Schema: sparrow; Owner: sparrow
--

CREATE TABLE sparrow.galleries (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    description character varying(500),
    background_color character varying(255),
    created_at timestamp without time zone DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'::text) NOT NULL,
    updated_at timestamp without time zone DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'::text) NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE sparrow.galleries OWNER TO sparrow;

--
-- Name: galleries_id_seq; Type: SEQUENCE; Schema: sparrow; Owner: sparrow
--

ALTER TABLE sparrow.galleries ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME sparrow.galleries_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: image_comments; Type: TABLE; Schema: sparrow; Owner: sparrow
--

CREATE TABLE sparrow.image_comments (
    id integer NOT NULL,
    text character varying(255) NOT NULL,
    created_at timestamp without time zone DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'::text) NOT NULL,
    user_id integer NOT NULL,
    image_id integer NOT NULL
);


ALTER TABLE sparrow.image_comments OWNER TO sparrow;

--
-- Name: image_comments_id_seq; Type: SEQUENCE; Schema: sparrow; Owner: sparrow
--

ALTER TABLE sparrow.image_comments ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME sparrow.image_comments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: images; Type: TABLE; Schema: sparrow; Owner: sparrow
--

CREATE TABLE sparrow.images (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    url character varying(255) NOT NULL,
    description character varying(255),
    location character varying(255),
    taken_at date,
    created_at timestamp without time zone DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'::text) NOT NULL,
    gallery_id integer NOT NULL
);


ALTER TABLE sparrow.images OWNER TO sparrow;

--
-- Name: images_id_seq; Type: SEQUENCE; Schema: sparrow; Owner: sparrow
--

ALTER TABLE sparrow.images ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME sparrow.images_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: messages; Type: TABLE; Schema: sparrow; Owner: sparrow
--

CREATE TABLE sparrow.messages (
    id integer NOT NULL,
    text character varying(255) NOT NULL,
    seen boolean NOT NULL,
    created_at timestamp without time zone DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'::text) NOT NULL,
    updated_at timestamp without time zone DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'::text) NOT NULL,
    sender_id integer NOT NULL,
    chat_id integer NOT NULL
);


ALTER TABLE sparrow.messages OWNER TO sparrow;

--
-- Name: messages_id_seq; Type: SEQUENCE; Schema: sparrow; Owner: sparrow
--

ALTER TABLE sparrow.messages ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME sparrow.messages_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: post_comments; Type: TABLE; Schema: sparrow; Owner: sparrow
--

CREATE TABLE sparrow.post_comments (
    id integer NOT NULL,
    content character varying(500) NOT NULL,
    created_at timestamp without time zone DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2'::text) NOT NULL,
    user_id integer NOT NULL,
    post_id integer NOT NULL
);


ALTER TABLE sparrow.post_comments OWNER TO sparrow;

--
-- Name: post_comments_id_seq; Type: SEQUENCE; Schema: sparrow; Owner: sparrow
--

ALTER TABLE sparrow.post_comments ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME sparrow.post_comments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: post_tags; Type: TABLE; Schema: sparrow; Owner: sparrow
--

CREATE TABLE sparrow.post_tags (
    post_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE sparrow.post_tags OWNER TO sparrow;

--
-- Name: posts; Type: TABLE; Schema: sparrow; Owner: sparrow
--

CREATE TABLE sparrow.posts (
    id integer NOT NULL,
    content character varying(500) NOT NULL,
    text_color character varying(7) DEFAULT '#ffffff'::character varying NOT NULL,
    text_font integer NOT NULL,
    created_at timestamp without time zone DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2'::text) NOT NULL,
    views integer DEFAULT 0 NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE sparrow.posts OWNER TO sparrow;

--
-- Name: posts_id_seq; Type: SEQUENCE; Schema: sparrow; Owner: sparrow
--

ALTER TABLE sparrow.posts ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME sparrow.posts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: tags; Type: TABLE; Schema: sparrow; Owner: sparrow
--

CREATE TABLE sparrow.tags (
    id integer NOT NULL,
    name character varying(63) NOT NULL,
    created_at timestamp without time zone DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2'::text) NOT NULL
);


ALTER TABLE sparrow.tags OWNER TO sparrow;

--
-- Name: tags_id_seq; Type: SEQUENCE; Schema: sparrow; Owner: sparrow
--

ALTER TABLE sparrow.tags ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME sparrow.tags_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: text_fonts; Type: TABLE; Schema: sparrow; Owner: sparrow
--

CREATE TABLE sparrow.text_fonts (
    id integer NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE sparrow.text_fonts OWNER TO sparrow;

--
-- Name: text_fonts_id_seq; Type: SEQUENCE; Schema: sparrow; Owner: sparrow
--

ALTER TABLE sparrow.text_fonts ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME sparrow.text_fonts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users; Type: TABLE; Schema: sparrow; Owner: sparrow
--

CREATE TABLE sparrow.users (
    id integer NOT NULL,
    username character varying(30) NOT NULL,
    password character varying(60) NOT NULL,
    twofa_secret character varying(40),
    name character varying(30),
    surname character varying(30),
    email character varying(60),
    description character varying(1000),
    date_of_birth date,
    phone_number character varying(20),
    pronouns character varying(30),
    sex boolean,
    gender character varying(30),
    country character varying(30),
    created_at timestamp without time zone DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'::text) NOT NULL,
    updated_at timestamp without time zone DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'::text) NOT NULL,
    last_login timestamp without time zone,
    last_login_attempt timestamp without time zone,
    banned boolean DEFAULT false NOT NULL,
    admin boolean DEFAULT false NOT NULL,
    avatar_id integer DEFAULT 1 NOT NULL
);


ALTER TABLE sparrow.users OWNER TO sparrow;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: sparrow; Owner: sparrow
--

ALTER TABLE sparrow.users ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME sparrow.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: avatars; Type: TABLE DATA; Schema: sparrow; Owner: sparrow
--

COPY sparrow.avatars (id, name, url, created_at) FROM stdin;
1	Default Sparrow	https://github.githubassets.com/assets/pull-shark-default-498c279a747d.png	2025-12-15 09:52:14.160574
2	Sky Wanderer	https://github.githubassets.com/assets/pair-extraordinaire-default-579438a20e01.png	2025-12-15 09:52:14.160574
3	Night Owl	https://raw.githubusercontent.com/drknzz/GitHub-Achievements/main/Media/Badges/Heart-on-your-sleeve/PNG/HeartOnYourSleeve.png	2025-12-15 09:52:14.160574
4	Crimson Hawk	https://raw.githubusercontent.com/drknzz/GitHub-Achievements/main/Media/Badges/Quick-Draw/PNG/Skin-Tones/QuickDraw_SkinTone1.png	2025-12-15 09:52:14.160574
5	Golden Finch	https://raw.githubusercontent.com/drknzz/GitHub-Achievements/main/Media/Badges/Galaxy-Brain/PNG/GalaxyBrain.png	2025-12-15 09:52:14.160574
\.


--
-- Data for Name: chat_members; Type: TABLE DATA; Schema: sparrow; Owner: sparrow
--

COPY sparrow.chat_members (member_id, chat_id) FROM stdin;
1	1
2	1
3	2
2	2
\.


--
-- Data for Name: chats; Type: TABLE DATA; Schema: sparrow; Owner: sparrow
--

COPY sparrow.chats (id, name, created_at, updated_at) FROM stdin;
1	Naujas pokalbis	2025-12-15 09:56:09.790519	2025-12-15 09:57:09.754325
2	dar vienas pokalbis	2025-12-15 10:03:41.84461	2025-12-15 10:03:54.018718
\.


--
-- Data for Name: galleries; Type: TABLE DATA; Schema: sparrow; Owner: sparrow
--

COPY sparrow.galleries (id, name, description, background_color, created_at, updated_at, user_id) FROM stdin;
\.


--
-- Data for Name: image_comments; Type: TABLE DATA; Schema: sparrow; Owner: sparrow
--

COPY sparrow.image_comments (id, text, created_at, user_id, image_id) FROM stdin;
\.


--
-- Data for Name: images; Type: TABLE DATA; Schema: sparrow; Owner: sparrow
--

COPY sparrow.images (id, name, url, description, location, taken_at, created_at, gallery_id) FROM stdin;
\.


--
-- Data for Name: messages; Type: TABLE DATA; Schema: sparrow; Owner: sparrow
--

COPY sparrow.messages (id, text, seen, created_at, updated_at, sender_id, chat_id) FROM stdin;
2	zinute 2	f	2025-12-15 09:56:54.737028	2025-12-15 09:56:54.737028	2	1
1	zinute 1 Naujas turinys	f	2025-12-15 09:56:49.697723	2025-12-15 09:58:49.154488	2	1
3	labas	f	2025-12-15 09:57:09.746077	2025-12-15 09:57:09.746077	1	1
4	Labas	f	2025-12-15 10:03:46.500989	2025-12-15 10:03:46.500989	2	2
5	Kol kas tik vienas siunciu zinutes...	f	2025-12-15 10:03:54.012287	2025-12-15 10:03:54.012287	2	2
\.


--
-- Data for Name: post_comments; Type: TABLE DATA; Schema: sparrow; Owner: sparrow
--

COPY sparrow.post_comments (id, content, created_at, user_id, post_id) FROM stdin;
1	Great to be here!	2025-12-15 07:51:44.180756	3	1
2	Welcome aboard!	2025-12-15 07:51:54.180756	2	1
3	Enjoy your time exploring the city!	2025-12-15 07:51:49.180756	2	2
\.


--
-- Data for Name: post_tags; Type: TABLE DATA; Schema: sparrow; Owner: sparrow
--

COPY sparrow.post_tags (post_id, tag_id) FROM stdin;
2	1
2	2
1	3
1	4
3	4
\.


--
-- Data for Name: posts; Type: TABLE DATA; Schema: sparrow; Owner: sparrow
--

COPY sparrow.posts (id, content, text_color, text_font, created_at, views, user_id) FROM stdin;
1	Just finished a great book on web development. Highly recommend it!	#7a7a7a	1	2025-12-15 07:51:14.175392	0	2
2	Exploring the city today!	#ff5733	2	2025-12-15 07:50:14.175392	0	3
3	Welcome to Sparrow! This is my first post.	#33ff57	1	2025-12-15 07:49:14.175392	0	2
4	TEST1	#ffffff	1	2025-12-15 07:48:14.175392	0	1
5	TEST2	#ffffff	1	2025-12-15 07:47:14.175392	0	1
6	TEST3	#ffffff	1	2025-12-15 07:46:14.175392	0	1
7	TEST4	#ffffff	1	2025-12-15 07:45:14.175392	0	1
8	TEST5	#ffffff	1	2025-12-15 07:44:14.175392	0	1
9	TEST6	#ffffff	1	2025-12-15 07:43:14.175392	0	1
10	TEST7	#ffffff	1	2025-12-15 07:42:14.175392	0	1
11	TEST8	#ffffff	1	2025-12-15 07:41:14.175392	0	1
12	TEST9	#ffffff	1	2025-12-15 07:40:14.175392	0	1
13	TEST10	#ffffff	1	2025-12-15 07:39:14.175392	0	1
14	TEST11	#ffffff	1	2025-12-15 07:38:14.175392	0	1
15	TEST12	#ffffff	1	2025-12-15 07:37:14.175392	0	1
16	TEST13	#ffffff	1	2025-12-15 07:36:14.175392	0	1
17	TEST14	#ffffff	1	2025-12-15 07:35:14.175392	0	1
18	TEST15	#ffffff	1	2025-12-15 07:34:14.175392	0	1
19	TEST16	#ffffff	1	2025-12-15 07:33:14.175392	0	1
20	TEST17	#ffffff	1	2025-12-15 07:32:14.175392	0	1
21	TEST18	#ffffff	1	2025-12-15 07:31:14.175392	0	1
22	TEST19	#ffffff	1	2025-12-15 07:30:14.175392	0	1
23	TEST20	#ffffff	1	2025-12-15 07:29:14.175392	0	1
\.


--
-- Data for Name: tags; Type: TABLE DATA; Schema: sparrow; Owner: sparrow
--

COPY sparrow.tags (id, name, created_at) FROM stdin;
1	Travel	2025-12-15 07:52:14.187826
2	Photography	2025-12-15 07:52:14.187826
3	Books	2025-12-15 07:52:14.187826
4	Technology	2025-12-15 07:52:14.187826
\.


--
-- Data for Name: text_fonts; Type: TABLE DATA; Schema: sparrow; Owner: sparrow
--

COPY sparrow.text_fonts (id, name) FROM stdin;
1	Roboto
2	Pacifico
3	Monoton
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: sparrow; Owner: sparrow
--

COPY sparrow.users (id, username, password, twofa_secret, name, surname, email, description, date_of_birth, phone_number, pronouns, sex, gender, country, created_at, updated_at, last_login, last_login_attempt, banned, admin, avatar_id) FROM stdin;
2	aaa	$2b$12$o9GVcvT8VfmBN6BA.PVWb.zudArlfr5T6AL2V03uAYLKXmr/ez6aS	\N	Luna	Martinez	luna.martinez@example.com	Photographer and traveler. Loves capturing sunsets.	1995-08-22	+34911222333	she/her	t	female	Spain	2025-12-15 09:52:14.16935	2025-12-15 09:52:14.16935	2025-12-15 10:03:19.505119	2025-12-15 10:03:19.505119	f	f	2
1	admin	$2b$12$VEUlGiag6gJv.S6i51/i3Ov00lICVZsK37xVwA/1wC5KBVvJItgUK	\N	Avery	Stone	luna.admin@example.com	System administrator and founder of the Sparrow platform.	1990-05-14	+12025550111	they/them	\N	nonbinary	United States	2025-12-15 09:52:14.16935	2025-12-15 09:52:14.16935	2025-12-15 10:04:34.294114	2025-12-15 10:04:34.294114	f	t	1
3	bbb	$2b$12$gZWy1JhHy.SaMjVBlgs0zOz2AT.h8AI8ekaYyVlu1OVGZ.j28ZMA2	G62SY3MV3MUS3F3ZT2BGAPTG7LGAR7TP	Noah	Kim	noah.kim@example.com	Software engineer and gamer.	1998-03-10	+821012345678	he/him	t	male	South Korea	2025-12-15 09:52:14.16935	2025-12-15 09:52:14.16935	2025-12-10 09:52:14.16935	2025-12-15 10:05:40.881577	f	f	3
\.


--
-- Name: avatars_id_seq; Type: SEQUENCE SET; Schema: sparrow; Owner: sparrow
--

SELECT pg_catalog.setval('sparrow.avatars_id_seq', 9, true);


--
-- Name: chats_id_seq; Type: SEQUENCE SET; Schema: sparrow; Owner: sparrow
--

SELECT pg_catalog.setval('sparrow.chats_id_seq', 2, true);


--
-- Name: galleries_id_seq; Type: SEQUENCE SET; Schema: sparrow; Owner: sparrow
--

SELECT pg_catalog.setval('sparrow.galleries_id_seq', 1, false);


--
-- Name: image_comments_id_seq; Type: SEQUENCE SET; Schema: sparrow; Owner: sparrow
--

SELECT pg_catalog.setval('sparrow.image_comments_id_seq', 1, false);


--
-- Name: images_id_seq; Type: SEQUENCE SET; Schema: sparrow; Owner: sparrow
--

SELECT pg_catalog.setval('sparrow.images_id_seq', 1, false);


--
-- Name: messages_id_seq; Type: SEQUENCE SET; Schema: sparrow; Owner: sparrow
--

SELECT pg_catalog.setval('sparrow.messages_id_seq', 5, true);


--
-- Name: post_comments_id_seq; Type: SEQUENCE SET; Schema: sparrow; Owner: sparrow
--

SELECT pg_catalog.setval('sparrow.post_comments_id_seq', 3, true);


--
-- Name: posts_id_seq; Type: SEQUENCE SET; Schema: sparrow; Owner: sparrow
--

SELECT pg_catalog.setval('sparrow.posts_id_seq', 23, true);


--
-- Name: tags_id_seq; Type: SEQUENCE SET; Schema: sparrow; Owner: sparrow
--

SELECT pg_catalog.setval('sparrow.tags_id_seq', 4, true);


--
-- Name: text_fonts_id_seq; Type: SEQUENCE SET; Schema: sparrow; Owner: sparrow
--

SELECT pg_catalog.setval('sparrow.text_fonts_id_seq', 15, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: sparrow; Owner: sparrow
--

SELECT pg_catalog.setval('sparrow.users_id_seq', 3, true);


--
-- Name: avatars avatars_name_key; Type: CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.avatars
    ADD CONSTRAINT avatars_name_key UNIQUE (name);


--
-- Name: avatars avatars_pkey; Type: CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.avatars
    ADD CONSTRAINT avatars_pkey PRIMARY KEY (id);


--
-- Name: avatars avatars_url_key; Type: CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.avatars
    ADD CONSTRAINT avatars_url_key UNIQUE (url);


--
-- Name: chats chats_pkey; Type: CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.chats
    ADD CONSTRAINT chats_pkey PRIMARY KEY (id);


--
-- Name: galleries galleries_pkey; Type: CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.galleries
    ADD CONSTRAINT galleries_pkey PRIMARY KEY (id);


--
-- Name: image_comments image_comments_pkey; Type: CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.image_comments
    ADD CONSTRAINT image_comments_pkey PRIMARY KEY (id);


--
-- Name: images images_pkey; Type: CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.images
    ADD CONSTRAINT images_pkey PRIMARY KEY (id);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (id);


--
-- Name: post_comments post_comments_pkey; Type: CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.post_comments
    ADD CONSTRAINT post_comments_pkey PRIMARY KEY (id);


--
-- Name: post_tags post_tags_pkey; Type: CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.post_tags
    ADD CONSTRAINT post_tags_pkey PRIMARY KEY (post_id, tag_id);


--
-- Name: posts posts_pkey; Type: CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (id);


--
-- Name: tags tags_name_key; Type: CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.tags
    ADD CONSTRAINT tags_name_key UNIQUE (name);


--
-- Name: tags tags_pkey; Type: CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (id);


--
-- Name: text_fonts text_fonts_name_key; Type: CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.text_fonts
    ADD CONSTRAINT text_fonts_name_key UNIQUE (name);


--
-- Name: text_fonts text_fonts_pkey; Type: CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.text_fonts
    ADD CONSTRAINT text_fonts_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: messages fk_chat_id; Type: FK CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.messages
    ADD CONSTRAINT fk_chat_id FOREIGN KEY (chat_id) REFERENCES sparrow.chats(id) ON DELETE CASCADE;


--
-- Name: chat_members fk_chat_id; Type: FK CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.chat_members
    ADD CONSTRAINT fk_chat_id FOREIGN KEY (chat_id) REFERENCES sparrow.chats(id);


--
-- Name: chat_members fk_member_id; Type: FK CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.chat_members
    ADD CONSTRAINT fk_member_id FOREIGN KEY (member_id) REFERENCES sparrow.users(id);


--
-- Name: messages fk_sender_id; Type: FK CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.messages
    ADD CONSTRAINT fk_sender_id FOREIGN KEY (sender_id) REFERENCES sparrow.users(id) ON DELETE CASCADE;


--
-- Name: galleries galleries_user_id_fkey; Type: FK CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.galleries
    ADD CONSTRAINT galleries_user_id_fkey FOREIGN KEY (user_id) REFERENCES sparrow.users(id) ON DELETE CASCADE;


--
-- Name: image_comments image_comments_image_id_fkey; Type: FK CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.image_comments
    ADD CONSTRAINT image_comments_image_id_fkey FOREIGN KEY (image_id) REFERENCES sparrow.images(id) ON DELETE CASCADE;


--
-- Name: image_comments image_comments_user_id_fkey; Type: FK CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.image_comments
    ADD CONSTRAINT image_comments_user_id_fkey FOREIGN KEY (user_id) REFERENCES sparrow.users(id) ON DELETE CASCADE;


--
-- Name: images images_gallery_id_fkey; Type: FK CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.images
    ADD CONSTRAINT images_gallery_id_fkey FOREIGN KEY (gallery_id) REFERENCES sparrow.galleries(id) ON DELETE CASCADE;


--
-- Name: post_comments post_comments_post_id_fkey; Type: FK CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.post_comments
    ADD CONSTRAINT post_comments_post_id_fkey FOREIGN KEY (post_id) REFERENCES sparrow.posts(id) ON DELETE CASCADE;


--
-- Name: post_comments post_comments_user_id_fkey; Type: FK CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.post_comments
    ADD CONSTRAINT post_comments_user_id_fkey FOREIGN KEY (user_id) REFERENCES sparrow.users(id) ON DELETE CASCADE;


--
-- Name: post_tags post_tags_post_id_fkey; Type: FK CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.post_tags
    ADD CONSTRAINT post_tags_post_id_fkey FOREIGN KEY (post_id) REFERENCES sparrow.posts(id) ON DELETE CASCADE;


--
-- Name: post_tags post_tags_tag_id_fkey; Type: FK CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.post_tags
    ADD CONSTRAINT post_tags_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES sparrow.tags(id) ON DELETE CASCADE;


--
-- Name: posts posts_user_id_fkey; Type: FK CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.posts
    ADD CONSTRAINT posts_user_id_fkey FOREIGN KEY (user_id) REFERENCES sparrow.users(id);


--
-- Name: users users_avatar_id_fkey; Type: FK CONSTRAINT; Schema: sparrow; Owner: sparrow
--

ALTER TABLE ONLY sparrow.users
    ADD CONSTRAINT users_avatar_id_fkey FOREIGN KEY (avatar_id) REFERENCES sparrow.avatars(id);


--
-- PostgreSQL database dump complete
--

\unrestrict 2X9mNdntIRpv86hSxJ7zWDpNO9NZiAl3rysy76VBqEd7FoppGTpGXsdLY5SNCl0

