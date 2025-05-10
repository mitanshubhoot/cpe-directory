-- schema.sql

DROP TABLE IF EXISTS cpe;

CREATE TABLE cpe (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cpe_title TEXT,
    cpe_22_uri TEXT,
    cpe_23_uri TEXT,
    reference_links TEXT, -- JSON string
    cpe_22_deprecation_date TEXT,
    cpe_23_deprecation_date TEXT
);
