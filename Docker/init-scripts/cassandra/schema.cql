CREATE KEYSPACE IF NOT EXISTS wine_catalog 
WITH replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 3 // Adjust replication factor based on your cluster setup
};

USE wine_catalog;

CREATE TABLE IF NOT EXISTS wine (
    article text,
    name text,
    type text,
    country text,
    region text,
    vintage_dating int,
    winery text,
    alcohol double,
    capacity double,
    description text,
    price double,
    items_left int,
    PRIMARY KEY (article) // Assuming 'article' is unique. Adjust the primary key as needed.
) WITH comment='Validation of wine collection';

// Inserting the first record
INSERT INTO wine_catalog.wine (article, name, type, country, region, vintage_dating, winery, alcohol, capacity, description, price, items_left)
VALUES ('137816', 'Anno Domini Cabernet Franc', 'Red Unfortified still wines', 'Italy', 'I.G.T./D.O.C. Veneto', 2019, 'Anno Domini Vineyards', 12.5, 0.75, 'Varieties: Cabernet\nFrancAllergens: Contains sulfites', 6.85, 50);

// Inserting the second record
INSERT INTO wine_catalog.wine (article, name, type, country, region, vintage_dating, winery, alcohol, capacity, description, price, items_left)
VALUES ('829044', 'Vi de Vila Cims de Porrera', 'Red Unfortified still wines', 'Spain', 'D.O.Q. Priorat', 2017, 'Cims De Porrera', 15, 0.75, 'Varieties: Carinyena / Mazuelo, Garnatxa\nNegraAllergens: Contains sulfites', 17.44, 50);
