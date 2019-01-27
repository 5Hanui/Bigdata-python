# 2. 연속 데이터 > 딕셔너리
# {}, dict()
# 순서가 없다 => 키와 값의 쌍으로(세트) 구성원이
# 구성된다. 키는 절대로 중복되면 안된다.
# 값은 중복되도 ok,
dic = {}
dic2 = dict()
print(dic, dic2, type(dic), len(dic))
dic = {
    'name': 'multi',
    'age': 10
}
print(dic)
