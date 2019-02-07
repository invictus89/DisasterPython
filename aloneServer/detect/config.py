class Keyward:
    keywordDic = {
        "지진":{
            "지진",
            "여진",
            "진도"
        },
        "날씨이상":{
            '비',
            '폭우'
        },
        "사고":{
            "교통사고",
            "교통 사고",
            "차량사고",
            "차량 사고"
        }
    }
class Key_Config:
    consumerKey = '[own key]'
    consumerSecret = '[own key]'
    accessToken = '[own key]'
    accessTokenSecret = '[own key]'
    
class Detect_Config:
    webConfig_1 = {
        '_title':'지진희갤러리',
        '_url':'http://gall.dcinside.com/board/lists/?id=jijinhee&page=1',
        '_format':'%Y.%m.%d %H:%M',
        '_config':{
                'rowName':'tr.td ',
                'className':'td.t_date',
                'attr':'title'
        }
    }

    webConfig_2 = {
        '_title':'루리웹',
        '_url':'http://bbs.ruliweb.com/community/board/300143/list?page=1',
        '_format':'%H:%M',
        '_config':{
                'rowName':'tr.table_body',
                'className':'td.time',
                'attr':False
        }
    }

    twitConfig = {
        '_title':'트위터',
        '_url': None,
        '_format':"%a %b %d %H:%M:%S +0000 %Y",
        '_config':{
                'rowName':'tr.table_body',
                'className':'td.time',
                'attr':False
        }
    }
    
    keyConfig = {
        '_title':'실시간검색어',
        '_url':'http://datalab.naver.com/keyword/realtimeList.naver?where=main',
        '_format':None,
        '_config':{
                'rowName':None,
                'className':'div.keyword_rank.select_date ul.rank_list li span.title',
                'attr':False
        }
    }

    newsConfig = {
        '_title':'뉴스',
        '_url':'https://search.naver.com/search.naver?where=news&query=지진&ie=utf8&sm=tab_srt&sort=1&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so%3Add%2Cp%3Aall%2Ca%3Aall&mynews=0&mson=0&refresh_start=0&related=0',
        '_format':None,
        '_config':{
                'rowName':None,
                'className':'div.title_desc.all_my span',
                'attr':False
        }
    }