# 1
print("techno once said:technoblade never dies!")

# 呵呵这一集好地狱
# 老大我们写这么多注释真的会给分吗
# 及格万岁

# 2
cities=["lanzhou","yuzhong","tianshui"]
print(cities[0])
print(cities[1])
print(cities[2])
# ok啊这个大写怎么搞我也是完全忘记了，呵呵


# 3(1)
guests = ['苏轼', '达·芬奇', '阿兰·图灵']
for guest in guests:
    print(f"{guest}，噢噢我呢也是想邀请您共进晚餐呀。")

# 3(2)
absent = '达·芬奇'
print(f"很遗憾，{absent} 临时有事，无法赴约。")
guests[guests.index(absent)] = '爱因斯坦'
print("新的邀请名单如下：")
for guest in guests:
    print(f"{guest}，诚挚邀请您与我共进晚餐。")

# 3(3)
guests = ['老子', '苏轼', '居里夫人', '爱因斯坦', '图灵', '白居易']
print("找一大桌，可邀更多客人！")
guests.insert(0, 'wangruoxi')
guests.insert(len(guests)//2, 'wangaoqing')
guests.append('wangtianqi')
for guest in guests:
    print(f"{guest}邀共餐。")

# 3(4)
guests = ['老子', '苏轼', '居里夫人', '爱因斯坦', '图灵', '白居易']

print("新餐桌无法及时送达，只邀两位嘉宾。")

del guests[1]

while len(guests) > 2:
    guest = guests.pop()
    print(f"抱歉，{guest}，这次无法邀请共进晚餐了。")

for guest in guests:
    print(f"{guest}，仍在邀请名单上。")

del guests[:]


# 4
sixs = list(range(6, 61, 6))
for number in sixs:
    print(number)


# 5
numbers = list(range(0, 21, 2))
print(f"1～20 的偶数共 {len(numbers)} 个：")
for number in numbers:
    print(number)


# 6三数比对呵呵这个我一直搞不明白我放弃了



# 7(1)

    print(f'你今年多大了')
    age = input()

    def stage_life(age):
        if age < 3:
            return "u r FREE！"
        elif age <=12:
            return "噢噢你需要被收费10美元"
        else:
            return "噢噢你需要被收费15美元。"


# 7(2)
    def ticket_message(age):
        if age < 3:
            return "噢噢免费"
        elif age <= 12:
            return "10 美元"
        else:
            return "15 美元"

    print("条件测试结束")
    age = input("请输入观众年龄（quit 退出）：")
    while age != 'quit':
        print(f"  票价：{ticket_message(int(age))}")
        age = input("请输入观众年龄（ quit 退出）：")

    print("active")
    active = True
    while active:
        age = input("请输入观众年龄（输入 quit 退出）：")
        if age == 'quit':
            active = False
        else:
            print(f"票价：{ticket_message(int(age))}")

    print("break 退出")
    while True:
        age = input("请输入观众年龄（输入 quit 退出）：")
        if age == 'quit':
            break
        print(f"  票价：{ticket_message(int(age))}")


# 8
def city_country(city, country):
    return f"{city.title()}, {country.title()}"
print(city_country('mango', 'thailand'))
print(city_country('chengdu', 'china'))
print(city_country('tokyo', 'nihongo'))


# # 9 加减乘除，两个参数
# a=float(input())
# b=float(input())
# c=a+b
# print(c)
# 呵呵我放弃了能不能不考数学呵呵呵呵我一直哭泣


# 10

class User:

    def __init__(self, first_name, last_name, age, gender):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender
#呵呵我真是一个对外国人友好的人
    def describe_user(self):
        print(f"姓名：{self.first_name} {self.last_name}")
        print(f"年龄：{self.age}　性别：{self.gender}")

    def greet_user(self):
        print(f"你好，{self.first_name} {self.last_name}，巴巴啦巴拉讨厌您来请问有什么不需要帮您？！")


users = [
    User('wang', 'ruoxi', 16, 'female'),
    User('wang', 'tianqi', 13, 'male'),
    User('Alice', 'Smith', 26, '一个沃尔玛塑料袋' ),]

for user in users:
    user.describe_user()
    user.greet_user()
    print()



