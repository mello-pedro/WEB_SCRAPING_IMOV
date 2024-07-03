from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class ImoSpider(CrawlSpider):
    name = 'myspider'
    allowed_domains = ["imovirtual.com"]
    start_urls = ["https://www.imovirtual.com/arrendar/"]

    ##Nesta parte podem ser definidos outros parametros como obey_robotsTXT, proxy rotation etc
    ## Observar arquivo settings.py deste repo. Melhor definir estes parâmetros lá.
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }
    
    rules = (
        Rule(LinkExtractor(allow=("page=",)), callback='parse_page', follow=True),
    )

    def parse_page(self, response):
        for offer_item in response.css('div.offer-item-details'):
            title = offer_item.css('span.offer-item-title::text').get()
            location = offer_item.css('p::text').get().strip()
            type_info = offer_item.css('p span.hidden-xs::text').get()
            price = offer_item.css('li.offer-item-price::text').get().strip()
            area = offer_item.css('li.hidden-xs.offer-item-area::text').get().strip()

            yield {
                'title': title,
                'location': location,
                'type': type_info,
                'price': price,
                'area': area
            }

##Atencao:a spider deve ser ativada via linha de comando no terminal. Para isso navegue até a pasta do 
# projeto via terminal, ative o ambiente virtual "venv_scrapy" e execute o scraping com o comando
# scrapy crawl nome_da_spider -o output2.json 
