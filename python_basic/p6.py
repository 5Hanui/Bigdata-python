# 2. 연속 데이터 > 튜플
# (), tuple()
# 순서존재, 인덱스 사용가능, 중복ok
# 오직 값을 묶는다. 수정불가
# immutable. 함수의 리턴값으로 많이 사용
tu = ()
print(tu, type(tu), len(tu))
tu = tuple()
print(tu, type(tu), len(tu))
##########################################
# 데이터가 1개인 경우
tu = (1,)
print(tu, type(tu), len(tu))
tu = (1,3,5,7,9)
# 인덱싱
print( tu[0] )
# 슬라이싱
print( tu[1:-1] )
# 변수로 값을 하나씩 획득
a = tu[1:-1]
a1 = a[0]
a2 = a[1]
a3 = a[2]
print(a, a1, a2, a3)
a = (1,2,3)
b = (4,5,6)
print( a+b )
