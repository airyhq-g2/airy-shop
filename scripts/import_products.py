from django_bootstrap import bootstrap

bootstrap()

from urllib import request, error
import csv, os
from main.models import Product

def main():
    os.makedirs('imgs')
    Product.objects.all().delete()
    with open('./scripts/condoms.csv') as csv_file:
        csv_content = csv.reader(csv_file, delimiter=',')
        counter = 0
        for row in csv_content:
            img_url = row[3]
            img_type = img_url.split('.')[-1]
            img_dest = './media/imgs/product_img{0}.{1}'.format(counter, img_type)
            try:
                request.urlretrieve(img_url, img_dest)
            except error.HTTPError as e:
                print(counter, e)
            product = Product.objects.create(
                name=row[0],
                desc=row[1],
                price=row[2],
                amount=50,
                pic= ('/imgs/product_img{0}.{1}'.format(counter, img_type))
            )
            product.save()
            counter += 1

    print(Product.objects.all())


if __name__ == '__main__':
    main()
