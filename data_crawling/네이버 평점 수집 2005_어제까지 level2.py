#!/usr/bin/env python
# coding: utf-8

# In[26]:


'''
평점별 랭킹 첫 집계일
https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=cur&date=20050207

현재시점까지 집계일 (오늘-1)
https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=cur&date=20190210
'''
from urllib.request import urlopen
from bs4 import BeautifulSoup


# In[27]:


url_base = 'https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=cur&date='
page     = urlopen(url_base+'20190210') #아무것도 없이 요청하면 get방식
soup     = BeautifulSoup( page, 'html.parser')
#soup


# In[28]:


# 날짜 20050207 ~ 20190210 연속된 문자열
import pandas as pd
# 시간의 연속값
#dates = pd.date_range('2005-2-7',periods=5117, freq='D')
#print(dates[:1], dates[-1:],len(dates))


# In[29]:


'''
데이터 구조, 2005.2.5 ~ 2019.2.10 수집 -> 내일부터는 하루에 한번 수집 (바로 직전일 것)
평점일(날짜, regdate timestamp)
영화제목 title varchar
평점 score float
출처 site(값 naver) varchar
'''
# 날짜 형식
dates = pd.date_range('2019-2-9',periods=2, freq='D')


# In[30]:


# dates = pd.date_range('2019-2-9',periods=2, freq='D')
for d in dates:
    print(type(d))
    # timestamp 타입을 문자열화해서 처리한 방식
    print(str(d)[:10].replace('-',''))
    # timestamp 자체에서 날짜 형식을 변경할 수 있다.
    print(d.strftime('%Y%m%d'))


# ### 데이터 수집필드
#  - 평점일(날짜, regdate timestamp)
#  - 영화제목 title varchar
#  - 평점 score float
#  - 출처 site(값 naver) varchar

# In[31]:


for d in dates:
    url      = url_base + d.strftime('%Y%m%d')
    print(url)
    page     = urlopen(url) #아무것도 없이 요청하면 get방식
    soup     = BeautifulSoup( page, 'html.parser')
    # 파싱 -> 적재
    # 평점일 : d
    # 영화제목 : .tit5 찾겠다
    titles   = soup.select('.tit5') 
    # 평점 : .point 찾겠다
    # td들 중에 class가 point인 모든 요소
    points   = soup.find_all('td','point')
    print( titles[0].a.string, points[0].string, 
          '데이터개수는 일치하는가?', len(titles)==len(points) )
    
# 디비입력


# In[34]:


tmp   = []
dates = pd.date_range('2019-2-9',periods=2, freq='D')
for d in dates:
    url      = url_base + d.strftime('%Y%m%d')
    page     = urlopen(url) 
    soup     = BeautifulSoup( page, 'html.parser')
    titles   = soup.select('.tit5') 
    points   = soup.find_all('td','point') 
    # 데이터화 (리스트 딕셔너리 구조)
    # 정방향 인덱스는 0 ~ 데이터개수-1 => range(총개수)
    dump     = [{
                    'title'   : titles[i].a.string,
                    'score'   : float(points[i].string),
                    'site'    : 'naver',
                    'regdate' : d        
                } for i in range(len(titles))]
    # 하루씩 수집한 데이터를 전체 그릇에 추가한다
    tmp.extend(dump)
#tmp


# In[35]:


# 진행율 표시(오래 걸릴 경우 진행율을 시각적으로 확인)
from tqdm import tqdm_notebook
tmp   = []
dates = pd.date_range('2005-2-7',periods=5118, freq='D')
for d in tqdm_notebook(dates):
    url      = url_base + d.strftime('%Y%m%d')
    page     = urlopen(url) 
    soup     = BeautifulSoup( page, 'html.parser')
    titles   = soup.select('.tit5') 
    points   = soup.find_all('td','point') 
    # 데이터화 (리스트 딕셔너리 구조)
    # 정방향 인덱스는 0 ~ 데이터개수-1 => range(총개수)
    dump     = [{
                    'title'   : titles[i].a.string,
                    'score'   : float(points[i].string),
                    'site'    : 'naver',
                    'regdate' : d        
                } for i in range(len(titles))]
    # 하루씩 수집한 데이터를 전체 그릇에 추가한다
    tmp.extend(dump)
#tmp


# In[36]:


import pymysql
from sqlalchemy import create_engine
import pandas as pd 
import pandas.io.sql as pSql
# 리스트 딕셔너리 구조
df_dict = pd.DataFrame.from_dict( tmp )
df_dict


# In[37]:


# 디비 접속
db_url = 'mysql+pymysql://{$아이디}:{$비번}@127.0.0.1/python_db' # 아이디(root):비번(root)
engine = create_engine( db_url, encoding='utf8' )
conn   = engine.connect()
# 디비에 밀어 넣기
df_dict.to_sql( name='movie_rank', con=conn , 
               if_exists='append', index=False) 


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




