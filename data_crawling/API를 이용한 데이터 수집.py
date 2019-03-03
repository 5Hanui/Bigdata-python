#!/usr/bin/env python
# coding: utf-8

# ## 데이터 수집 1레벨
# 
# - API 공급자로부터 내가 원하는 데이터를 제공해주면
# - 즉, openAPI가 존재하여 제공해준다면
# - 꼭, openAPI가 아니더라도 자유롭게 사용할 수 있다면
# - 요청 -> 응답 -> json or xml등 파싱
# - 원하는 데이터를 획득 -> 전처리 -> 적재
# 

# In[2]:


# 요청용
from urllib.request import urlopen, Request


# In[3]:


import urllib


# In[4]:


# KAKAO REST API 키
KAKAO_REST_API = '{$API_KEY}' # 부여받은 API키 입력하면됨.
URL_BASE = "https://dapi.kakao.com/v2/search/web"
# 검색어에 한글이 존재하거나, 공백이 존재하면 오류발생
# url 인코딩 처리를 해서 %xxx 형식으로 처리되어야 한다.
keyword = urllib.parse.quote('iphone')
keyword


# In[5]:


params =   'query={}&page={}&size=50&sort=recency'.format(keyword,1)
params


# In[6]:


# 헤더 세팅
HEADER_VALUE = 'KakaoAK '+ KAKAO_REST_API
HEADER_VALUE


# In[7]:


# get 방식으로 구성
url = '%s?%s' % (URL_BASE, params)
url


# In[8]:


# 요청을 만들어서 헤더를 설정
req = Request(url)
req.add_header('Authorization', HEADER_VALUE)


# In[9]:


# 요청후 응답
response = urlopen(req)


# In[10]:


if response.code == 200 : 
    print('통신성공')
    # json 파싱
    import json
    tmp = json.load( response )


# In[11]:


# 데이터의 구조 파악이 끝나면
# > tmp
# > tmp['documents']
# > len(tmp['documents'])
# > type(tmp['documents'])
# ...
for res in tmp['documents']:
    # 일종의 데이터 정제작업
    print(res['title'].replace('<b>','').replace('</b>',''))


# - 제목, 날짜, 컨텐츠 3개 수집
# - 디비에 어떻게 넣을 것인가? 이 부분 결정이 안되서 데이터를
# - 모아두는데까지  -> 1페이지 ~ 50페이지까지 총 2500개의 결과를 
# - 위의 방식이 성공하면 1~50페이지까지 확장적용
# - 리스트[딕셔너리 구조] 수집
#     >     [
#             {'title':'제목', 'datetime':시간, 'contents':'내용' }
#             { .. }
#       ]
#     > 위의 구조로 총 2500개를 모아둔다

# In[42]:


# ~/v2/search/web?query=검색어&page=1&size=50&sort=recency
# ~/v2/search/web?query=검색어&page=2&size=50&sort=recency
# ~
# ~/v2/search/web?query=검색어&page=50&size=50&sort=recency
def makeParam(searchStr, page):
    keyword = urllib.parse.quote('아이즈원')
    params = 'query={}&page={}&size=50&sort=recency'.format(keyword,page)
    return params


# In[50]:


import json
import time
# 데이터를 담을 그릇
results = list()
for page in range(1,51): #51
    # 페이지 번호
    print(page)
    # 요청 URL 구성
    params = makeParam('아이즈원', page)
    url    = '%s?%s' % (URL_BASE, params)
    url
    print(url)
    # 헤더설정
    req = Request(url)
    req.add_header('Authorization', HEADER_VALUE)
    # 요청
    response = urlopen(req)
    # 응답
    if response.code == 200 : 
        tmp = json.load( response )
        # 데이터를 파싱해서 제목, 날짜, 컨텐츠를 적재
        # 자료구조!!
        print('총 데이터량', len(tmp['documents']))
        # 검색 결과로 나온 데이터를 계속 적재시킨다(이어붙임)
        results.extend(tmp['documents'])
        # 1초 쉬고
        time.sleep(1)


# In[55]:


# 결과물 확인
print(len(results))
# 데이터 덩어리는 앞에 샘플, 뒤에 샘플 확인한다. [0:10], [-10:]
results[-1:]


# In[56]:


# 검색어 강조 처리하는 <b> 태그 제거 함수
def deleteBTag(str):
    return str.replace('<b>','').replace('</b>','')


# In[64]:


# 데이터 보정 처리: 'url'을 제거하시오
# 간단한 데이터 전처리 과정
# del 딕셔너리['url']
for r in results:
    # 원본조작
    r['title']    = deleteBTag(r['title'])
    r['contents'] = deleteBTag(r['contents'])
    # 해당 키가 존재하면 삭제해라
    if 'url' in r:
        del r['url']
results[-2:]


# ## 데이터 적재
# 
# - 데이터(리스트 딕셔너리 구조)를 RDBMS의 특정 테이블에 입력(insert)
# - 일반적인 방법으로 진행을 하면 insert 구문은 데이터수 만큼 하거나, sql을 한번에 넣을 수 있게 짜거나 해야 한다.
# - 이 방법은 속도가 느리고, 번잡하다.
# - 수집한 데이터 => DataFrame 변환(Pandas의 자료구조)
# - numpy : ndarray => 배열
# - pandas : Series(1차원 자료구조), DataFrame(2차원이상) 자료구조
# - pandas의 함수를 이용하여 간단하게 디비에 데이터를 적재할 수 있다.
# 
# 

# - 필요한 모듈 
# - mysql 계열 접근 처리
# - pip install pymysql
# - 상위 레벨의 디비 처리 (wrapping으로 사용)
# - pip install sqlalchemy
# - 데이터 전송 처리
# - pip install pandas
# - 데이터 흐름 파이프라인
# - dict -> DataFrame -> sqlalchemy -> pymysql -> table 적재

# In[65]:


import pymysql
from sqlalchemy import create_engine
import pandas as pd 
import pandas.io.sql as pSql


# In[82]:


# 파이프라인
# dict -> DataFrame -> sqlalchemy -> pymysql -> table 적재
# 1. dict -> DataFrame
# results -> 변환
df_dict = pd.DataFrame.from_dict(results)
df_dict #인덱스도 데이터로 들어갈수 있으므로 조심하기!


# In[83]:


# sqlalchemy -> pymysql -> mysql
# 연결 문구
db_url = 'mysql+pymysql://{$아이디}:{$비번}@127.0.0.1/python_db' # 아이디:비번 입력!
# 엔진 생성
engine = create_engine( db_url, encoding='utf8' )


# In[84]:


# 연결
conn = engine.connect() # 디비연결됨..


# In[85]:


# 데이터 가져오기 (번외)
# 주식 데이터를 가져와서 DataFrame으로 생성
df_trade = pSql.read_sql('select * from tbl_trade', conn)
df_trade.head(2)


# In[86]:


# 삽입 (insert)
# index => DataFrame상의 index 파트를 데이터를 간주해서 입력할
# 것인가?
df_dict.to_sql( name='kakaoSearch', con=conn , 
               if_exists='append', index=False) 


# In[ ]:




