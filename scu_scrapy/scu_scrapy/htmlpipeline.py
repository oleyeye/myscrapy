# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from string import Template


class HTMLPipeline:
    headers = ['#', '导师', '职称', '方向', '摘要', '链接']

    def open_spider(self, spider):
        with open('template.html', 'r', encoding='utf-8') as reader:
            self.template = Template(reader.read())
        self.data = []
        self.count = 1

    def close_spider(self, spider):
        with open('mentor.html', 'w', encoding='utf-8') as writer:
            writer.write(
                self.template.safe_substitute(content=''.join(self.data)))

    def process_item(self, item, spider):
        value = ItemAdapter(item).asdict()
        self.write_line(value)
        return item

    def write_line(self, value):
        self.data.append(f"""<tr>
            <td>{self.count}</td>
            <td>{value['name']}</td>
            <td>{value['title']}</td>
            <td>{value['domain']}</td>
            <td>{value['abstract']}</td>
            <td><a href="{value['url']}" target="_blank">go</a></td>
        </tr>""")
        self.count += 1
