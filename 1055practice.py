# # # # # current_number=0
# # # # # while current_number<10:
# # # # #     current_number=current_number+1
# # # # #     if current_number%2==0:
# # # # #         continue
# # # # #     else:
# # # # #         print(current_number)
# # # # #
# # # # # x=1
# # # # # while x<6:
# # # # #     print(x)
# # # # #     x +=1
# # # #
# # # # while True:
# # # #     age_input = input("请输入您的年龄：")
# # # #     age = int(age_input)  # 将输入的字符串转换为整数
# # # #
# # # #     if age < 3:
# # # #         print("票价：免费")
# # # #     elif 3 <= age <= 12:
# # # #         print("票价：10 美元")
# # # #     else:
# # # #         print("票价：15 美元")
# # # #
# # # #         prompt = "请输入您的年龄（输入 'quit' 退出）："
# # # #         active = True
# # # #
# # # #
# # # #     prompt = "请输入您的年龄（输入 'quit' 退出）："
# # # #     message = input(prompt)
# # # #
# # # #     while message != 'quit':
# # # #         age = int(message)
# # # #         if age < 3:
# # # #             print("票价：免费")
# # # #         elif 3 <= age <= 12:
# # # #             print("票价：10 美元")
# # # #         else:
# # # #             print("票价：15 美元")
# # # #
# # # #         message = input(prompt)
# # # #
# # # #
# # # #
# # # #
# # # #
# # # #
# # # #
# # # #     while True:
# # # #         age_input = input("请输入您的年龄：")
# # # #         age = int(age_input)  # 将输入的字符串转换为整数
# # # #
# # # #         if age < 3:
# # # #             print("票价：免费")
# # # #         elif 3 <= age <= 12:
# # # #             print("票价：10 美元")
# # # #         else:
# # # #             print("票价：15 美元")
# # # #
# # # #             prompt = "请输入您的年龄（输入 'quit' 退出）："
# # # #             active = True
# # # #
# # # #
# # # #         prompt = "请输入您的年龄（输入 'quit' 退出）："
# # # #         active = True
# # # #
# # # #         while active:
# # # #             message = input(prompt)
# # # #
# # # #             if message == 'quit':
# # # #                 active = False  # 改变变量状态，结束循环
# # # #             else:
# # # #                 age = int(message)
# # # #                 if age < 3:
# # # #                     print("票价：免费")
# # # #                 elif 3 <= age <= 12:
# # # #                     print("票价：10 美元")
# # # #                 else:
# # # #                     print("票价：15 美元")
# # # #
# # # #         while True:
# # # #             age_input = input("请输入您的年龄：")
# # # #             age = int(age_input)  # 将输入的字符串转换为整数
# # # #
# # # #             if age < 3:
# # # #                 print("票价：免费")
# # # #             elif 3 <= age <= 12:
# # # #                 print("票价：10 美元")
# # # #             else:
# # # #                 print("票价：15 美元")
# # # #
# # # #                 prompt = "请输入您的年龄（输入 'quit' 退出）："
# # # #                 active = True
# # # #
# # # #             prompt = "请输入您的年龄（输入 'quit' 退出）："
# # # #
# # # #             while True:
# # # #                 message = input(prompt)
# # # #
# # # #                 if message == 'quit':
# # # #                     break  # 直接跳出循环
# # # #
# # # #                 age = int(message)
# # # #                 if age < 3:
# # # #                     print("票价：免费")
# # # #                 elif 3 <= age <= 12:
# # # #                     print("票价：10 美元")
# # # #                 else:
# # # #                     print("票价：15 美元")
# # # #
# # # #                     while True:
# # # #                         print("无限循环！。")
# # #
# # #
# # #
# # # """"""class Solution:
# # #     def Sum(self, nums, target):
# # #         n = len(nums)
# # #         for i in range(n):
# # #             for j in range(i + 1, n):
# # #                 if nums[i] + nums[j] == target:
# # #                     return [i, j]
# # #         return []
# # #
# # #
# # # if __name__ == "__main__":
# # #
# # #     nums_input = [2, 7, 11, 15]
# # #     target_input = 9
# # #     # 示例 1
# # #     solver = Solution()
# # #     result = solver.Sum(nums_input, target_input)
# # #
# # #     print(f"输入: nums = {nums_input}, target = {target_input}")
# # #     print(f" {result}")
# # #
# # #
# # #
# # # def rem(nums):
# # #     if not nums:
# # #         return 0
# # #     slow = 0
# # #     for fast in range(1, len(nums)):
# # #         if nums[fast] != nums[slow]:
# # #             slow += 1
# # #             nums[slow] = nums[fast]
# # #
# # #     return slow + 1
# # #
# # #
# # # if __name__ == "__main__":
# # #     num1 = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
# # #
# # #     # 调用定义的函数
# # #     k = rem(num1)
# # #     # 打印结果
# # #     print("返回的长度 k =", k)
# # #     print("修改后的数组前 k 个元素 =", num1[:k])
# # #
# # #
# # # def tanheqin(name):
# # #     print(tanheqin)
# # #
# # #     realname = 'technoblade'
# # #     tanheqin(realname)
# # #
# # # a=6
# # # b=2
# # # def add(a,b):
# # #     add=a+b
# # #     return add
# # # print(add(a,b))
# # #
# # #
# #
# # def display_message():
# #     print("Hello World")
# # display_message()
# #
# # def favorite_number(title):
# #     return "ur favorite book is"+ title
# # print(favorite_number(" allce in wonderland"))
# #
# # #
# # def pet(animal,pet):
# #     print("i have a"+ animal+".")
# #     print("my"animal+"'s name is"+pet)
# #
# # pet(animal"cat",pet"dog")
#
# def make (size,color):
#     print(f"the size is{size}.the color is {color}.")
#
# make(10,"red")
# make(size="small",color="blue")
# make(size="medium",color="yellow")
#
# def make_shirt(size='L', message='I love Python'):
#     print( f"{size} 码的T恤，印有字样：'{message}'。")
#
#
# def city(city, country='iceland'):
#     print(f"{city} is in {country}.")
#
# city('zarbark')
# city('xquree')
#
# city('Beijing', 'China')


def show_messages(messages):
    for message in messages:
        print(message)
messages = ['你好', '今天天气不错', '晚上一起吃饭吗？']
show_messages(messages)

def send_messages(messages, sent_messages):

    while messages:
        current_message = messages.pop()
        print(f"正在发送: {current_message}")
        sent_messages.append(current_message)

messages = ['你好', '今天天气不错', '晚上一起吃饭吗？']
sent_messages = []

send_messages(messages, sent_messages)
print("\n原始消息列""）:", messages)
print("已发送消息列表:", sent_messages)

def send_messages(messages, sent_messages):
    while messages:
        current_message = messages.pop()
        print(f"正在发送: {current_message}")
        sent_messages.append(current_message)

messages = ['你好', '今天天气不错', '晚上一起吃饭吗？']
sent_messages = []

send_messages(messages[:], sent_messages)
print("\n原始消息列表（应保留所有消息）:", messages)
print("已发送消息列表:", sent_messages)

