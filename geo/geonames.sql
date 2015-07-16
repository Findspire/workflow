CREATE TABLE geonames(
       geonameid INTEGER PRIMARY KEY,
       name TEXT,
       asciiname TEXT,
       alternatenames TEXT,
       latitude REAL,
       longitude REAL,
       feature_class TEXT,
       feature_code TEXT,
       country_code TEXT,
       cc2 TEXT,
       admin1_code TEXT,
       admin2_code TEXT,
       admin3_code TEXT,
       admin4_code TEXT,
       population INTEGER,
       elevation INTEGER,
       dem INTEGER,
       timezone TEXT,
       modification_date TEXT
);
CREATE INDEX idx_gn_feature_class ON geonames(feature_class);
CREATE INDEX idx_gn_country_code ON geonames(country_code);
CREATE INDEX idx_gn_admin1_code ON geonames(admin1_code);

CREATE TABLE alternate_names(
       alternatenameid INTEGER PRIMARY KEY,
       geonameid INTEGER,
       iso_language TEXT,
       alternate_name TEXT,
       is_preferred_name INT,
       is_short_name INT,
       is_colloquial INT,
       is_historic INT,
       FOREIGN KEY(geonameid) REFERENCES geonames(geonameid)
);
CREATE INDEX idx_an_idlang ON alternate_names(geonameid, iso_language);

CREATE TABLE countries(
       iso2 TEXT PRIMARY KEY,
       iso3 TEXT,
       iso_num NUMERIC,
       fips_code TEXT,
       name TEXT,
       capital TEXT,
       area REAL,
       population INT,
       continent TEXT,
       tld TEXT,
       currency_code TEXT,
       currency_name TEXT,
       phone TEXT,
       postalcode TEXT,
       postalcode_regex TEXT,
       languages TEXT,
       geonameid INTEGER,
       neighbors TEXT,
       equiv_fips_code TEXT,
       FOREIGN KEY(geonameid) REFERENCES geonames(geonameid)
);
CREATE INDEX idx_c_iso2 ON countries(iso2);

-- Local Variables:
-- sql-product: sqlite
-- End:
