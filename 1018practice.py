# from collections.abc import async_generator
#
# points=["e","w","r","s","a"]
# for point in points:
#     print(point)
#     #for循環完全忘記是啥意思了..哦哦是遍歷列表
#
#
# #這個是依照大小由小到大升序排序
# points.sort()
# print(points)
#
# #似乎是希望列表整個反向
# points.reverse()
# print(points)
#
# #這個是依照大小由大到小降序排序
# points.sort(reverse=True)
# print(points)
#
# #那這裏應該就會輸出上一個的按照字符串的反向的
# points.reverse()
# print(points)
#
#
# #youtubers2=[2,3,4]
# #youtubers2.sort(reverse=True)
# #print(youtubers2)
#
# youtubers=["wrx","hzx","xjr"]
# print(len(youtubers))
#
# for youtuber in youtubers:
#     print(youtuber)
#     #進行一些邊歷
#
# for youtuber in youtubers:
#     q="l dont like " + youtuber
#     print(q)
#     #同一句話
#
# animals=["cat","dog"]
# for animal in animals:
#     print(animal)
#     for animal in animals:
#         print("idk about",animal)
# #這個練習説是讓我用for循環打印動物名稱，
# #然後針對每種動物再打印一個句子，我不太理解想幹嘛，意思是每個句子要不一樣嗎
#
# animals = ["cat", "dog"]
# for animal in animals:
#     print(animal)
#     print(f"I like {animal}s.")   # 針對這一種動物講一句話,這是ds說的但我還是不理解
#
# animals = ["cat", "dog"]
# traits = ["cute", "loud"]
# #每種動物配一個特徵嗎
# for animal in animals:
#     print(animal)
#     for trait in traits:
#         print(f"  {animal} is {trait}.")
#
#
#
# for vw in range(1,11,1):
#     print(vw)
#
# numbers=list(range(2,11,2))
# print(numbers)
# #偶數按照列表打印出來
# for number in numbers:
#     print(number)
# #一個一個打印
#
#
#
# egg_chans=[]
# #定義一個空列表等會裝元素進去
# numbers=list(range(2,11))
# #再次定義一個
# for number in numbers:
#     value=number**2
#     #進行一些平方
#     egg_chans.append(value)
# print(egg_chans)
#
# for nums in range(1,11,2):
#         print(nums)
#
#
# for numbers in range(1,21):
#     print(numbers)
# #數到20
#
# for numbers in range(1,100):
#     print(numbers)
#
# wemmbu=[]
# for s in range(1,101):
#     wemmbu.append(s)
# print(wemmbu)
# #把1-1000放進wemmbu裏面去
#
# print("最小值:", min(wemmbu))
# print("最大值:", max(wemmbu))
#
# numbers=list(range(1,21,2))
# print(numbers)
# for number in numbers:
#     print(number)
# #奇數
#
# numbers=list(range(3,31,3))
# print(numbers)
# for number in numbers:
#     print(number)
# #3倍數
#
# parrotx2=[]
# #定義一個空列表裝立方
# numbers=list(range(1,11))
# #用變數命名一些數字列表出來
# for number in numbers:
#     x2=number**3
#     #定義一些x2的變數的概念
#     parrotx2.append(x2)
#     #插入進去
# print(parrotx2)
# #立方
#
# youtubers = ["wrx", "hzx", "xjr"]
# for youtuber in youtubers:
#     if youtuber != "hzx":
#         print("well i dont care about " + youtuber + ".")
#     else:
#         print("OMG I like " + youtuber + ".")
#
# age=10
#
# if age<0:
#     print("age is less than 0,thank you.")
# elif age<18 and age>=0:
#     print("your addmission fee is 20")
# elif age >= 18 and age <= 30:
#     print("your addmission fee is 60")
# else :
#     print("your addmission fee is 80")
#
# #or
# age=50
#
# if age<0:
#     print("age is less than 0,thank you.")
# elif age <= 18 and age >= 0:
#     price=30
# elif age > 18 and age <= 20:
#     price=40
# else:
#     price = 80
# #     print(f"your addmission fee is {price}.")
# #
#
# alien_colors=['green','yellow','red']
# alien_color=alien_colors[0]
# if alien_color=='green':
#     print("got 5 points.")
# #外星人顔色
#
# alien_colors=['green','yellow','red']
# alien_color=alien_colors[1]
# if alien_color=='green':
#     print("got 5 points.")
# else:
#     print("got 10 points.")
# #外星人顔色2
#
# alien_colors=['green','yellow','red']
# alien_color=alien_colors[0]
# if alien_color=='green':
#     print("got 5 points.")
# elif alien_color=='yellow':
#     print("got 10 points.")
# else:
#     print("got 15 points.")
#
# alien_colors=['green','yellow','red']
# alien_color=alien_colors[1]
# if alien_color=='green':
#     print("got 5 points.")
# elif alien_color=='yellow':
#     print("got 10 points.")
# else:
#     print("got 15 points.")
#
# alien_colors=['green','yellow','red']
# alien_color=alien_colors[2]
# if alien_color=='green':
#     print("got 5 points.")
# elif alien_color=='yellow':
#     print("got 10 points.")
# else:
#     print("got 15 points.")
#
# #外星人顔色3
#
# age=21
# if age<2:
#     print("A baby.")
# elif age<4 and age>=2:
#     print("A chlid.")
# elif age<13 and age>=4:
#     print("An older child.")
# elif age < 18 and age >= 13:
#     print("A teenager.")
# elif age <65 and age >= 18:
#     print("A man.")
# else:
#     print("A old man.")
# #年齡
#
# favourite_fruits=['apples','bananas','oranges']
# for fruit in favourite_fruits:
#     if fruit == 'apples':
#         print(f'you really like {fruit}.')
#     elif fruit == 'bananas':
#         print(f'you really like {fruit}.')
#     else:
#         print(f'you really like {fruit}.')

# a=4
# b=2
# c=3
# m=max(a,max(b,c))
# n=min(a,min(b,c))
# print(m,'是最大')
# print(n,'是最小')

# name=input("Enter your name: ")
# print("hello,"+name)
#
# height=int(input("Enter your height: "))
# if height>=55:
#     print("you are so tall.")
# else:
#     print("////you are so cute////")
#
#
# name=input("Enter ur favourite car: ")
# if name=='beyond':
#     print('let m see if i can find u a beyond')
# else:
#     print('u r fucking an idlot! NOBODY WOULD NOT CHOOSE BYD')
#
# name=int(input("Enter ur how many people will come here: "))
# if name>=8:
#     print('No,there is no kong zhuo')
# else:
#     print('come here! PLZ')
#
# name=int(input("Enter a num: "))
# if name%10==0:
#     print('yes')
# else:
#     print('no')


