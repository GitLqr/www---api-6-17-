#!/usr/bin/env python
# -*- coding: utf8 -*-

reason_desc = [
    ("特征前缀","意义","tag例子","推荐理由描述","例子","热门补足描述","例子"),
    ("movivtnf","豆瓣年份","movivtnf1985","为你找到更多%s年电影","为你找到更多1985年电影","大家都在看%s年的电影","大家都在看1985年的电影"),
    ("movibtqt","百度其他","movibtqt爱情","猜你喜欢的“%s”电影","猜你喜欢的“爱情”电影","大家都在看的%s电影","大家都在看的爱情电影"),
    ("movibtpm","百度片名","movibtpm哈利波特","你是不是在找“%s”","你是不是在找“哈利波特”","大家都在看%s","大家都在看“哈利波特”"),
    ("moviyear","发行年","moviyear1985","为你找到更多%s年电影","为你找到更多1985年电影","大家都在看%s的电影","大家都在看1985年的电影"),
    ("movivtpm","豆瓣片名","movivtpm哈利波特","你是不是在找“%s”","你是不是在找“哈利波特”","大家都在看%s","大家都在看“哈利波特”"),
    ("movivtdq","豆瓣地区","movivtdq香港电影","找到更多%s电影","找到更多香港电影","大家都在看的%s电影","大家都在看的香港电影"),
    ("moviacto","演员","moviacto葛优","%s还演过","葛优还演过","大家都在看%s演的电影","大家都在看葛优演的电影"),
    ("movivtqt","豆瓣其他","movivtqt温情","猜你喜欢的“%s”电影","猜你喜欢的“温情”电影","大家都在看的%s电影","大家都在看的温情电影"),
    ("movibtlx","百度类型","movibtlx科幻","猜你喜欢的%s电影","猜你喜欢的科幻电影","大家都在看的%s电影","大家都在看的科幻电影"),
    ("movivtyr","豆瓣影人","movivtyr汤姆·汉克斯","你爱看的%s的电影","你爱看的汤姆·汉克斯的电影","大家都在看%s的电影","大家都在看汤姆·汉克斯的电影"),
    ("movidire","导演","movidire张艺谋","%s还拍过","张艺谋还拍过","大家都在看%s的电影","大家都在看张艺谋的电影"),
    ("movibtdq","百度地区","movibtdq美国","你爱看的%s电影","你爱看的美国电影","大家都在看%s的电影","大家都在看美国的电影"),
    ("movibtnf","百度年份","movibtnf1985","为你找到更多%s年电影","为你找到更多1985年电影","大家都在看%s的电影","大家都在看1985年的电影"),
    ("moviloca","地区","moviloca美国","你爱看的%s电影","你爱看的美国电影","大家都在看%s的电影","大家都在看美国的电影"),
    ("movibtyr","百度影人","movibtyr汤姆·汉克斯","你爱看的%s的电影","你爱看的汤姆·汉克斯的电影","大家都在看%s的电影","大家都在看汤姆·汉克斯的电影"),
    ("movivtlx","豆瓣类型","movivtlx科幻","猜你喜欢的%s电影","猜你喜欢的科幻电影","大家都在看的%s电影","大家都在看的科幻电影"),
    ("movicate","类型","movicate科幻","猜你喜欢的%s电影","猜你喜欢的科幻电影","大家都在看的%s电影","大家都在看的科幻电影"),
    ("newssorc","文章来源","newssorc华龙网","找到更多来自%s的新闻","找到更多来自华龙网的新闻","来自%s的最热新闻","来自华龙网的最热新闻"),
    ("newsctgy","文章类型","newsctgy体育","为你找到更多%s新闻","为你找到更多体育新闻","最热%s新闻","最热体育新闻"),
    ("newstopi","文章主题","newstopi互联网精选","为你找到更多%s新闻","为你找到更多互联网精选新闻","最热%s新闻","最热互联网精选新闻"),
    ("newsname","分类下的人名","newsname姚明","为你找到更多%s的新闻","为你找到更多姚明的新闻","最热%s新闻","最热姚明新闻"),
    ("newsinst","分类下的机构名","newsinst发改委","为你找到更多%s的新闻","为你找到更多发改委的新闻","最热%s的新闻","最热发改委的新闻"),
    ("newsaddr","分类下的地名","newsaddr中关村","为你找到更多%s的新闻","为你找到更多中关村的新闻","最热%s的新闻","最热中关村的新闻"),
    ("newsngrm","分类下的ngram","newsngrm体育_小德_法网","为你找到更多%(2)s、%(3)s的新闻","为你找到更多小德、法网的新闻","最热%(2)s、%(3)s的新闻","最热小德、法网的新闻"),
    ("newsttag","分类下的tag","newsttag科技_iphone","找到更多%(2)s的%(1)s新闻","找到更多iphone的科技新闻","%(2)s最热的%(1)s新闻","iphone最热的科技新闻"),
    ("newsword","专名","newsword我是歌手","为你找到更多%s的资讯","为你找到更多我是歌手的资讯","最热%s的新闻","最热我是歌手的资讯"),
    ("newsregn","地域","newsregn北京市","%s的新鲜事儿","北京市的新鲜事儿","%s的新鲜事儿","北京市的新鲜事儿"),
    ("movilike","看了又看","movilike<itemid>","看过《%s》的人还看","看过《青春期》的人还看","x","x"),
]
