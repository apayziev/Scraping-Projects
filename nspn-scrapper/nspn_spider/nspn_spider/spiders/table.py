import scrapy

class TableSpider(scrapy.Spider):
    name = 'table'
    start_urls = ['https://www.espn.com/soccer/standings/_/league/uefa.champions/season/2021']

    def fifth(self, lst):
        start = 0
        end = 5

        while end <= len(lst):
            yield lst[start:end]
            start += 5
            end += 5

    def parse(self, response):
        data = {}

        team_rows = response.css("table")[0].css("tr")
        detail_rows = response.css("table")[1].css("tr")

        for group, group_detail in zip(self.fifth(team_rows), self.fifth(detail_rows)):
            group_label = group[0].css("td span::text").get()

            data[group_label] = {} 

            for team, detail in zip(group[1:], group_detail[1:]):
                team_label = team.css("td span.hide-mobile a::text").get()

                table_details = detail.css("td span::text").getall()
                
                data[group_label][team_label] = {
                    "Wins": table_details[1],
                    "Draws": table_details[2], 
                    "Loses": table_details[3],
                    "Points": table_details[-1]
                }
        
        yield data