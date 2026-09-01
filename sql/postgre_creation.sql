DROP TABLE IF EXISTS marques;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS produits;
DROP TABLE IF EXISTS produits_categories;

-- ============================================
-- Table: marques
-- ============================================
CREATE TABLE marques (
    id      BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nom     VARCHAR(255) NOT NULL
);

-- ============================================
-- Table: categories
-- ============================================
CREATE TABLE categories (
    id      BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nom     VARCHAR(255) NOT NULL,

    CONSTRAINT uq_nom_categories
        UNIQUE (nom)
);

-- ============================================
-- Table: produits
-- ============================================
CREATE TABLE produits (
    code            BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    marque_id       BIGINT NOT NULL,
    nom             VARCHAR(255) NOT NULL,
    fiber           SMALLINT,
    proteins        SMALLINT,
    energy          SMALLINT,
    saturated_fat   SMALLINT,
    sugars          SMALLINT,
    salt            SMALLINT,

    CONSTRAINT fk_marques
        FOREIGN KEY (marque_id)
        REFERENCES marques (id)
);

-- ============================================
-- Table: produits_categories (table d'association)
-- ============================================
CREATE TABLE produits_categories (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    categorie_id    BIGINT NOT NULL,
    produit_id      BIGINT NOT NULL,

    CONSTRAINT fk_categories
        FOREIGN KEY (categorie_id)
        REFERENCES categories (id),

    CONSTRAINT fk_produits
        FOREIGN KEY (produit_id)
        REFERENCES produits (code)
);