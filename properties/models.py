from __future__ import unicode_literals

import ast

from django.core import serializers
from django.db import models, transaction
from django.db.models import Min, Max
from django.utils.functional import cached_property


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
        p_params = dict(params)
        price    = p_params.pop('price')
        tdate    = p_params.pop('transfer_date')
        tid      = p_params.pop('tid')
        if item:
            # update any parameters that might have changed
            for key in params:
                if getattr(item, key) != p_params.get(key):
                    setattr(item, key, p_params.get(key))
            item.save()
            t = Transaction(price=price, transfer_date=tdate, abode=item, tid=tid)
            t.save()

    @staticmethod
    @transaction.atomic
    def add(params):
        """
        Adds a new property
        :param params:
        """
        previous = Property.objects.filter(postcode=params.get('postcode'),
                                           paon_saon=params.get('paon_saon'),
                                           street=params.get('street')).first()

        p_params = dict(params)
        price    = p_params.pop('price')
        tdate    = p_params.pop('transfer_date')
        tid      = p_params.pop('tid')
        if previous:  # add transaction
            t = Transaction(price=price, transfer_date=tdate, abode=previous, tid=tid)
            t.save()
        else:         # add new property and transaction
            p = Property(**p_params)
            p.save()
            t = Transaction(price=price, transfer_date=tdate, abode=p, tid=tid)
            t.save()

    @staticmethod
    def list_filtered(postcode, dateranges):
        """

        :param postcode:
        :param dateranges:
        :return:
        """
        result = []
        low = dateranges['min']
        high = dateranges['max']
        props = Property.objects.prefetch_related('transactions').filter(postcode__startswith=postcode,
                                                                         transactions__transfer_date__range=[low, high])
        for p in props:
            # print p.to_json()['postcode'], p.to_json()['paon_saon'], p.to_json()['street']
            # prop_tr = Transaction.objects.filter(abode=p, transfer_date__range=[low, high])
            prop_tr = p.transactions.filter(transfer_date__range=[low, high])
            result.append(p.to_json(prop_tr))
        return result

    def to_json(self, transactions=None):
        """
        Serializes the item as a dictionary
        :return: {dict}
        """
        result = serializers.serialize('json', [self, ])
        result = ast.literal_eval(result)[0]['fields']
        transactions = transactions if transactions else self.transactions.all()
        result['transactions'] = [i.to_json() for i in transactions]
        return result


class Transaction(models.Model):
    tid             = models.CharField(null=False, max_length=200, default='', unique=True)  # don't index because of the scope of this project we won't look according to tid
    price           = models.IntegerField(null=False)
    transfer_date   = models.DateField(null=False, db_index=True)
    abode           = models.ForeignKey('Property', related_name='transactions')

    @staticmethod
    def update(params):
        tid = params.get('tid', None)
        tc = params.get('type_of_transaction')
        if tid:
            trans = Transaction.objects.filter(tid=tid).first()
            if trans:
                if tc == 'C':
                    for key in ['price', 'transfer_date']:
                        if params.get(key, None):
                            setattr(tc, key, params.get(key))
                    tc.save()
                if tc == 'D':
                    tc.delete()

    # @cached_property
    @staticmethod
    def date_limits():
        return [
            Transaction.objects.all().aggregate(Min('transfer_date'))["transfer_date__min"].strftime('%Y-%m-%d'),
            Transaction.objects.all().aggregate(Max('transfer_date'))["transfer_date__max"].strftime('%Y-%m-%d')]

    def to_json(self, verbose=False):
        """
        Serializes the item as a dictionary
        :return: {dict}
        """
        result = serializers.serialize('json', [self, ])
        result = ast.literal_eval(result)[0]['fields']
        result.pop('abode')
        if not verbose:
            result.pop('tid')
        return result
