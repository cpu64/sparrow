CREATE SCHEMA IF NOT EXISTS my_schema;

SET search_path TO my_schema;

CREATE TABLE IF NOT EXISTS AVATARAS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pavadinimas VARCHAR(30) NOT NULL,
    nuoroda TEXT NOT NULL,
    sukurimo_data TIMESTAMP NOT NULL
);

INSERT INTO AVATARAS (pavadinimas, nuoroda, sukurimo_data) VALUES
('Default Avatar', 'https://example.com/avatar1.png', CURRENT_TIMESTAMP),
('Cool Cat', 'https://example.com/avatar2.png', CURRENT_TIMESTAMP),
('Mountain Hiker', 'https://example.com/avatar3.png', CURRENT_TIMESTAMP),
('Space Explorer', 'https://example.com/avatar4.png', CURRENT_TIMESTAMP),
('Sunset Vibes', 'https://example.com/avatar5.png', CURRENT_TIMESTAMP),
('Tech Wizard', 'https://example.com/avatar6.png', CURRENT_TIMESTAMP),
('Ocean Breeze', 'https://example.com/avatar7.png', CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS NAUDOTOJAS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    slapvardis VARCHAR(30) UNIQUE NOT NULL,
    slaptazodis VARCHAR(60) NOT NULL,
    vardas VARCHAR(30),
    pavarde VARCHAR(30),
    el_pastas VARCHAR(60),
    du_fa_paslaptis VARCHAR(40),
    biografija VARCHAR(1000),
    gimimo_data TIMESTAMP,
    telefono_nr VARCHAR(20),
    narsykle VARCHAR(30),
    lytis BOOLEAN,
    lyties_tapatybe VARCHAR(30),
    pilietybe VARCHAR(30),
    sukurimo_data TIMESTAMP NOT NULL,
    redagavimo_data TIMESTAMP NOT NULL,
    paskutinio_prisijungimo_data TIMESTAMP,
    uzblokuotas BOOLEAN DEFAULT FALSE,
    administratorius BOOLEAN DEFAULT FALSE,
    avataras_id INT,
    FOREIGN KEY (avataras_id) REFERENCES AVATARAS(id)
);

