from __future__ import unicode_literals

import ast

from django.core import serializers
from django.db import models, transaction, connection
from dateutil import parser
from django.db.models import Count


class Property(models.Model):
    class Meta:
        unique_together = ('postcode', 'paon_saon', 'street')
    PROPERTY_TYPE = (
        ('D', 'Detached'),
        ('S', 'Semi - Detached'),
        ('T', 'Terraced'),
        ('F', 'Flats / Maisonettes'),
        ('O', 'Other'),
    )
    AGE          = (('Y', 'Yearly new built'), ('N', 'Established residential building'))
    DURATION     = (('F', 'Freehold'), ('N', 'Leasehold'))
    PPD_CATEGORY = (('A', 'Standard price paid'), ('B', 'Additional price paid'))

    postcode       = models.CharField(null=False, max_length=20, db_index=True)
    property_type   = models.CharField(null=False, max_length=1,  choices=PROPERTY_TYPE)
    age             = models.CharField(null=False, max_length=1,  choices=AGE)
    duration        = models.CharField(null=False, max_length=1,  choices=DURATION)
    ppd             = models.CharField(null=False, max_length=1,  choices=PPD_CATEGORY)
    paon_saon       = models.CharField(null=False, max_length=200)
    street          = models.CharField(null=False, max_length=200)
    locality        = models.CharField(null=False, max_length=200)
    town            = models.CharField(null=False, max_length=200)
    district        = models.CharField(null=False, max_length=200)
    county          = models.CharField(null=False, max_length=200)

    @staticmethod
    def update(params):
        """
        Updates the property.
        :param params:
        """
        item = Property.objects.filter(postcode=params.get('postcode'),
                                       paon_saon=params.get('paon_saon'),
                                       street=params.get('street')).first()
        if item:
            for key in params:
                if getattr(item, key) != params.get(key):
                    setattr(item, key, params.get(key))
            item.save()

    @staticmethod
    @transaction.atomic
    def add(params):
        """
        Adds a new property
        :param params:
        """
        item = Property.objects.filter(postcode=params.get('postcode'),
                                       paon_saon=params.get('paon_saon'),
                                       street=params.get('street')).first()

        p_params = dict(params)
        price = p_params.pop('price')
        tdate = p_params.pop('transfer_date')
        type_of_update = p_params.pop('type_of_update')
        if item:
            last_update = item.transactions.order_by('-transaction_id').first()
            if last_update:
                if last_update.type_of_update == 'C' and type_of_update == 'A':
                    # Since we go from newest to oldest data the change has been registered
                    last_update.type_of_update = 'E'
                    last_update.save()
                else:
                    tid = last_update.transaction_id + 1
                    t = Transaction(price=price, transfer_date=tdate, abode=item, transaction_id=tid,
                                    type_of_update=type_of_update)
                    t.save()
        else:
            p = Property(**p_params)
            p.save()
            t = Transaction(price=price, transfer_date=tdate, abode=p, transaction_id=1, type_of_update=type_of_update)
            t.save()

    @staticmethod
    def list_filtered(postcode, dateranges):
        result = []
        low = dateranges['min']
        high = dateranges['max']
        props = Property.objects.prefetch_related('transactions').filter(postcode=postcode).filter(transactions__transfer_date__range=[low, high])
        for p in props:
            filtered_transactions = Transaction.objects.filter(abode=p, transfer_date__range=[low, high])
            result.append(p.to_json(filtered_transactions))
        return result

    def to_json(self, transactions=None):
        """
        Serializes the item as a dictionary
        :return: {dict}
        """
        result = serializers.serialize('json', [self, ])
        result = ast.literal_eval(result)[0]['fields']
        if transactions:
            result['transactions'] = [i.to_json() for i in transactions]
        else:
            result['transactions'] = [i.to_json() for i in self.transactions.all()]
        return result


class Transaction(models.Model):
    UPDATE          = (('C', 'Change'), ('A', 'New sale'), ('E', 'Change evaluated'))

    price           = models.IntegerField(null=False)
    transfer_date   = models.DateField(null=False, db_index=True)
    abode           = models.ForeignKey('Property', related_name='transactions')

    # we need these because of the way we read the data (newest to oldest). If it is C then the next A should be avoided
    transaction_id  = models.IntegerField(null=False)
    type_of_update  = models.CharField(null=False, max_length=1,  choices=UPDATE)

    def to_json(self):
        """
        Serializes the item as a dictionary
        :return: {dict}
        """
        result = serializers.serialize('json', [self, ])
        result = ast.literal_eval(result)[0]['fields']
        result.pop('abode')
        return result
