# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MDPipeline:
    def open_spider(self, spider):
        self.file = open('mentor.md', 'w', encoding='utf-8')
        self.addHeader()

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        value = ItemAdapter(item).asdict()
        self.addData(value)
        return item

    def addHeader(self):
        self.file.write('| # | 导师   | 职称 | 方向 | 摘要 | 链接 |\n')
        self.file.write(
            '| ---- | ---- | ---- | ------ | -------------- | ---- |\n')

    def addData(self, item):
        self.file.write(
            f"| {item['index']} | {item['name']} | {item['title']} | {item['domain']} | {item['abstract']} | {item['url']} |\n"
        )
