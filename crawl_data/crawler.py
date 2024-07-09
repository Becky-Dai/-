import os
from time import sleep
from lxml import etree
import requests, re
from urllib.parse import urljoin, urlencode

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # Chrome浏览器中的示例，常见请求头
    'Cookie': '',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    # 添加请求头（爬虫和反爬虫斗争的第一步）伪造User-Agent，这是百度搜索之后显示的常用的User-Agent
}

base_url = 'http://www.aihuhua.com/hua/'
classification = ['花卉类别', '花卉功能', '应用环境', '盛花期_习性', '养护难度']  # 总类别
page_size = [0, 12, 20, 34, 42, 46]  # 页面范围
flower_class = {}  # 花卉类别
flower_class_file = open('data/种类.txt', 'a', encoding='utf8')

# 界门纲目科属种
Kingdom = {}
Phylum = {}
Class = {}
Order = {}
Family = {}
Genus = {}
Species = {}


Kingdom_file = open('data/科属/界.txt', 'a', encoding='utf8')
# data/科属/界.txt路径下，以a模式打开（使用“a”模式。把所有要写入文件的数据都追加到文件的末尾，如果文件不存在，将自动被创建。），以UTF-8编码方式进行读写
Phylum_file = open('data/科属/门.txt', 'a', encoding='utf8')
Class_file = open('data/科属/纲.txt', 'a', encoding='utf8')
Order_file = open('data/科属/目.txt', 'a', encoding='utf8')
Family_file = open('data/科属/科.txt', 'a', encoding='utf8')
Genus_file = open('data/科属/属.txt', 'a', encoding='utf8')
Species_file = open('data/科属/种.txt', 'a', encoding='utf8')
relation_file = open('data/科属/归属关系.txt', 'a', encoding='utf8')


def get_base_html(get):
    if get:
        res = requests.get(base_url,
                           headers=headers)  # res = requests.get(http://www.aihuhua.com/hua/, headers=headers)
        file = open('base_html.txt', 'w', encoding='utf8')
        # base_html.txt路径下，以W模式打开（以”写”的方式打开），以UTF-8编码方式进行读写
        file.write(res.text)  # 把获取的内容写进去保存
        print('主页源码爬取完成')
    else:
        text = open('base_html.txt', encoding='utf8').read()  # 将文件数据作为utf8编码格式返回到base_html.txt
        print('主页源码获取完成')
        return text


def get_classification():
    global classification
    base_html = get_base_html(0)
    classification = re.findall('<h2 class="title " title="(.*?)">', base_html)
    # <h2 class="title " title="花卉类别">花卉类别</h2>获取大分类class="title "
    content = re.findall('<li><a href="(.*?)" class="a " title="(.*?)" target="_self">', base_html)
    # <li><a href="/hua/guanshang/" class="a " title="观赏花卉" target="_self">观赏</a>获取的大份类下的小分类class="a "
    url = 'http://www.aihuhua.com'
    k = 0
    for i in range(len(classification)):
        classification[i] = classification[i].replace(' / ', '_')  # i是5个大类别+1，且把类别文字中有/的换成_
        file = open('data/' + '花卉大全.txt', 'a', encoding='utf8')  # 追加写入花卉大全.txt
        # os.mkdir('data/' + classification[i])
        for j in range(page_size[i], page_size[i + 1]):  # j是【0,12】【12,20】
            open('data/' + classification[i] + '/' + content[j][1] + '.txt', 'w', encoding='utf8')
            # data路径下i个大分类下用w模式创建小分类.txt（以utf8编码格式）
            # w：只写。1. 如果文件不存在会创建文件兵写入数据 2. 如果文件存在，那么会把文件中原有数据先清空，然后再写入，
            file.write(str(k) + '\t' + url + content[j][0] + '\t' + content[j][1] + '\n')
            k += 1
        file.close()
    print('类别构造完成')


