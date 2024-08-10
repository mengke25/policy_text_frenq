# function citycode

import pandas as pd
import re

def citycode(df, city_variable):
    # 创建新的 citycode 变量并初始化为0
    df['citycode'] = 0
    
    # 定义城市名和对应的城市代码
    city_codes = {
        "北京": 110000, "天津": 120000, "石家庄": 130100, "唐山": 130200, "秦皇岛": 130300,
        "邯郸": 130400, "邢台": 130500, "保定": 130600, "张家口": 130700, "承德": 130800,
        "沧州": 130900, "廊坊": 131000, "衡水": 131100, "太原": 140100, "大同": 140200,
        "阳泉": 140300, "长治": 140400, "晋城": 140500, "朔州": 140600, "晋中": 140700,
        "运城": 140800, "忻州": 140900, "临汾": 141000, "吕梁": 141100, "呼和浩": 150100,
        "包头": 150200, "乌海": 150300, "赤峰": 150400, "通辽": 150500, "鄂尔多": 150600,
        "呼伦贝": 150700, "巴彦淖": 150800, "巴音郭": 652800, "乌兰察": 150900, "沈阳": 210100,
        "大连": 210200, "鞍山": 210300, "抚顺": 210400, "本溪": 210500, "丹东": 210600,
        "锦州": 210700, "营口": 210800, "阜新": 210900, "辽阳": 211000, "盘锦": 211100,
        "铁岭": 211200, "朝阳": 211300, "葫芦岛": 211400, "长春": 220100, "吉林": 220200,
        "四平": 220300, "辽源": 220400, "通化": 220500, "白山": 220600, "松原": 220700,
        "白城": 220800, "哈尔滨": 230100, "齐齐哈": 230200, "鸡西": 230300, "鹤岗": 230400,
        "双鸭山": 230500, "大庆": 230600, "伊春": 230700, "佳木斯": 230800, "七台河": 230900,
        "牡丹江": 231000, "黑河": 231100, "绥化": 231200, "上海": 310000, "南京": 320100,
        "无锡": 320200, "徐州": 320300, "常州": 320400, "苏州": 320500, "南通": 320600,
        "连云港": 320700, "淮安": 320800, "盐城": 320900, "扬州": 321000, "镇江": 321100,
        "泰州": 321200, "宿迁": 321300, "杭州": 330100, "宁波": 330200, "温州": 330300,
        "嘉兴": 330400, "湖州": 330500, "绍兴": 330600, "金华": 330700, "衢州": 330800,
        "舟山": 330900, "台州": 331000, "丽水": 331100, "合肥": 340100, "芜湖": 340200,
        "蚌埠": 340300, "淮南": 340400, "马鞍山": 340500, "淮北": 340600, "铜陵": 340700,
        "安庆": 340800, "黄山": 341000, "滁州": 341100, "阜阳": 341200, "宿州": 341300,
        "巢湖": 341400, "六安": 341500, "亳州": 341600, "池州": 341700, "宣城": 341800,
        "福州": 350100, "厦门": 350200, "莆田": 350300, "三明": 350400, "泉州": 350500,
        "漳州": 350600, "南平": 350700, "龙岩": 350800, "宁德": 350900, "南昌": 360100,
        "景德镇": 360200, "萍乡": 360300, "九江": 360400, "新余": 360500, "鹰潭": 360600,
        "赣州": 360700, "吉安": 360800, "宜春": 360900, "抚州": 361000, "上饶": 361100,
        "济南": 370100, "青岛": 370200, "淄博": 370300, "枣庄": 370400, "东营": 370500,
        "烟台": 370600, "潍坊": 370700, "济宁": 370800, "泰安": 370900, "威海": 371000,
        "日照": 371100, "莱芜": 371200, "临沂": 371300, "德州": 371400, "聊城": 371500,
        "滨州": 371600, "菏泽": 371700, "郑州": 410100, "开封": 410200, "洛阳": 410300,
        "平顶山": 410400, "安阳": 410500, "鹤壁": 410600, "新乡": 410700, "焦作": 410800,
        "濮阳": 410900, "许昌": 411000, "漯河": 411100, "三门峡": 411200, "南阳": 411300,
        "商丘": 411400, "信阳": 411500, "周口": 411600, "驻马店": 411700, "武汉": 420100,
        "黄石": 420200, "十堰": 420300, "宜昌": 420500, "襄阳": 420600, "鄂州": 420700,
        "荆门": 420800, "孝感": 420900, "荆州": 421000, "黄冈": 421100, "咸宁": 421200,
        "随州": 421300, "长沙": 430100, "株洲": 430200, "湘潭": 430300, "衡阳": 430400,
        "邵阳": 430500, "岳阳": 430600, "常德": 430700, "张家界": 430800, "益阳": 430900,
        "郴州": 431000, "永州": 431100, "怀化": 431200, "娄底": 431300, "广州": 440100,
        "韶关": 440200, "深圳": 440300, "珠海": 440400, "汕头": 440500, "佛山": 440600,
        "江门": 440700, "湛江": 440800, "茂名": 440900, "肇庆": 441200, "惠州": 441300,
        "梅州": 441400, "汕尾": 441500, "河源": 441600, "阳江": 441700, "清远": 441800,
        "东莞": 441900, "中山": 442000, "潮州": 445100, "揭阳": 445200, "云浮": 445300,
        "南宁": 450100, "柳州": 450200, "桂林": 450300, "梧州": 450400, "北海": 450500,
        "防城港": 450600, "钦州": 450700, "贵港": 450800, "玉林": 450900, "百色": 451000,
        "贺州": 451100, "河池": 451200, "来宾": 451300, "崇左": 451400, "海口": 460100,
        "三亚": 460200, "三沙": 460300, "儋州": 460400, "重庆": 500000, "成都": 510100,
        "自贡": 510300, "攀枝花": 510400, "泸州": 510500, "德阳": 510600, "绵阳": 510700,
        "广元": 510800, "遂宁": 510900, "内江": 511000, "乐山": 511100, "南充": 511300,
        "眉山": 511400, "宜宾": 511500, "广安": 511600, "达州": 511700, "雅安": 511800,
        "巴中": 511900, "资阳": 512000, "贵阳": 520100, "六盘水": 520200, "遵义": 520300,
        "安顺": 520400, "毕节": 520500, "铜仁": 520600, "昆明": 530100, "曲靖": 530300,
        "玉溪": 530400, "保山": 530500, "昭通": 530600, "丽江": 530700, "普洱": 530800,
        "临沧": 530900, "拉萨": 540100, "日喀则": 540200, "昌都": 540300, "林芝": 540400,
        "山南": 540500, "那曲": 540600, "西安": 610100, "铜川": 610200, "宝鸡": 610300,
        "咸阳": 610400, "渭南": 610500, "延安": 610600, "汉中": 610700, "榆林": 610800,
        "安康": 610900, "商洛": 611000, "兰州": 620100, "嘉峪关": 620200, "金昌": 620300,
        "白银": 620400, "天水": 620500, "武威": 620600, "张掖": 620700, "平凉": 620800,
        "酒泉": 620900, "庆阳": 621000, "定西": 621100, "陇南": 621200, "西宁": 630100,
        "海东": 630200, "海南藏": 632500, "银川": 640100, "石嘴山": 640200, "吴忠": 640300,
        "固原": 640400, "中卫": 640500, "乌鲁木": 650100, "克拉玛": 650200, "吐鲁番": 650400,
        "哈密": 650500, "宜城": 420684, "喀什": 653101, "阿克苏": 652900, "楚雄": 532300,
        "大理": 532900, "恩施": 422800, "锡林郭": 152500, "玉树": 632700, "阿拉善": 152900,
        "阿勒泰": 654301, "昌吉": 652301, "临夏": 622900, "塔城": 654200, "文山": 532600,
        "和田": 653201, "大兴安": 232700, "延边州": 222400, "凉山": 513400, "黔西南": 522300,
        "黔南": 522700, "西双版": 532800, "德宏": 533100, "杨凌": 610403, "甘南": 623000,
        "海北": 632200, "黄南": 632500, "海西": 632800, "巴音郭楞": 652800, "一师": 660100,
        "二师": 660200, "三师": 660300, "五师": 660500, "六师": 660600, "七师": 660700,
        "八师": 660800, "十师": 661000, "工师": 661100, "十二师": 661200, "十三师": 661300,
        "十四师": 661400, "兴安盟": 152200, "大兴安岭": 232700, "济源市": 419001,
        "神农架": 429021, "湘西": 433100, "黔东南": 522600, "红河": 532500, "怒江": 533300,
        "迪庆": 533400, "博尔塔拉": 652700, "克孜勒": 653000, "和田": 653201, "伊犁": 654002,
        "绥芬河": 231081, "湘西": 433100, "果洛": 632600, "海西": 632800, "四师": 660400,
        "九师": 660900, "永城": 411400, "潜江": 429005, "阿坝": 513200, "甘孜州": 513300,
        "博州": 652700, "抚远县": 230833, "平潭综合实": 350128, "贵安新区": 550003,
        "平潭综合实验区": 350128, "仙桃": 429004, "梅河口": 220581, "西咸新区": 610100,
        "天门": 429006
    }
    
    # 使用条件语句根据城市名变量更新 citycode
    for city, code in city_codes.items():
        df.loc[df[city_variable].str.contains(city, case=False, na=False), 'citycode'] = code
    
    return df
