import pandas as pd
import re

def provcode(df, prov_variable):
    # 创建新的 provcode 变量并初始化为0
    df['provcode'] = 0
    
    # 定义省份名和对应的省份代码
    prov_codes = {
        "北京": 110000, "天津": 120000, "河北": 130000, "山西": 140000, "内蒙": 150000,
        "辽宁": 210000, "吉林": 220000, "黑龙江": 230000, "上海": 310000, "浦东": 310000,
        "江苏": 320000, "浙江": 330000, "安徽": 340000, "福建": 350000, "江西": 360000,
        "山东": 370000, "河南": 410000, "湖北": 420000, "湖南": 430000, "广东": 440000,
        "广西": 450000, "海南": 460000, "重庆": 500000, "四川": 510000, "贵州": 520000,
        "云南": 530000, "西藏": 540000, "陕西": 610000, "甘肃": 620000, "青海": 630000,
        "宁夏": 640000, "新疆": 650000
    }
    
    # 使用条件语句根据城市名变量更新 provcode
    for prov, code in prov_codes.items():
        df.loc[df[prov_variable].str.contains(prov, case=False, na=False), 'provcode'] = code

    # 特殊处理：根据特定区/县更新省份代码
    beijing_districts = ["东城区", "西城区", "朝阳区", "丰台区", "石景山区", "海淀区", "门头沟区", "房山区", "通州区", "顺义区", "昌平区", "大兴区", "怀柔区", "平谷区", "密云区", "延庆区"]
    tianjin_districts = ["和平区", "河东区", "河西区", "南开区", "河北区", "红桥区", "东丽区", "西青区", "津南区", "北辰区", "武清区", "宝坻区", "滨海新区", "宁河区", "静海区", "蓟州区"]
    shanghai_districts = ["黄浦区", "徐汇区", "长宁区", "静安区", "普陀区", "虹口区", "杨浦区", "闵行区", "宝山区", "嘉定区", "浦东新区", "金山区", "松江区", "青浦区", "奉贤区", "崇明区"]
    chongqing_districts = ["万州区", "涪陵区", "渝中区", "大渡口区", "江北区", "沙坪坝区", "九龙坡区", "南岸区", "北碚区", "綦江区", "大足区", "渝北区", "巴南区", "黔江区", "长寿区", "江津区", "合川区", "永川区", "南川区", "璧山区", "铜梁区", "潼南区", "荣昌区", "开州区", "梁平区", "武隆区", "城口县", "丰都县", "垫江县", "忠县", "云阳县", "奉节县", "巫山县", "巫溪县", "石柱土家族自治县", "秀山土家族苗族自治县", "酉阳土家族苗族自治县", "彭水苗族土家族自治县"]

    for district in beijing_districts:
        df.loc[df[prov_variable].str.contains(district, case=False, na=False), 'provcode'] = 110000

    for district in tianjin_districts:
        df.loc[df[prov_variable].str.contains(district, case=False, na=False), 'provcode'] = 120000

    for district in shanghai_districts:
        df.loc[df[prov_variable].str.contains(district, case=False, na=False), 'provcode'] = 310000

    for district in chongqing_districts:
        df.loc[df[prov_variable].str.contains(district, case=False, na=False), 'provcode'] = 500000
    
    return df