INSERT INTO NAUDOTOJAS (vardas, pavarde, el_pastas, slapvardis, slaptazodis, du_fa_paslaptis, biografija, gimimo_data, telefono_nr, narsykle, lytis, lyties_tapatybe, pilietybe, sukurimo_data, redagavimo_data, paskutinio_prisijungimo_data, uzblokuotas, administratorius, avataras_id)
VALUES
('Jonas', 'Jonaitis', 'jonas@example.com', 'jonasj', 'hashedpassword123', '2FAKey1', 'Developer and photographer.', '1990-01-01', '+37060000001', 'Firefox', 'Vyras', 'Cis', 'Lietuva', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE, TRUE, 1),
('Eglė', 'Petrauskaitė', 'egle@example.com', 'egle_p', 'securepass456', '2FAKey2', 'Mėgstu keliauti.', '1992-05-10', '+37060000002', 'Chrome', 'Moteris', 'Cis', 'Lietuva', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE, FALSE, 2),
('Mantas', 'Kazlauskas', 'mantas.k@example.com', 'm_kaz', 'pass123', '2FAkey3', 'Keliautojas iš širdies.', '1988-03-05', '+37060000003', 'Edge', 'Vyras', 'Cis', 'Lietuva', CURRENT_TIMESTAMP, NULL, CURRENT_TIMESTAMP, FALSE, FALSE, 3),
('Dovilė', 'Stankevičiūtė', 'dovile.s@example.com', 'dovi', 'pass456', '2FAkey4', 'Rašytoja ir menininkė.', '1995-07-22', '+37060000004', 'Chrome', 'Moteris', 'Cis', 'Lietuva', CURRENT_TIMESTAMP, NULL, CURRENT_TIMESTAMP, FALSE, FALSE, 4),
('Tomas', 'Urbonas', 'tomas.u@example.com', 'turbo', 'pass789', '2FAkey5', 'Sporto entuziastas.', '1985-12-01', '+37060000005', 'Firefox', 'Vyras', 'Cis', 'Lietuva', CURRENT_TIMESTAMP, NULL, CURRENT_TIMESTAMP, FALSE, FALSE, 5),
('Ieva', 'Vaitkutė', 'ieva.v@example.com', 'ieva_v', 'pass101', '2FAkey6', 'Myliu gamtą ir fotografiją.', '1993-04-19', '+37060000006', 'Safari', 'Moteris', 'Cis', 'Lietuva', CURRENT_TIMESTAMP, NULL, CURRENT_TIMESTAMP, FALSE, FALSE, 6),
('Rokas', 'Šimkus', 'rokas.s@example.com', 'rokas', 'pass202', '2FAkey7', 'Programuotojas dieną, muzikantas naktį.', '1990-09-15', '+37060000007', 'Brave', 'Vyras', 'Cis', 'Lietuva', CURRENT_TIMESTAMP, NULL, CURRENT_TIMESTAMP, FALSE, FALSE, 7),
('Gabija', 'Jankauskaitė', 'gabija.j@example.com', 'gabby', 'pass303', '2FAkey8', 'Gamta – mano aistra.', '1996-06-30', '+37060000008', 'Chrome', 'Moteris', 'Cis', 'Lietuva', CURRENT_TIMESTAMP, NULL, CURRENT_TIMESTAMP, FALSE, FALSE, 1),
('Justas', 'Žukauskas', 'justas.z@example.com', 'justis', 'pass404', '2FAkey9', 'IT studentas.', '1999-11-11', '+37060000009', 'Firefox', 'Vyras', 'Cis', 'Lietuva', CURRENT_TIMESTAMP, NULL, CURRENT_TIMESTAMP, FALSE, FALSE, 2),
('Greta', 'Kavaliauskaitė', 'greta.k@example.com', 'gkava', 'pass505', '2FAkey10', 'Savanorė ir keliautoja.', '1991-02-17', '+37060000010', 'Safari', 'Moteris', 'Cis', 'Lietuva', CURRENT_TIMESTAMP, NULL, CURRENT_TIMESTAMP, FALSE, FALSE, 3),
('Karolis', 'Daugirdas', 'karolis.d@example.com', 'karold', 'pass606', '2FAkey11', 'Rašau kodą ir tinklaraštį.', '1987-08-08', '+37060000011', 'Edge', 'Vyras', 'Cis', 'Lietuva', CURRENT_TIMESTAMP, NULL, CURRENT_TIMESTAMP, FALSE, FALSE, 4),
('Aistė', 'Petraitė', 'aiste.p@example.com', 'aiste', 'pass707', '2FAkey12', 'Tikiu minimalistiniu gyvenimo būdu.', '1994-01-01', '+37060000012', 'Brave', 'Moteris', 'Cis', 'Lietuva', CURRENT_TIMESTAMP, NULL, CURRENT_TIMESTAMP, FALSE, FALSE, 5);

