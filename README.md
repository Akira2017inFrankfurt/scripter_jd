README:

- 运行环境： windows+py3.7+pycharm
- 安装包： selenium + pyquery
- 代码75行： 修改本地查询txt文件地址
- 结果存储在76行的jd_item.txt中
--格式为: item_id(int) \t query_item(str)
- 87行的count需要修改，建议提前将train的数据分割成几个dataset，然后count等于它的行数
- 如果时间充裕，可以调节time.sleep()的数值增大，防止被反爬虫机制制裁

- 新增linux版本
- 下载chromedriver：https://chromedriver.chromium.org/downloads
- 在本地解压，替换83行中地址
