#!/usr/bin/env python

"exclude marked patients from train and test"

import pandas as pd

train_file = 'data/orig/patients_train.csv'
train_exclude_file = 'data/orig/train_patients_to_exclude.csv'
train_output_file = 'data/train.csv'

test_file = 'data/orig/patients_test.csv'
test_exclude_file = 'data/orig/test_patients_to_exclude.csv'
test_output_file = 'data/test.csv'

#

train = pd.read_csv( train_file )
train_exclude = pd.read_csv( train_exclude_file, header = None, names = [ 'patient_id' ] )

train.drop( 'patient_gender', axis = 1, inplace = True )
train_new = train[ ~train.patient_id.isin( train_exclude.patient_id ) ]

print "train - before: {}, after: {}".format( len( train ), len( train_new ))

train_new.to_csv( train_output_file, index = None )

#

test = pd.read_csv( test_file )
test_exclude = pd.read_csv( test_exclude_file, header = None, names = [ 'patient_id' ] )

test.drop( 'patient_gender', axis = 1, inplace = True )
test_new = test[ ~test.patient_id.isin( test_exclude.patient_id ) ]

print "test - before: {}, after: {}".format( len( test ), len( test_new ))

test_new.to_csv( test_output_file, index = None )

"""
train - before: 1476637, after: 1157817
test - before: 2169045, after: 1701813
"""
