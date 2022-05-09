# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
import hashlib
from scrapy.utils.python import to_bytes
from scrapy.pipelines.images import ImagesPipeline
from itemadapter import ItemAdapter


class CastoramaScraperPipeline:
    def process_item(self, item, spider):
        print()
        return item


class CastoramaImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        _hash = hashlib.sha1(to_bytes(request.url)).hexdigest()
        temp = str(item['url'])
        temp = temp[25:]
        path_name = f'full/{temp}/{_hash}.jpg'
        return path_name




