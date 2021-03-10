import scrapy

from scrapy.loader import ItemLoader

from ..items import NkbmsiItem
from itemloaders.processors import TakeFirst


class NkbmsiSpider(scrapy.Spider):
	name = 'nkbmsi'
	start_urls = ['https://www.nkbm.si/aktualno']

	def parse(self, response):
		post_links = response.xpath('//a[@class="newslink boxshadow"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//div[@id="newstitle"]/h2/text()').get()
		description = response.xpath('//div[@class="content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@id="newsdate"]//text()[normalize-space()]').getall()
		date = [p.strip() for p in date]
		date = ' '.join(date).strip()

		item = ItemLoader(item=NkbmsiItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