def get_content():
    file = open('data/花卉大全.txt', 'r', encoding='utf8')  # r ：只读
    lines = file.readlines()  # readlines() 方法用于读取所有行(直到结束符 EOF)并返回列表，该列表可以由 Python 的 for... in ... 结构进行处理。如果碰到结束符 EOF 则返回空字符串
    # page_size = [0, 12, 20, 34, 42, 46]  # 页面范围
    ALL_INDEX = 0
    # 0 6477 10977 20857
    for i in range(0, 5):
        # -------
        # 分批次爬取 修改i的起始值 以及ALL_INDEX的值
        # -------
        for j in range(page_size[i], page_size[i + 1]):
            id, url, name = lines[j].split()
            save_file_name = open('data/' + classification[i] + '/' + name + '.txt', 'w', encoding='utf8')
            # data 下大分类下 小分类名字.txt w模式写入
            index = 1
            # 从第一页开始
            while True:
                content_page_url = url + 'page-' + str(index) + '.html'  # page[index].html
                print(content_page_url, '爬取中...')  # 页面网址
                content_page_html = requests.get(content_page_url, headers=headers)
                if content_page_html.status_code == 200:
                    # 200是“OK”的HTTP状态代码，是一个成功的响应。
                    content_page_text = content_page_html.text
                    # 返回的基于对内容类型的猜测而加工过的数据
                    end = re.findall('class=\'next\'>下一页</a></div>', content_page_text)
                    # 爬取详细花卉信息
                    # ---------------------------------------
                    detail_url = re.findall('<a class="title" target="_blank" title="(.*?)" href="(.*?)">(.*?)</a>',
                                            content_page_text)
                    # <a class="title" target="_blank" title="大叶落地生根" href="http://www.aihuhua.com/huahui/dayeluodishenggen.html">
                    for detail in detail_url:
                        content_url = detail[1]
                        res = requests.get(content_url, headers=headers)
                        if res.status_code == 200:
                            content_text = res.text # 请求得到了"http://www.aihuhua.com/huahui/dayeluodishenggen.html"的页面信息
                            flower_name = detail[0] # 花名的detail的第0个元素（title="大叶落地生根"）
                            anonther_name = re.findall('<label class="cate">别名：(.*?)</label>', content_text)  # 返回别名
                            #   <label class="cate">别名：宽叶不死鸟</label>
                            img = re.findall('<img width="140" alt="(.*?)" title="(.*?)" src="(.*?)"', content_text)
                            #   <img width="140" alt="大叶落地生根" title="大叶落地生根"
                            #   src="http://pic1.huashichang.com/2018/0924/10/5ba84a0199c50_140_120.jpg" />
                            img_link = img[0][2] if len(img[0]) >= 2 and len(img[0][2]) > 0 else '无'
                            # 第0列的第二个元素src  img[0]指的是第0列alt="(.*?)" title="(.*?)" src="(.*?)
                            flower_class_get = re.findall(
                                '<label class="cate">分类：<a href="(.*?)" title="(.*?)" target="_blank">(.*?)</a></label>',
                                content_text)
                            # <label class="cate">分类：<a href="http://www.aihuhua.com/baike/duorouduojiang/"
                            # title="多肉多浆植物" target="_blank">多肉多浆植物</a></label>
                            print(flower_name, flower_class_get[0][-1])
                            if len(flower_class_get) > 0 and flower_class_get[0][-1] not in flower_class:
                                flower_class[flower_class_get[0][-1]] = 1
                                flower_class_file.write(flower_class_get[0][-1] + '\n')
                            belong = re.findall('<label class="cate">科属：(.*?)</label>', content_text)
                            # 	<label class="cate">科属：植物界 被子植物门 双子叶植物纲 蔷薇目 景天科 伽蓝菜属</label>
                            if len(belong[0]) > 0:
                                relation_file.write(str(ALL_INDEX) + '\t' + belong[0] + '\n')
                            belong_line = belong[0].split()
                            for temp in belong_line:
                                if '界' in temp and temp not in Kingdom:
                                    Kingdom[temp] = 1
                                    Kingdom_file.write(temp + '\n')
                                elif '门' in temp and temp not in Phylum:
                                    Phylum[temp] = 1
                                    Phylum_file.write(temp + '\n')
                                elif '纲' in temp and temp not in Class:
                                    Class[temp] = 1
                                    Class_file.write(temp + '\n')
                                elif '目' in temp and temp not in Order:
                                    Order[temp] = 1
                                    Order_file.write(temp + '\n')
                                elif '科' in temp and temp not in Family:
                                    Family[temp] = 1
                                    Family_file.write(temp + '\n')
                                elif '属' in temp and temp not in Genus:
                                    Genus[temp] = 1
                                    Genus_file.write(temp + '\n')
                                elif '种' in temp and temp not in Species:
                                    Species[temp] = 1
                                    Species_file.write(temp + '\n')
                            open_time_get = re.findall(
                                '<label class="cate">盛花期：<a title="(.*?)" target="_blank" href="(.*?)">(.*?)</a>',
                                content_text)
                            # <label class="cate">盛花期：<a title="春季花卉" target="_blank" href="http://www.aihuhua.com/hua/chunji/">春季</a>
                            open_time = '四季'
                            if len(open_time_get) > 0:
                                open_time = open_time_get[0][-1]
                            cmp = re.compile('<p class="desc">(.*?)</p>', re.DOTALL)
                            #  <p class="desc">大叶落地生根是常见的多浆植物，又名宽叶不死鸟，原产于非洲马达加斯加岛。其叶片肥厚多汁，边缘长出整齐美观的不定芽，形似一群小蝴蝶，飞落于地，立即扎根繁育子孙后代，颇有奇趣。同种类还有‘‘棒叶不死鸟”，也被称为细叶不死鸟。用于盆栽，是窗台绿化的好材料，点缀书房和客室也具雅趣。株高50-150cm，茎单生，直立，褐色。
                            # 大叶落地生根叶交互对生中，叶片肉质，长三角形、卵形，叶长15-20cm，宽2-3c...</p>
                            desc = ' '.join(re.findall(cmp, content_text)[0].split())
                            # split方法输出的是列表  join方法输出的是字符串，刚好配合起来
                            # print(re.findall(cmp, content_text))
                            # print(desc)
                            # 保存到文件
                            save_text = str(ALL_INDEX) + '\t' + flower_name + '\t'  # 30	姬牡丹
                            save_text += anonther_name[0] if len(anonther_name[0]) > 0 else '无'  # 姬黑牡丹
                            save_text += '\t' + img_link  # http://pic1.huashichang.com/2016/0531/00/574c66e31c411_140_120.jpg
                            save_text += '\t' + flower_class_get[0][-1] if len(flower_class_get) > 0 else '无'  # 多肉多浆植物
                            save_text += '\t' + belong[0] if len(belong[0]) > 0 else '无'  # 植物界 被子植物门 双子叶植物纲  仙人掌科 岩牡丹属
                            save_text += '\t' + open_time + '\t'  # 夏季
                            save_text += desc if len(desc) > 0 else '无'
                            # 姬牡丹，仙人球族、岩牡丹属多年生肉质植物，为黑牡丹的矮性变种。 姬牡丹为多年生肉质植物，植株初为单生，成年后会在基部萌发仔球，使其成为丛生状。姬牡丹属于黑牡丹的矮性变种，植株较小，株幅3－5厘米，表面灰绿色，其他特征同黑牡丹。二者之间还有一个杂交种，株形似姬牡丹，表皮颜色像黑牡丹，有人称它为“姬黑牡丹”。
                            save_file_name.write(save_text + '\n')  # save + 换行
                            ALL_INDEX += 1

                        # print(flower_name, '已保存')
                        else:
                            print(content_url, '爬取失败')
                    # ---------------------------------------
                    if len(end) <= 0:
                        break
                    index += 1
                    # if index == 2:
                    #     break
                else:
                    print(content_page_html, '获取失败')
                # break
            print(name, '爬取完成')  # 二级文本
            # sleep(3)
            # break
        print(classification[i], '爬取完成')  # 一级目录
        sleep(10)
        # break
    # 保存分类
    # 保存科属


if __name__ == '__main__':
    get_classification()  # 建立分类文件
    get_content()  # 爬取详细词条
