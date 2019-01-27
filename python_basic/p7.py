# 2. 연속 데이터 > 집합
# set()
# 중복 제거, 딕셔너리는 적용 불가
# 리스트, 튜플에 적용가능
# 중복 제거후 정렬하지 않는다.
####################################
a = 'helloworld'
print(set(a))
a = set([1,2,4,3,12,5,2,1,5,7])
print(list(a))
####################################
# 차집합, 교집합, 합집합
a = set( [1, 3, 5, 7, 9, 9, 2, 4] )
b = set( [2, 4, 6, 8, 3, 7, 4, 2] )
# 중복 제거 여부
print( a, b )
# 합집합
print( a.union(b) )
# 교집합
print( a.intersection(b) )
# 차집합 : 빼는 방향이 중요
print( a.difference(b) ) # a-b
print( b.difference(a) ) # b-a
