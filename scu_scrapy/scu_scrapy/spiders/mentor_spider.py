import scrapy
from scrapy_splash import SplashRequest
from ..items import MentorItem
from textrank4zh import TextRank4Sentence
import unicodedata


class MentorSpider(scrapy.Spider):
    name = 'mentor'
    list_args = {
        'html': 1,
        'png': 1,
        'wait': 1,
    }
    detail_args = {
        'html': 1,
        'png': 1,
        'wait': 10,
    }

    target = [
        '徐玖平',
        '顾新',
        '邓富民',
        '陈传',
        '李跃宇',
        '张欣莉',
        '童利忠',
        '王緌',
        '钟胜',
        '向晓林',
        '刘馨',
        '李晓峰',
        '梁学栋',
        '颜锦江',
        '王涛',
        '卢毅',
        '周贵川',
        '吴鹏昆',
        '曾自强',
        '梁海明',
        '李智',
        '孟致毅',
        '金茂竹',
        '姚黎明',
        '腾格尔',
        '晁祥瑞',
    ]

    # target = ["刘馨"]

    def __init__(self):
        self.tr4s = TextRank4Sentence()

    def start_requests(self):

        urls = ['http://bs.scu.edu.cn/quanyuanjiaoshi.html']
        for url in urls:
            yield SplashRequest(url,
                                self.parse,
                                endpoint='render.json',
                                args=self.list_args)

    def parse(self, response):
        # html = response.body

        # you can also query the html result as usual
        # title = response.css('title').get()
        # print("title: ", title)
        count = 0
        for item in response.css('div.inlist a'):
            # if count > 5:
            #     return

            name = item.css('::text').get()
            if not name in self.target:
                continue

            count += 1
            detail_url = item.attrib['href']

            if detail_url is not None:
                detail_url = response.urljoin(detail_url)

                cb_args = {
                    'index': count,
                    'name': name,
                    'url': detail_url,
                }

                request = SplashRequest(detail_url,
                                        self.parse_detail,
                                        endpoint='render.json',
                                        args=self.detail_args,
                                        cb_kwargs=cb_args)
                self.target.remove(name)
                yield request

        print(f"{' '.join(self.target)} are not found")
        for notFoundMan in self.target:
            count += 1
            item = MentorItem()
            item['index'] = count
            item['name'] = notFoundMan
            item['title'] = 'N/A'
            item['domain'] = 'N/A'
            item['abstract'] = 'N/A'
            item['fullContent'] = 'N/A'
            item['url'] = ''
            yield item

    def parse_detail(self, response, index, name, url):
        # html = response.body
        # print('html: ', html)

        title = self.processTitle(
            response.css(
                'div.teacher.clearfix div.con ul li:nth-child(2) ::text').
            getall())

        full_content = self.processContent(
            response.css('div.teadetail ::text').getall())

        domain = self.processDomain(full_content)
        abstract = self.getAbstract(full_content)

        item = MentorItem()
        item['index'] = index
        item['name'] = name
        item['title'] = title
        item['domain'] = domain
        item['abstract'] = abstract
        item['fullContent'] = full_content
        item['url'] = url
        yield item

    def processTitle(self, titlelist):
        if len(titlelist) == 3:
            return self.amendLine(titlelist[2])
        return ''

    def processContent(self, contentList):
        return ' '.join(self.amendLine(content)
                        for content in contentList).strip()

    def processDomain(self, content):
        bracket_start = '【'
        bracket_end = '】'
        start_index = content.find(f"{bracket_start}研究领域{bracket_end}：") + 7
        if start_index < 7:
            start_index = content.find("研究方向") + 4
            if start_index < 4:
                return ""

        otherSectionIndex = content.find(bracket_start, start_index)
        end_index = len(
            content) if otherSectionIndex == -1 else otherSectionIndex
        return self.amendLine(content[start_index:end_index])

    def getAbstract(self, text):
        self.tr4s.analyze(text=text, lower=True, source='all_filters')
        results = self.tr4s.get_key_sentences(num=1)
        if len(results) == 1:
            return results[0].sentence
        return ''

    def amendLine(self, content):
        content = content.encode('utf-8', 'ignore').decode('utf-8')
        return content.replace(' ', '').replace('\n', '').strip()
