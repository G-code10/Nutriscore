DROP TABLE IF EXISTS brands CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS products_categories CASCADE;
DROP TABLE IF EXISTS nutriments CASCADE;
 
-- ============================================
-- Table: brands
-- ============================================
CREATE TABLE brands (
    id      BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name    TEXT NOT NULL,
 
    CONSTRAINT uq_name_brands
        UNIQUE (name)
);
 
-- ============================================
-- Table: categories
-- ============================================
CREATE TABLE categories (
    id      BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name    TEXT NOT NULL,
    main    BOOLEAN NOT NULL,
 
    CONSTRAINT uq_name_categories
        UNIQUE (name)
);
 
-- ============================================
-- Table: products
-- ============================================
CREATE TABLE products (
    code                TEXT PRIMARY KEY,
    brand_id            BIGINT,
    brand               TEXT,
    name                TEXT NOT NULL,
    nutriscore_grade    VARCHAR(1)
);
 
-- ============================================
-- Table: products_categories (table d'association)
-- ============================================
CREATE TABLE products_categories (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    category_id     BIGINT NOT NULL,
    product_id      TEXT  NOT NULL,
 
    CONSTRAINT fk_categories
        FOREIGN KEY (category_id)
        REFERENCES categories (id),
 
        UNIQUE (product_id, category_id)
    --     ,
 
    -- CONSTRAINT fk_products
    --     FOREIGN KEY (product_id)
    --     REFERENCES products (code)
);
 
-- ============================================
-- Table: nutriments (table d'association)
-- ============================================
-- energy-kcal_100g, fat_100g, saturated-fat_100g, carbohydrates_100g, sugars_100g, fiber_100g, proteins_100g, salt_100g
CREATE TABLE nutriments (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id      TEXT NOT NULL UNIQUE,
    energy          FLOAT,
    energy_u        VARCHAR(10),
    fat             FLOAT,
    fat_u           VARCHAR(10),
    saturated_fat   FLOAT,
    saturated_fat_u VARCHAR(10),
    carbohydrates   FLOAT,
    carbohydrates_u VARCHAR(10),
    sugars          FLOAT,
    sugars_u        VARCHAR(10),
    fiber           FLOAT,
    fiber_u         VARCHAR(10),
    proteins        FLOAT,
    proteins_u      VARCHAR(10),
    salt            FLOAT,
    salt_u          VARCHAR(10),
 
    UNIQUE (product_id),
 
    CONSTRAINT fk_products
        FOREIGN KEY (product_id)
        REFERENCES products (code),
    
    CONSTRAINT ck_energy_kcal   CHECK (energy BETWEEN 0 AND 950),
    CONSTRAINT ck_fat           CHECK (fat BETWEEN 0 AND 100),
    CONSTRAINT ck_saturated_fat CHECK (saturated_fat BETWEEN 0 AND 100),
    CONSTRAINT ck_carbohydrates CHECK (carbohydrates BETWEEN 0 AND 100),
    CONSTRAINT ck_sugars        CHECK (sugars BETWEEN 0 AND 100),
    CONSTRAINT ck_fiber         CHECK (fiber BETWEEN 0 AND 100),
    CONSTRAINT ck_proteins      CHECK (proteins BETWEEN 0 AND 100),
    CONSTRAINT ck_salt          CHECK (salt BETWEEN 0 AND 100)
);