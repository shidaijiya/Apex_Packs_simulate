import random
import time


def check_and_write_file(filename):
    try:
        # 'r+' 模式是为了读写，文件指针将会放在文件的开头
        with open(filename, 'r+') as file:
            # 读取文件内容
            contents = file.read()
            if not contents:  # 检查内容是否为空
                file.write('0,30,500')  # 写入内容
            else:
                pass
    except FileNotFoundError:
        # 如果文件不存在，'w' 模式将创建文件并写入
        with open(filename, 'w') as file:
            file.write('0,30,500')
    except IOError as e:
        # 捕获并打印其他可能的IO错误
        print(f"操作文件时发生错误: {e}")


def draw_lottery():
    prizes = ["稀有", "史诗", "传说", "神话"]
    probabilities_percent = [67.6, 24.8, 7.4, 0.2]
    total_probability = sum(probabilities_percent)
    probabilities = [percent / total_probability for percent in probabilities_percent]

    random_number = random.random()
    cumulative_probability = 0

    for i in range(len(prizes)):
        cumulative_probability += probabilities[i]
        if random_number < cumulative_probability:
            return prizes[i]


def rare_or_better():
    prizes = ["普通", "稀有"]
    probabilities_percent = [45.54, 46.53]
    total_probability = sum(probabilities_percent)
    probabilities = [percent / total_probability for percent in probabilities_percent]

    random_number = random.random()
    cumulative_probability = 0

    for i in range(len(prizes)):
        cumulative_probability += probabilities[i]
        if random_number < cumulative_probability:
            return prizes[i]


def augment_draws():
    with open('history.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()  # 去除行首尾的空白字符
            number_draws, next_legendary, next_mythical = line.split(',')
            number_draws = int(number_draws)
            next_legendary = int(next_legendary)
            next_mythical = int(next_mythical)
    number_draws += 1
    next_legendary -= 1
    next_mythical -= 1
    print(f"目前开箱{number_draws}次\n"
          f"距离下次传说级还有{next_legendary}次\n"
          f"距离下次传家宝碎片还有{next_mythical}次")
    with open('history.txt', 'w+') as file:
        new_data = f'{number_draws},{next_legendary},{next_mythical}'
        file.write(new_data)
        file.close()


def legendary():
    legendary_appear = False
    with open('history.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()  # 去除行首尾的空白字符
            number_draws, next_legendary, next_mythical = line.split(',')
            number_draws = int(number_draws)
            next_legendary = int(next_legendary)
            next_mythical = int(next_mythical)
    if next_legendary == 0:
        legendary_appear = True
        with open('history.txt', 'w+') as file:
            new_data = f'{number_draws},30,{next_mythical}'
            file.write(new_data)
            file.close()
    else:
        pass

    return legendary_appear


def mythical():
    mythical_appear = False
    with open('history.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()  # 去除行首尾的空白字符
            number_draws, next_legendary, next_mythical = line.split(',')
            number_draws = int(number_draws)
            next_legendary = int(next_legendary)
            next_mythical = int(next_mythical)
    if next_mythical == 0:
        mythical_appear = True
        with open('history.txt', 'w+') as file:
            new_data = f'{number_draws},{next_legendary},500'
            file.write(new_data)
            file.close()
    else:
        pass
    return mythical_appear


def set_mythical():
    with open('history.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()  # 去除行首尾的空白字符
            number_draws, next_legendary, next_mythical = line.split(',')
            number_draws = int(number_draws)
            next_legendary = int(next_legendary)
    with open('history.txt', 'w+') as file:
        new_data = f'{number_draws},{next_legendary},500'
        file.write(new_data)
        file.close()


def start_draw():
    list_result = []
    legendary_appear = legendary()
    mythical_appear = mythical()
    if mythical_appear == True:
        list_result.append("传家宝碎片*50,传家宝碎片*50,传家宝碎片*50")
    else:
        for i in range(3):
            lottery_result = draw_lottery()
            better_result = rare_or_better()
            if lottery_result == '稀有':
                list_result.append(better_result)
            elif lottery_result == '神话':
                list_result.clear()
                list_result.append("传家宝碎片*50,传家宝碎片*50,传家宝碎片*50")
                set_mythical()
                break
            elif legendary_appear == True:
                list_result.append('传说')
            else:
                list_result.append(lottery_result)
    augment_draws()
    return list_result


check_and_write_file('history.txt')
print("                      《声明》\n"
      "概率依照Apex Ledgends游戏公示概率\n"
      "稀有或更好100% , 史诗24.8% , 传说7.4% , 神话>1% 即0.2%\n"
      "此代码与Electronic Arts Inc.和Respawn Studio Inc.\n"
      "无任何关系,仅供娱乐")
for i in range(100):  # 修改里面数字设置连抽次数
    print('------------------------')
    list_result = start_draw()
    print(list_result)
    time.sleep(0.5)  # 修改里面数字设置连抽间隔时间
