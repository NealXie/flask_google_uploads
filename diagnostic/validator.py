import sys
import os
import argparse
import csv
from csvvalidator import *

def create_validator():
	
	field_names = (
					'Brand',
					'Date',
					'Campaign Start Date',
					'Campaign End Date',
					'Publisher',
					'Campaign Name',
					'DCM Campaign ID',
					'Creative Name',
					'Consumer Target (Age)',
					'Consumer Target (Gender)',
					'Consumer Target (Ethnicity)',
					'Placement Name',
					'DCM Placement ID',
					'Placement Type',
	 				'Unit Size',
					'Planned Impressions',
					'Delivered Impressions',
					'Delivered Unique Impressions',
					'Frequency',
					'Delivered Clicks',
					'CTR',
					'% Viewable Impressions',
					'Click to Play or Autoplay',
					'Video Views - Total',
					'Video Views - First Quartile',
					'Video Views - Mid Quartile',
					'Video Views - Third Quartile',
					'Video Views - Completions',
					'VCR',
					'Cost Method',
					'Placement Rate',
					'Delivered Spend'
					)

	validator = CSVValidator(field_names)

	# basic header and record length check
	validator.add_header_check('EX1' , 'Bad Header')
	validator.add_record_length_check('EX2', 'Unexpected Recoed Length')

	# some simple value checks
	validator.add_value_check('Brand', str, 'EX3', 'Invalid Brand')
	validator.add_value_check('Date', datetime_string('%Y-%m-%d'), 'EX4', 'Invalid Date')
	validator.add_value_check('Campaign Start Date', datetime_string('%Y-%m-%d'), 'EX5', 'Invalid Campaign Start Date')
	validator.add_value_check('Campaign End Date', datetime_string('%Y-%m-%d'), 'EX6', 'Invalid Campaign End Date')
	validator.add_value_check('Publisher', str, 'EX7', 'Invalid Publisher')
	validator.add_value_check('Campaign Name', str, 'EX8', 'Campaign Name')
	validator.add_value_check('DCM Campaign ID', int, 'EX9', 'Invalid DCM Campaign ID')
	validator.add_value_check('Creative Name', str, 'EX10', 'Invalid Creative Name')
	validator.add_value_check('Consumer Target (Age)', str, 'EX11', 'Invalid Consumer Target (Age)')
	validator.add_value_check('Consumer Target (Gender)', str, 'EX12', 'Invalid Consumer Target (Gender)')
	validator.add_value_check('Consumer Target (Ethnicity)', str, 'EX13', 'Invalid Consumer Target (Ethnicity)')
	validator.add_value_check('Placement Name', str, 'EX14', 'Invalid Placement Name')
	validator.add_value_check('DCM Placement ID', int, 'EX15', 'Invalid DCM Placement ID')
	validator.add_value_check('Placement Type', str, 'EX16', 'Invalid Placement Type')
	validator.add_value_check('Unit Size', float, 'EX17', 'Invalid Unit Size')
	validator.add_value_check('Planned Impressions', int, 'EX18', 'Invalid Planned Impressions')
	validator.add_value_check('Delivered Impressions', int, 'EX19', 'Invalid Delivered Impressions')
	validator.add_value_check('Delivered Unique Impressions', int, 'EX20', 'Invalid Planned Unique Impressions')
	validator.add_value_check('Frequency', float, 'EX21', 'Invalid Frequency')
	validator.add_value_check('Delivered Clicks', int, 'EX22', 'Invalid Delivered Clicks')
	validator.add_value_check('CTR', float, 'EX23', 'Invalid CTR')
	validator.add_value_check('% Viewable Impressions', float, 'EX24', '% Viewable Impressions')
	validator.add_value_check('Click to Play or Autoplay', str, 'EX25', 'Invalid Click to Play or Autoplay')
	validator.add_value_check('Video Views - Total', int, 'EX26', 'Invalid Video Views - Total')
	validator.add_value_check('Video Views - First Quartile', int, 'EX27', 'Invalid Video Views - First Quartile')
	validator.add_value_check('Video Views - Mid Quartile', int, 'EX28', 'Invalid Video Views - Mid Quartile')
	validator.add_value_check('Video Views - Third Quartile', int, 'EX29', 'Invalid Video Views - Third Quartile')
	validator.add_value_check('Video Views - Completions', int, 'EX30', 'Invalid Video Views - Completions')
	validator.add_value_check('VCR', float, 'EX31', 'Invalid VCR')
	validator.add_value_check('Cost Method', str, 'EX32', 'Invalid Cost Method')
	validator.add_value_check('Placement Rate', float, 'EX33', 'Invalid Placement Rate')
	validator.add_value_check('Delivered Spend', float, 'EX34', 'Invalid Delivered Spend')

	return validator

def main():

	description = 'Validate a CSV data file.'
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument('file', metavar='FILE', help='a file to be validated')
	parser.add_argument('-l', '--limit', dest='limit', type=int, action='store', default=0, help='limit the number of problems reported')
	parser.add_argument('-s', '--summarize', dest='summarize', action='store_true', default=False, help='output only a summary of the different types of problem found')
	parser.add_argument('-e', '--report-unexpected-exceptions', dest='report_unexpected_exceptions', action='store_true', default=False, help='report any unexpected exceptions as problems')

	args = parser.parse_args()

	if not os.path.isfile(args.file):
		print('%s is not a file' % args.file)
		sys.exit()

	with open(args.file, 'r') as f:

		data = csv.reader(f, delimiter='\t')

		validator = create_validator()

		problems = validator.validate(data, summarize=args.summarize, report_unexpected_exceptions=args.report_unexpected_exceptions, context={'file': args.file})

		write_problems(problems, sys.stdout, summarize=args.summarize, limit=args.limit)

		if problems:
			sys.exit(1)
		else:
			sys.exit(0)

if __name__ == "__main__":
	main()