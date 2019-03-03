#!/usr/bin/env python
# coding: utf-8

# ### 대상
# * 로그인이나, 첨부 파일 등 사용자의 개입이 안되는 케이스
# * 그냥 사이트를 긁어서 원하는 데이터를 추출하는 방식

# * 목표
# > 사이트 긁기 <br>
# > html 파싱 처리 (BS4) <br>
# > 데이터 적재 <br>
# > 스케줄링(윈도우 스케줄러, 리눅스 cron)
# 

# * 대상 사이트
#     > 네이버 환율 사이트 <br>
#     > https://finance.naver.com/marketindex/exchangeList.nhn

# In[12]:


from urllib.request import urlopen
from bs4 import BeautifulSoup


# In[15]:


# 요청 -> html 획득
url_base = 'https://finance.naver.com/marketindex/exchangeList.nhn'
# 요청
page     = urlopen(url_base) #아무것도 없이 요청하면 get방식
page


# In[17]:


# 응답 객체를 BS에 넣어서 DOM 트리로 올린다(html 객체를 메모리로 로드)
# 1번 인자는 html 문자열, html 응답객체
# 2번 인자는 파싱(html에서 원하는 데이터를 추출) 엔진 종류
# html.parser로 사용 -> 만약 안되면 html5lib사용
soup = BeautifulSoup( page, 'html.parser')
soup


# In[96]:


# 모든 통화명 추출 -> 통화명을 찾아서, 추출해라
# body > div > table > tbody > tr:nth-child(1) > td.tit
# td.tit
# 이 문서상에 존재하는 모든 td중에 class가 tit인 요소만 모아라
tits = soup.select('td.tit')
print(type(tits), len(tits)) # list->for문 돌려서 뽑는다1!


# In[30]:


titles = list()
for tit in tits:
    # print( tit.a.string.strip() ) 
    titles.append(tit.a.string.strip())
# 코드를 개선해서 통화 목록을 리스트로 모아서 출력하시오
# ['미국 USD','유럽연합 EUR', ... ]
titles[:2]


# In[32]:


# 리스트내 for를 활용하여 출력 형식을 맞춘다.(간단하게)
titles = [tit.a.string.strip() for tit in soup.select('td.tit')]
titles[:2]


# In[45]:


# 통화에 걸려있는 링크값 획득
# tit => <td class='tit'>  .....  </td>
# td>a의 href 속성값
# marketindexCd=FX_USDKRW
# 링크에서 환율별 고유 코드를 획득
# ~/marketindex/exchangeDetail.nhn?
# marketindexCd=고유코드 => 당일 고시차수별 환율 변동정보
for tit in tits: # split() 아무것도 안쓰면 공백으로 쪼갠다!!
    print( 
        {
           'na':  tit.a.string.strip().split()[0],
           'code': tit.a.string.strip().split()[-1],
           'ncode': tit.a['href'].split('=')[-1] 
       }    
       )
# 최종 결과물을 리스트 딕셔너리 형태로 출력하시오
# [ {}, {}, {} ]
# 한줄로 해도 ok, 지금 코드를 변형해도 ok


# In[47]:


# 무난하게 데이터 정제 작업
results   = list()
for tit in tits: # split() 아무것도 안쓰면 공백으로 쪼갠다!!
    tmp   = tit.a.string.strip().split()
    na    = tmp[0]
    code  = tmp[-1]
    ncode = tit.a['href'].split('=')[-1]
    dic   = {'na':na, 'code':code, 'ncode':ncode}
    #print(dic)
    results.append(dic)
print(results)


# In[55]:


# results = [리스트멤버 반복문 (조건문)]
results = [
    {
        'na':  tit.a.string.strip().split()[0],
        'code': tit.a.string.strip().split()[-1],
        'ncode': tit.a['href'].split('=')[-1] 
    }
    for tit in tits
]
results


# In[59]:


# 매매 기준율 데이터를 뽑아서
# 최종적인 데이터 1개의 구조
'''
    {
        'na': '미국', 
        'code': 'USD', 
        'ncode': 'FX_USDKRW'
        'stdSell':1,125.40
    }
'''
print(len(tits))
print( len(soup.select('td') ))
print( '환율정보 한 row에 존재하는 총 td개수(데이터종류개수)'
      , len(soup.select('td') )/len(tits))


# In[94]:


tds = soup.findAll('td')
print( len(tds) )
# i: 인덱스, td: 데이터 덩어리
# enumerate()는 데이터의 순서를 같이 리턴해줘서
# 인덱스를 활용한 연산 처리에 도움을 준다.
results = list()
for i, td in enumerate(tds): # 7의 배수로 세트가(환율 정보가 변경된다.)
    #print(i, td)
    # 기준 매매가 출력 : 1, 8, 15, ... 번쨰 td의 텍스트값
    position = i%7
    if position==0: #통화명 정보
        dic = { 'na':  td.a.string.strip().split()[0],
                'code': td.a.string.strip().split()[-1],
                'ncode': td.a['href'].split('=')[-1] }
        # 통화 정보 추가 (딕셔너리구조)
        results.append(dic)
    elif position==1:
        # results의 마지막 멤버(방금추가된세트)
        # 그 구조에 기준매매가 추가
        results[-1]['stdSell']=td.string.strip() # 방금 추가된 것은 -1번째!!
results


# In[ ]:




