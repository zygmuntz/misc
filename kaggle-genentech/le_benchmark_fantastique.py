#!/usr/bin/env python

"This script scores 0.66 on the public leaderboard"

import numpy as np
import pandas as pd

train_file = 'data/orig/patients_train.csv'
test_file = 'data/orig/patients_test.csv'
output_file = 'data/predictions.csv'

#

train = pd.read_csv( train_file )
test = pd.read_csv( test_file )

train.drop( 'patient_gender', axis = 1, inplace = True )
test.drop( 'patient_gender', axis = 1, inplace = True )

# validation AUC: 69.92% without backup
# validation AUC: 69.95% with backup
group_cols = [ 'patient_age_group', 'patient_state', 'ethinicity', 'household_income', 'education_level' ]
backup_cols = [ 'patient_age_group', 'ethinicity', 'household_income', 'education_level' ]

means = train.groupby( group_cols )['is_screener'].mean()
means = means.reset_index()

backup_means = train.groupby( backup_cols )['is_screener'].mean()
backup_means = backup_means.reset_index()

pred = pd.merge( test, means, on = group_cols, how = 'left' )
backup_pred = pd.merge( test, backup_means, on = backup_cols, how = 'left' )

print "# {} NaNs in test".format( pred.is_screener.isnull().sum())

i_null = pred.is_screener.isnull()
pred.loc[ i_null, 'is_screener' ] = backup_pred.loc[ i_null, 'is_screener' ]

print "# {} NaNs in test after merging backup".format( pred.is_screener.isnull().sum())

i_null = pred.is_screener.isnull()
pred.loc[ i_null, 'is_screener' ] = train.is_screener.mean()

assert( pred.is_screener.isnull().sum() == 0 )

print "saving..."

pred[[ 'patient_id', 'is_screener' ]].to_csv( output_file, index = None, 
	header = ( 'patient_id', 'predict_screener' ))
