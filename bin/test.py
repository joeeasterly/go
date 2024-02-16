from go.bin.lib_date import get_mongodb_date_as_string
from pymongo import *
from connect_mungo import connect_mungo
from datetime import datetime
from dateparser import parse
from lib_mungo import get_record_by_identifier
from pprint import pprint
collection = connect_mungo()
record = get_record_by_identifier("qztp")
pprint(record)
print(get_mongodb_date_as_string(record, "expires"))