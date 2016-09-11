import re
import urllib2
from csv import reader

from dateutil import parser
from django.core.management import BaseCommand

from properties.models import Property


class Command(BaseCommand):
    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--clear', default=None, action='store_true', help='Clear previous entries')
        parser.add_argument('--nostore', default=None, action='store_true', help='Clear previous entries')

    def handle(self, *args, **options):
        if options['clear']:
            Property.objects.all().delete()
        if not options['nostore']:
            self.read_data()

    def read_data(self):
        """

        :return:
        """
        url_month = "http://prod1.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-monthly-update.txt"
        url_all = "http://prod1.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-complete.txt"
        data = urllib2.urlopen(url_month)
        c = 0
        for line in reader(data):
            c += 1
            if line[-1] != 'D':  # if D skip as we have the latest data. We traverse newest change to oldest
                corrected = line[0:7] + ["%s %s" % (line[7], line[8])] + line[9:]
                obj = self.parse_object(corrected)
                Property.add(obj)
            if c % 10000 == 0:
                print('Wrote %ik lines' % (c / 1000))
            # if c == 300: break

    def parse_object(self, item):
        """

        :param item:
        :return:
        """
        result = {}
        item_ref = {
            1:  {'format': int, 'key': 'price'},
            2:  {'format': parser.parse, 'key': 'transfer_date'},
            3:  {'format': str, 'key': 'post_code'},
            4:  {'format': str, 'key': 'property_type'},
            5:  {'format': str, 'key': 'age'},
            6:  {'format': str, 'key': 'duration'},
            7:  {'format': str, 'key': 'paon_saon'},
            8:  {'format': str, 'key': 'street'},
            9:  {'format': str, 'key': 'locality'},
            10: {'format': str, 'key': 'town'},
            11: {'format': str, 'key': 'district'},
            12: {'format': str, 'key': 'county'},
            13: {'format': str, 'key': 'ppd'},
            14: {'format': str, 'key': 'type_of_update'},
        }
        for ind in item_ref:
            key = item_ref[ind]['key']
            formater = item_ref[ind]['format']
            result[key] = formater(item[ind])
        # print result
        # print ""
        return result

  # 0Transaction unique identifier         1Price       2Date of Transfer    3Postcode   4Type  5Old/New6Durat  7PAON / SAON                                           8Street         9Locality          10Town/City      11District               12County              13PPD    Record Status
['{7696BA9F-BB3E-4A2B-9671-D39DB8EF9105}', '179150',    '2006-09-15 00:00', '"BN2 3LQ"', '"F"', '"N"', '"L"', '"34"',                    '""',                       '"SHANKLIN ROAD"',  '""',           '"BRIGHTON"',   '"BRIGHTON AND HOVE"',  '"BRIGHTON AND HOVE"',  '"A"', '"C"']
['{29ADD55C-CC72-4BDE-8E2B-CCCD0ADA3BBA}', '73000',     '2006-08-10 00:00', '"S9 1LD"',  '"F"', '"Y"', '"L"', '"CENTURION APARTMENTS',   ' 30"', '"APARTMENT 1"',    '"VAUXHALL ROAD"',  '""',           '"SHEFFIELD"',  '"SHEFFIELD"',          '"SOUTH YORKSHIRE"',    '"A"', '"C"']