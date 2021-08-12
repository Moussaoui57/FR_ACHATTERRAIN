## How to launch a spider
 - Create a virtualEnv Python2.7 
 - Install all libraries that exists in the file `requirements.txt`
 - Launch `list_ads.py`
 - Launch `ACHATTERRAIN.py`
 - Drop all duplicated rows based on field ID_CLIENT

<hr>

## Follow this steps

- Install libraries in VirtualEnv
```
pip install -r requirements.txt
```

- Launch a spider `list_ads.py` in Screen
``` 
scrapy crawl name_of_spider -o name_file_links.txt
```
- Modify the script `ACHATTERRAIN.py` with the new file name `name_file_links.txt`
```
f = open('/home/name_of_user/SELOGER_ACHATTERRAIN/FR_ACHATTERRAIN/spiders/name_file_links.txt', 'r')
```

- Launch a spider `ACHATTERRAIN.py` in Screen
``` 
scrapy crawl name_of_spider -o name_file_csv.csv
```

- Drop duplicate
```
sort -u -k3,3 -t";" name_file_csv.csv > file_without_dup.csv
```
# FR_ACHATTERRAIN