/*
-- 3. POKALBIS (Conversation) - Independent
CREATE TABLE IF NOT EXISTS POKALBIS (
    id INT PRIMARY KEY,
    sukurimo_data TIMESTAMP NOT NULL,
    pavadinimas TEXT,
    aprasymas TEXT,
    atnaujinimo_data TIMESTAMP NOT NULL
);

-- 4. ZYME (Tag) - Independent
CREATE TABLE IF NOT EXISTS ZYME (
    id INT PRIMARY KEY,
    tekstas TEXT UNIQUE NOT NULL,
    sukurimo_data TIMESTAMP NOT NULL
);

-- 5. GALERIJA (Gallery) - Depends on NAUDOTOJAS (Creator FK)
CREATE TABLE IF NOT EXISTS GALERIJA (
    id INT PRIMARY KEY,
    pavadinimas TEXT NOT NULL,
    aprasymas TEXT,
    redagavimo_data TIMESTAMP,
    sukurimo_data TIMESTAMP NOT NULL,
    fono_spalva TEXT,
    naudotojas_id INT NOT NULL,
    FOREIGN KEY (naudotojas_id) REFERENCES NAUDOTOJAS(id)
);

-- 6. NUOTRAUKA (Photo) - Depends on GALERIJA (Container FK)
CREATE TABLE IF NOT EXISTS NUOTRAUKA (
    id INT PRIMARY KEY,
    pavadinimas TEXT NOT NULL,
    nuoroda TEXT NOT NULL,
    aprasymas TEXT,
    vietove TEXT,
    fotografijos_data TIMESTAMP,
    sukurimo_data TIMESTAMP NOT NULL,
    galerija_id INT NOT NULL,
    FOREIGN KEY (galerija_id) REFERENCES GALERIJA(id)
);

-- 7. IRASAS (Post) - Depends on NAUDOTOJAS (Creator FK)
CREATE TABLE IF NOT EXISTS IRASAS (
    id INT PRIMARY KEY,
    tekstas VARCHAR(50000) NOT NULL,
    teksto_sriftas TEXT, -- Based on enumeration (Roboto, Pacifico, Monoton)
    teksto_spalva TEXT,
    sukurimo_data TIMESTAMP NOT NULL,
    apsilankymu_skaicius INT DEFAULT 0,
    naudotojas_id INT NOT NULL,
    FOREIGN KEY (naudotojas_id) REFERENCES NAUDOTOJAS(id)
);

-- 8. NUOTRAUKOS_KOMENTARAS (Photo Comment) - Depends on NUOTRAUKA, NAUDOTOJAS
CREATE TABLE IF NOT EXISTS NUOTRAUKOS_KOMENTARAS (
    id INT PRIMARY KEY,
    tekstas VARCHAR(5000) NOT NULL,
    sukurimo_data TIMESTAMP NOT NULL,
    nuotrauka_id INT NOT NULL,
    naudotojas_id INT NOT NULL,
    FOREIGN KEY (nuotrauka_id) REFERENCES NUOTRAUKA(id),
    FOREIGN KEY (naudotojas_id) REFERENCES NAUDOTOJAS(id)
);

-- 9. ZINUTE (Message) - Depends on POKALBIS, NAUDOTOJAS
CREATE TABLE IF NOT EXISTS ZINUTE (
    id INT PRIMARY KEY,
    tekstas VARCHAR(5000) NOT NULL,
    ar_perskaityta BOOLEAN DEFAULT FALSE,
    sukurimo_data TIMESTAMP NOT NULL,
    redagavimo_data TIMESTAMP,
    pokalbis_id INT NOT NULL,
    naudotojas_id INT NOT NULL, -- The user who sent the message
    FOREIGN KEY (pokalbis_id) REFERENCES POKALBIS(id),
    FOREIGN KEY (naudotojas_id) REFERENCES NAUDOTOJAS(id)
);

-- 10. IRASO_KOMENTARAS (Post Comment) - Depends on IRASAS, NAUDOTOJAS
CREATE TABLE IF NOT EXISTS IRASO_KOMENTARAS (
    id INT PRIMARY KEY,
    tekstas VARCHAR(5000) NOT NULL,
    sukurimo_data TIMESTAMP NOT NULL,
    irasas_id INT NOT NULL,
    naudotojas_id INT NOT NULL,
    FOREIGN KEY (irasas_id) REFERENCES IRASAS(id),
    FOREIGN KEY (naudotojas_id) REFERENCES NAUDOTOJAS(id)
);

-- Bridge Tables for Many-to-Many relationships

-- 11. NAUDOTOJAS_POKALBIS (User-Conversation relationship)
CREATE TABLE IF NOT EXISTS NAUDOTOJAS_POKALBIS (
    naudotojas_id INT NOT NULL,
    pokalbis_id INT NOT NULL,
    PRIMARY KEY (naudotojas_id, pokalbis_id),
    FOREIGN KEY (naudotojas_id) REFERENCES NAUDOTOJAS(id),
    FOREIGN KEY (pokalbis_id) REFERENCES POKALBIS(id)
);

-- 12. IRASAS_ZYME (Post-Tag relationship)
CREATE TABLE IF NOT EXISTS IRASAS_ZYME (
    irasas_id INT NOT NULL,
    zyme_id INT NOT NULL,
    PRIMARY KEY (irasas_id, zyme_id),
    FOREIGN KEY (irasas_id) REFERENCES IRASAS(id),
    FOREIGN KEY (zyme_id) REFERENCES ZYME(id)
);







-- 3. POKALBIS
INSERT INTO POKALBIS (id, sukurimo_data, pavadinimas, aprasymas, atnaujinimo_data) VALUES
(1, CURRENT_TIMESTAMP, 'General Chat', 'Pokalbis apie viską.', CURRENT_TIMESTAMP);

-- 4. ZYME
INSERT INTO ZYME (id, tekstas, sukurimo_data) VALUES
(1, 'Fotografija', CURRENT_TIMESTAMP),
(2, 'Kelionės', CURRENT_TIMESTAMP),
(3, 'Gamta', CURRENT_TIMESTAMP);

-- 5. GALERIJA
INSERT INTO GALERIJA (id, pavadinimas, aprasymas, redagavimo_data, sukurimo_data, fono_spalva, naudotojas_id) VALUES
(1, 'Mano Pirmoji Galerija', 'Gamta ir kelionės.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, '#FFFFFF', 1);

-- 6. NUOTRAUKA
INSERT INTO NUOTRAUKA (id, pavadinimas, nuoroda, aprasymas, vietove, fotografijos_data, sukurimo_data, galerija_id) VALUES
(1, 'Saulėlydis', 'https://example.com/photo1.jpg', 'Gražus saulėlydis prie ežero.', 'Trakai', '2023-08-10 20:30:00', CURRENT_TIMESTAMP, 1),
(2, 'Kalnai', 'https://example.com/photo2.jpg', 'Kelionė į kalnus.', 'Alpės', '2023-07-15 10:00:00', CURRENT_TIMESTAMP, 1);

-- 7. IRASAS
INSERT INTO IRASAS (id, tekstas, teksto_sriftas, teksto_spalva, sukurimo_data, apsilankymu_skaicius, naudotojas_id) VALUES
(1, 'Tai yra mano pirmasis įrašas šiame tinklaraštyje.', 'Roboto', '#000000', CURRENT_TIMESTAMP, 15, 1),
(2, 'Pasidalinsiu savo kelionės įspūdžiais iš Italijos.', 'Pacifico', '#333333', CURRENT_TIMESTAMP, 25, 2);

-- 8. NUOTRAUKOS_KOMENTARAS
INSERT INTO NUOTRAUKOS_KOMENTARAS (id, tekstas, sukurimo_data, nuotrauka_id, naudotojas_id) VALUES
(1, 'Labai gražu!', CURRENT_TIMESTAMP, 1, 2),
(2, 'Kur tiksliai daryta ši nuotrauka?', CURRENT_TIMESTAMP, 2, 1);

-- 9. ZINUTE
INSERT INTO ZINUTE (id, tekstas, ar_perskaityta, sukurimo_data, redagavimo_data, pokalbis_id, naudotojas_id) VALUES
(1, 'Labas, kaip sekasi?', FALSE, CURRENT_TIMESTAMP, NULL, 1, 1),
(2, 'Viskas puiku, o tau?', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1, 2);

-- 10. IRASO_KOMENTARAS
INSERT INTO IRASO_KOMENTARAS (id, tekstas, sukurimo_data, irasas_id, naudotojas_id) VALUES
(1, 'Labai įdomus įrašas, ačiū!', CURRENT_TIMESTAMP, 1, 2),
(2, 'Lauksiu daugiau tokių pasidalijimų!', CURRENT_TIMESTAMP, 2, 1);

-- 11. NAUDOTOJAS_POKALBIS
INSERT INTO NAUDOTOJAS_POKALBIS (naudotojas_id, pokalbis_id) VALUES
(1, 1),
(2, 1);

-- 12. IRASAS_ZYME
INSERT INTO IRASAS_ZYME (irasas_id, zyme_id) VALUES
(1, 1),
(2, 2),
(2, 3);
*/
