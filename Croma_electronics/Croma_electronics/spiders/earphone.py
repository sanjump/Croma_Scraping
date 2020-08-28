import scrapy,random,string
from ..items import CromaElectronicsItem

class CromaSpider(scrapy.Spider):

    name = 'cromaearphone'

    pageno=2

    start_urls=['https://www.croma.com/audio-video/headphones-earphones/c/1012?q=%3Arelevance%3AskuStockFlag%3Atrue&page=1']

    def parse(self, response):


        page = response.css("a.product__list--thumb::attr(href)").getall()

        for p in page:

             url = 'https://www.croma.com' + p
             yield scrapy.Request(url, callback=self.parse_elec)

        page = 'https://www.croma.com/audio-video/headphones-earphones/c/1012?q=%3Arelevance%3AskuStockFlag%3Atrue&page='+ str(CromaSpider.pageno)
        if CromaSpider.pageno <=5:
            CromaSpider.pageno += 1
            yield response.follow(page, callback=self.parse)


    def parse_elec(self, response):

        items = CromaElectronicsItem()

        product_name = response.css('h1::text').get()

        storeprice = response.css('.pdpPrice::text').get()

        storeLink = response.url


        photos = response.css('img._pdp_im::attr(src)').extract()

        spec_title = response.css(".attrib::text").extract()

        spec_detail = response.css(".attribvalue::text").extract()

        product_id = ''.join(random.sample(string.ascii_lowercase + string.digits, 20))

        rating = response.css('#finalReviewRating::text').get()

        id = storeLink[::-1].find('/')

        #reviews = response.css('#defaultReviewsCard p::text').extract()

        stores = {

            "rating": rating,
            "reviews": [],
            'storeproductid': storeLink[-id:],
            "storeLink": storeLink,
            "storeName": "Croma",
            "storePrice": storeprice[1:]

        }

        items['product_name'] = product_name.strip()
        items['product_id'] = product_id
        items['stores'] = stores
        items['category'] = 'electronics'
        items['subcategory'] = 'earphones'
        items['brand'] = product_name.split()[0]
        items['description'] = {}

        for i in range(len(spec_title)):
            items['description'][spec_title[i].strip()] = spec_detail[i].strip()

        items['photos'] = photos

        yield items