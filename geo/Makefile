CLDR_VERSION = 24

all: cldr/README geonames.db

cldr/%.zip:
	@mkdir -p cldr
	wget -nv -c -O $@ http://unicode.org/Public/cldr/$(CLDR_VERSION)/$(@F)

cldr/%: cldr/json.zip
	unzip -q -d cldr/ $^

geonames/countryInfo.txt:
	@mkdir -p geonames
	wget -nv -c -O $@ http://download.geonames.org/export/dump/$(@F)

geonames/%.zip:
	@mkdir -p geonames
	wget -nv -c -O $@ http://download.geonames.org/export/dump/$(@F)

geonames/%.txt: geonames/%.zip
	unzip -q -d geonames/ $^

geonames.db: geonames/allCountries.txt geonames/alternateNames.txt geonames/countryInfo.txt
	sqlite3 $@ < geonames.sql
	./import_sql.py

.PHONY: clean
clean:
	rm -rf cldr geonames geonames.db
