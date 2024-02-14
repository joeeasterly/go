from get_mongodb_date_as_string import get_mongodb_date_as_string
from pymongo import *
from connect_mungo import connect_mungo
from datetime import datetime
from dateparser import parse
from .get_record_by_identifier import get_record_by_identifier
collection = connect_mungo()
record = get_record_by_identifier("qztp")
print (get_mongodb_date_as_string(record, "expires"))