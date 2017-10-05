from django_bootstrap import bootstrap
bootstrap()

import sys
import csv

from majors.models import Campus

def main():
	filename = sys.argv[1]
	counter = 0
	with open(filename) as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for items in reader:
			if len(items) != 5:
				continue

			product_name = items[0]
			product_desc = items[1]
			product_price = item[2]
			product_amount = items[3]
			product_pic = items[4]

			product = Product(name = product_name,desc = product_desc,price = product_price,amount = product_amount,pic = product_pic)
			product.save()
			counter += 1
	print('Imported',counter,'products')

if __name__ == '__main__':
	main()