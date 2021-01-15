import scrapy
from ..items import ImdbItem

class IMDBSpider(scrapy.Spider):
	name = 'imdb'
	index = 1

	#user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
	def start_requests(self):
		urls = ['https://www.imdb.com/search/title/?countries=us&title_type=feature&num_votes=10000%2C&sort=user_rating%2Cdesc&fbclid=IwAR0qlD-jJt4JUhp_7F0-DGNkKAMJfawu4M6KyDhpdnfBDquEY06nHGL8NIo']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parsePage)

	def parsePage(self, response):
		# imdb_item = ImdbItem()
		for page in response.xpath("//div[@class='lister-item mode-advanced']"):
			title = page.xpath("./div[@class='lister-item-content']/h3/a/text()").extract_first()
			release = page.xpath("./div[@class='lister-item-content']/h3/span[@class='lister-item-year text-muted unbold']/text()").extract_first()[-5:-1]
			genre = page.xpath("./div[@class='lister-item-content']/p[@class='text-muted ']/span[@class='genre']/text()").extract_first().replace('\n', '').replace(' ','')
			rating = page.xpath("./div[@class='lister-item-content']/div[@class='ratings-bar']/div[@class='inline-block ratings-imdb-rating']/strong/text()").extract_first()
			urlFilm = page.xpath("./div[@class='lister-item-content']/h3/a/attribute::href").extract_first()

			# lấy giá trị trong thuộc tính data-value của tất cả thẻ span thỏa mãn
			votes_gross = page.xpath("./div[@class='lister-item-content']/p[@class='sort-num_votes-visible']/span[@name='nv']/attribute::data-value").extract()
			# kiểm tra trong trường hợp không có gross
			votes = votes_gross[0]
			if len(votes_gross) == 2:
				gross = votes_gross[1]
			else:
				gross = ''


			# tách director và starts
			ds_path = page.xpath("./div[@class='lister-item-content']/p[@class='']/child::*") # lấy tất cả tag con của tag hiện tại
			ds = []
			for tag in ds_path:
				ds.extend(tag.xpath("./text()").extract())
			
			# kiểm tra trong trường hợp không có stars
			try:
				i = ds.index('|')
				director = ds[: i]
				stars = ds[i+1:]
			except:
				director = ds 
				stars = []

			# tách thể loại phim
			genre = genre.split(',')
			genres = {'Action': 0, 'Adventure': 0, 'Animation': 0, 'Biography': 0, 'Comedy': 0, 'Crime': 0, 'Documentary': 0,
					  'Drama': 0, 'Family': 0, 'Fantasy': 0, 'Film-Noir': 0, 'Game-Show': 0, 'History': 0, 'Horror': 0, 'Music': 0, 
					  'Musical': 0, 'Mystery': 0, 'News': 0,'Reality-TV':0,	'Romance': 0, 'Sci-Fi': 0, 'Sport': 0, 'Talk-Show': 0,	 
					  'Thriller': 0, 'War': 0, 'Western':0 }

			for i in range(len(genre)):
				genres[genre[i]] = 1


			data = {}
			# đi vào trong link để lấy data khác, cần truyền vào data hiện tại để lưu kèm
			yield scrapy.Request(url='https://www.imdb.com/'+urlFilm, meta={'data':data}, callback=self.getBudget)


			data['title'] 			= title
			#data['release'] 		= release
			#	'genre' : genre
			#data['rating'] 		= rating
			#data['votes'] 			= votes
			data['gross'] 			= gross
			# data['director']		= director
			# data['stars']			= stars
			# data['Action']		= genres['Action'] 
			# data['Adventure']		= genres['Adventure'] 
			# data['Animation']		= genres['Animation'] 
			# data['Biography']		= genres['Biography'] 
			# data['Comedy']		= genres['Comedy']
			# data['Crime']			= genres['Crime'] 
			# data['Documentary']	= genres['Documentary']
			# data['Drama']			= genres['Drama']
			# data['Family']		= genres['Family'] 
			# data['Fantasy']		= genres['Fantasy'] 
			# data['Film-Noir']		= genres['Film-Noir']
			# data['Game-Show']		= genres['Game-Show'] 
			# data['History']		= genres['History'] 
			# data['Horror']		= genres['Horror'] 
			# data['Music']			= genres['Music']
			# data['Musical']		= genres['Musical'] 
			# data['Mystery']		= genres['Mystery'] 
			# data['News']			= genres['News']
			# data['Reality-TV']	= genres['Reality-TV']	
			# data['Romance']		= genres['Romance'] 
			# data['Sci-Fi']		= genres['Sci-Fi'] 
			# data['Sport']			= genres['Sport']
			# data['Talk-Show']		= genres['Talk-Show']	 
			# data['Thriller']		= genres['Thriller'] 
			# data['War']			= genres['War'] 
			# data['Western']		= genres['Western']

			

		# next trang tự động

		# nextButtonUrl = response.xpath("//div[@class='desc']/a[@class='lister-page-next next-page']/@href").extract_first()
		# if nextButtonUrl is not None and self.index < 10:
		# 	self.index += 1
		# 	yield scrapy.Request(url='https://www.imdb.com' + nextButtonUrl, callback=self.parsePage)


	def getBudget(self, response):
		data = response.meta['data']
		budget = ''
		for att in response.xpath("//div[@class='txt-block']"):
			if att.xpath("./h4/text()").extract_first() == 'Budget:':
				budget = att.xpath('./child::text()').extract()[1].strip() #child::text -> lấy tất cả text nằm trong thẻ hiện tại

		data['budget'] = budget
		yield data

'''
 con crawl lưu vào hàng đợi bằng yield (scrapy.Request), nên ghi dữ liệu (yield data) để ở con crawl cuối 
'''






			 