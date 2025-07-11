import re
import urllib2
from csv import reader

from dateutil import parser
from django.core.management import BaseCommand

from properties.models import Property, Transaction


class Command(BaseCommand):
    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--clear', default=None, action='store_true', help='Clear previous entries')
        parser.add_argument('--nostore', default=None, action='store_true', help='Clear previous entries')
        parser.add_argument('--large', default=None, action='store_true', help='Use large dataset (3.5GB)')

    def handle(self, *args, **options):
        if options['clear']:
            Property.objects.all().delete()
            Transaction.objects.all().delete()
        if not options['nostore']:
            self.read_data(large=options['large'])

    def read_data(self, large=False):
        """
        Reads the data from the land registry and then adds them to the database
        :param large: Use the large dataset
        """
        url_month = "http://prod1.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-monthly-update.txt"
        url_2016 = "http://prod1.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-2016.txt"
        url_all = "http://prod1.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-complete.txt"
        data = urllib2.urlopen(url_all if large else url_2016)
        c = 0
        for line in reader(data):
            c += 1
            corrected = line[0:7] + ["%s %s" % (line[7], line[8])] + line[9:]
            obj = self.parse_object(corrected)
            Property.add(obj)   # this needs Postgres' bulk import
                                # check here https://docs.djangoproject.com/en/dev/ref/models/querysets/#django.db.models.query.QuerySet.bulk_create
            if c % 10000 == 0:
                print('Wrote %ik lines' % (c / 1000))
            # if c == 300: break
        print 'Total %i' % c

    def parse_object(self, item):
        """
        Accepts an item that was read from the land registry and parses it as a dict
        :param item: The transaction from the land register
        :return: {dict}
        """
        result = {}

        def fix_id(id_str):
            return re.sub("[{}]", "", id_str)

        item_ref = {
            0:  {'format': fix_id, 'key': 'tid'},
            1:  {'format': int, 'key': 'price'},
            2:  {'format': parser.parse, 'key': 'transfer_date'},
            3:  {'format': str, 'key': 'postcode'},
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
        }
        for ind in item_ref:
            key = item_ref[ind]['key']
            formater = item_ref[ind]['format']
            result[key] = formater(item[ind])
        return result
