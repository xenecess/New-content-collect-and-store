import scrapy
import urllib.parse

class ArticlesSpider(scrapy.Spider):
    name = 'articles'
    # Enter article to search 
    name_to_search=input("Please write what you want to search here : ") 
    urllib.parse.quote_plus(name_to_search)
    name_to_search='https://www.bbc.co.uk/search?q='+ name_to_search

    start_urls = [name_to_search]

    #import urllib.parse
    #urllib.parse.quote_plus('text text') 
    
    def parse(self, response):
        
        next_page = response.urljoin(response.xpath("//nav/div[last()]/div/a/@href").get())
        
        for article in response.xpath("//div[@class='css-14rwwjy-Promo ett16tt11']"):
            
            
            title = article.xpath(".//div/div/p/a/span/text()").get()
            link = article.xpath(".//div/div/p/a/@href").get()
            abstract = article.xpath(".//div/div/p[2]/text()").get()
            date_published = article.xpath(".//div/div/div/dl/div/dd/span/span[2]/text()").get()
            

            yield scrapy.Request(url=link, callback=self.parse_article, meta={
            'title':title,'link':link,'abstract':abstract,'date_published':date_published})

        

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_article(self, response):

        title = response.request.meta['title']
        link = response.request.meta['link']
        abstract = response.request.meta['abstract']
        date_published = response.request.meta['date_published']

        #extracting the text of article
        Raw_text = response.xpath("//div[@class='story-body__inner']/p")
        Ntext = []
        for ptext in Raw_text: 
            t = " ".join(ptext.xpath('.//text()').getall()) 
            Ntext.append(t) 

        #attach text with </>
        text='' 
        for t in Ntext: 
            text+=' </> ' 
            text+=t 

        yield{
            'title':title,
            'link':link,
            'abstract':abstract,
            'date_published':date_published,
            'text': text
        }