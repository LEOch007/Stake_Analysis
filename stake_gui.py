#  @copyright
#  linjialiang 2018/8/12
#  Github: LEOch007

from tkinter import *
import tkinter.messagebox as messagebox

# 预处理
def preprocess(filepath):
    # 读入数据
    with open(filepath, 'r') as f:
        str_f = f.readlines()

    # 找到操作数据区间
    rows = []
    for i in range(len(str_f)):
        try:
            num = int(str_f[i].split(',')[0]) #首个数据为股票编码
            rows.append(i)
        except:
            pass
    min_row = min(rows)
    max_row = max(rows)

    return str_f,min_row,max_row

# 提取信息
def extract_data(str_f,min_row,max_row):
    #获取结构体list
    stake_list = [] 
    for i in range(min_row,max_row+1):
        stake_list.append(str_f[i].split(',')[0:3])

    #排序
    sorted_list = sorted(stake_list, key=lambda s:float(s[2]),reverse=True)

    return sorted_list

# 主逻辑
def handler(file5,file10,file15,outputfile,up_num,down_num):
    #读取5天文件
    str_f1,m1,M1 = preprocess(file5)

    #提取数据
    sorted_list1 = extract_data(str_f1,m1,M1)
    
    #获取兴趣股票代码
    stake_code = []
    result_list = []
    for i in range(up_num):
        stake_code.append(int(sorted_list1[i][0]))
        result_list.append(sorted_list1[i])
    for j in range(1,down_num+1):
        stake_code.insert(up_num,int(sorted_list1[-j][0]))
        result_list.insert(up_num,sorted_list1[-j])

    
    #读取10天文件
    str_f2,m2,M2 = preprocess(file10)

    #提取数据
    sorted_list2 = extract_data(str_f2,m2,M2)
    
    #遍历查找兴趣股票
    for i in range(len(sorted_list2)):
        code = int(sorted_list2[i][0])
        try:
            idx = stake_code.index(code)
            result_list[idx].append(sorted_list2[i][2]) #涨幅
            if idx<up_num:
                result_list[idx].append(i+1) #顺向排名
            else:
                result_list[idx].append(len(sorted_list2)-i) #逆向排名
        except:
            pass

    #读取15天文件
    str_f3,m3,M3 = preprocess(file15)

    #提取数据
    sorted_list3 = extract_data(str_f3,m3,M3)
    
    #遍历查找兴趣股票
    for i in range(len(sorted_list3)):
        code = int(sorted_list3[i][0])
        try:
            idx = stake_code.index(code)
            result_list[idx].append(sorted_list3[i][2]) #涨幅
            if idx<up_num:
                result_list[idx].append(i+1) #顺向排名
            else:
                result_list[idx].append(len(sorted_list3)-i) #逆向排名
        except:
            pass


    #写文件
    with open(outputfile, 'w') as f:
        f.write('CODE,NAME,5D,10D,,15D\n')
        for i in range(len(result_list)):
            if i==up_num:
                f.write('\n') #空行隔开
            for j in range(len(result_list[0])):
                if (j==2)or(j==3)or(j==5):
                    f.write(str(result_list[i][j])+'%,')
                else:
                    f.write(str(result_list[i][j])+',')
            f.write('\n')
    
# 点击事件
def onclick():
    # 数据文件地址
    file5 = './'+e1.get()+'.csv'
    file10 = './'+e2.get()+'.csv'
    file15 = './'+e3.get()+'.csv'
    outputfile = './'+e_o.get()+'.csv'
    # 参数
    up_num = int(e_up.get())
    down_num = int(e_down.get())
    # 执行逻辑
    handler(file5,file10,file15,outputfile,up_num,down_num)
    # UI提示
    messagebox.showinfo('Message', '数据已提取！')

if __name__ == '__main__':
    
    root = Tk()      #布局
    e1 = Entry(root) #输入控件
    e2 = Entry(root)
    e3 = Entry(root)
    e_up = Entry(root)
    e_down = Entry(root)
    e_o = Entry(root)

    Label(root,text="5日数据：").grid(row=0,padx=5,pady=8) #第一行
    e1.grid(row=0,column=1,padx=10)
    Label(root,text="涨股数量：").grid(row=0,column=2,padx=5,pady=8)
    e_up.grid(row=0,column=3,padx=10)
    
    Label(root,text="10日数据：").grid(row=1,padx=5,pady=8)#第二行
    e2.grid(row=1,column=1,padx=10)
    Label(root,text="跌股数量：").grid(row=1,column=2,padx=5,pady=8)
    e_down.grid(row=1,column=3,padx=10)
    
    Label(root,text="15日数据：").grid(row=2,padx=5,pady=8)#第三行
    e3.grid(row=2,column=1,padx=10)
    Label(root,text="输出文件：").grid(row=2,column=2,padx=5,pady=8)
    e_o.grid(row=2,column=3,padx=10)
    
    Button(root,text="执行提取",command=onclick).grid(row=3,column=3) #第四行
    
    root.title("股票涨幅数据提取")
    root.mainloop()
