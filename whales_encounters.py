import scrapy
import re

class WhalesEncountersSpider(scrapy.Spider):
    name = 'whales_encounters'

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }

    start_urls = ['http://www.splashcatalog.org/encounters/allEncounters.jsp?start=1&end=10']

    def parse(self, response):
        # Extract the links to the whale encounter pages
        whale_enc_links = response.xpath('//table[@id="results"]/tr[@class="lineitems"]/td[2]/a/@href').extract()

        for i in range(len(whale_enc_links)):
            yield scrapy.Request(
                url=response.urljoin(whale_enc_links[i]),
                callback=self.parse_whale_enc,
                meta={
                    'url': whale_enc_links[i]
                }
            )

        # Follow pagination links and repeat
        next_url = response.xpath('//table[@id="results"]//tr[@class="paging"]//a/@href').extract()[0]

        yield scrapy.Request(
            url=next_url,
            callback=self.parse
        )

    def parse_whale_enc(self, response):
        url = response.request.meta['url']

        # Extract data from the whale encounter show page

        encounter_id = response.xpath('//div[@id="main"]/table//tr/td/p[1]/font/text()').extract()
        individual_id = response.xpath('//div[@id="main"]/table//tr/td/p[3]/a/text()').extract()[0]

        occurrence_id = response.xpath('//div[@id="main"]/table//tr/td/p[5]/a/text()').extract()[0]

        # Whale status, e.g.: 'alive'
        status = response.xpath('//div[@id="main"]/table//tr/td/p[contains(text(), "Status:")]/text()').extract()[0]
        encounter_date = response.xpath('//div[@id="main"]/table//tr/td/table//tr/td/p[1]/a/text()').extract()[0]
        # This contains location name, location ID, latitude and longitude
        encounter_location_info = response.xpath('//div[@id="main"]/table//tr/td/table//tr/td/p[3]/text()').extract()
        # Sex of the whale as recorded on the enounter record
        encounter_sex = response.xpath('//div[@id="main"]/table//tr/td/table//tr/td/p/strong[contains(text(), "Sex:")]/../text()').extract()[0]
        # Noticeable scarring
        scarring = response.xpath('//div[@id="main"]/table//tr/td/table//tr/td/p/strong[contains(text(), "Noticeable scarring:")]/../text()').extract()[0]
        behavior = response.xpath('//div[@id="main"]/table//tr/td/table//tr/td/p/strong[contains(text(), "Behavior:")]/../text()').extract()
        life_stage = response.xpath('//div[@id="main"]/table//tr/td/table//tr/td/p/strong[contains(text(), "Life stage:")]/../text()').extract()
        beh_role = response.xpath('//div[@id="main"]/table//tr/td/table//tr/td/p/strong[contains(text(), "Beh Role")]/../text()').extract()
        locality = response.xpath('//div[@id="main"]/table//tr/td/table//tr/td/p/strong[contains(text(), "Locality")]/../text()').extract()
        region_name = response.xpath('//div[@id="main"]/table//tr/td/table//tr/td/p/strong[contains(text(), "Region Name")]/../text()').extract()
        sighting = response.xpath('//div[@id="main"]/table//tr/td/table//tr/td/p/strong[contains(text(), "Sighting")]/../text()').extract()[1]
        pos_type = response.xpath('//div[@id="main"]/table//tr/td/table//tr/td/p/strong[contains(text(), "Pos Type")]/../text()').extract()
        sighting_comments = response.xpath('//div[@id="main"]/table//tr/td/table//tr/td/p/strong[contains(text(), "Sighting Comments")]/../text()').extract()
        est_size_best = response.xpath('//div[@id="main"]/table//tr/td/table//tr/td/p/strong[contains(text(), "Est Size Best")]/../text()').extract()
        vessel = response.xpath('//div[@id="main"]/table//tr/td/table//tr/td/p/strong[contains(text(), "Vessel")]/../text()').extract()
        group_behavior = response.xpath('//div[@id="main"]/table//tr/td/table//tr/td/p/strong[contains(text(), "Group Behavior")]/../text()').extract()
        number_calves = response.xpath('//div[@id="main"]/table//tr/td/table//tr/td/p/strong[contains(text(), "Number Calves")]/../text()').extract()
        group_type = response.xpath('//div[@id="main"]/table//tr/td/table//tr/td/p/strong[contains(text(), "Group Type")]/../text()').extract()
        additional_comments = response.xpath('//div[@id="main"]/table//tr/td/table//tr/td/p/strong[contains(text(), "Additional comments:")]/../text()').extract()
        submitter = response.xpath('//div[@id="main"]/table//tr/td/table//tr/td/p/strong[contains(text(), "Submitter")]/../text()').extract()
        photographer = response.xpath('//div[@id="main"]/table//tr/td/table//tr/td/p/strong[contains(text(), "Photographer")]/../text()').extract()


        yield {
            'url': url,

            'encounter_id': encounter_id,
            'individual_id': individual_id,
            'occurrence_id': occurrence_id,
            'status': status,
            'encounter_date': encounter_date,

            'encounter_location_info': encounter_location_info,
            'encounter_sex': encounter_sex,
            'scarring': scarring,
            'behavior': behavior,
            'life_stage': life_stage,
            'beh_role': beh_role,
            'locality': locality,
            'region_name': region_name,
            'sighting': sighting,
            'pos_type': pos_type,
            'sighting_comments': sighting_comments,
            'est_size_best': est_size_best,
            'vessel': vessel,
            'group_behavior': group_behavior,
            'number_calves': number_calves,
            'group_type': group_type,
            'additional_comments': additional_comments,
            'submitter': submitter,
            'photographer': photographer
        }
