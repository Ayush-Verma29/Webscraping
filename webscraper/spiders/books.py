import scrapy 


class bookspider(scrapy.Spider):
    name='books'
    start_urls=['https://books.toscrape.com/']

    def parse(self,response):
        books=response.css('article.product_pod')
        for book in books:
            try: 
                yield{
                    'name': book.css('h3 a::text').get(),
                    'price': book.css('.product_price .price_color::text').get().replace('£',''),
                    'rating':book.css('p').attrib['class']  
                }
            except:
                yield{
                   'name': book.css('h3 a::text').get(),
                    'price': 'Sold out',
                    'rating':book.css('p').attrib['class']
                }
        next_page=response.css('li.next a').attrib['href'] 
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url='https://books.toscrape.com/'+ next_page
            else:
                next_page_url='https://books.toscrape.com/catalogue/'+ next_page
            yield response.follow(next_page_url, callback=self.parse)    