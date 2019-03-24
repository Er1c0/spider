import requests
import re
import pymysql
import time as timer


class Bym:
    def __init__(self):
        """初始化清空数据库"""
        self.conn = pymysql.Connect(host='localhost',
                                    port=3306,
                                    user='root',
                                    password='123456',
                                    db='t',
                                    charset='utf8')
        self.cur = self.conn.cursor()

        self.cur.execute("TRUNCATE TABLE test")
        self.conn.commit()

    def html_insert(self,list_x):
        """数据插入数据库"""
        sql_insert = "INSERT INTO test(link,time,title) VALUES (%s,%s,%s)"
        self.cur.executemany(sql_insert, list_x)
        self.conn.commit()
        print("下载成功")

    def splitlines(self, table):
        """每元组的第一个数据加链接头，组成新列表"""
        list_x=[]
        for i in range(len(table)):
            tuple_x1='http://8ym.cn'+table[i][0]
            tuple_x=[tuple_x1,table[i][1],table[i][2]]
            list_x.append(tuple_x)
        self.html_insert(list_x)
    def regex(self, html):
        """正则匹配"""
        table = re.findall(r'<a href="(/rpt/1.*?)" class="list-group-item"><span class="badge today">(.*?)</span>(.*?)</a>', html,
            re.S)
        self.splitlines(table)
    def html(self):
        """获取网页数据"""
        h1 = {'user-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0'}
        for i in range(1, 2):
            url = 'http://8ym.cn/rptlist/{}'.format(i)
            r = requests.get(url, headers=h1)
            html = r.content.decode()
            self.regex(html)

    def add(self):
        print("您选择的操作是【增加线报】")
        link_str = input("请输入链接：")
        link_str = "http://" + link_str
        time = timer.strftime("%H:%M:%S")
        title_str = input("请输入标题：")
        card_dict = [link_str, time, title_str]
        sql_insert = "INSERT INTO test(link,time,title) VALUES (%s,%s,%s)"
        self.cur.execute(sql_insert, card_dict)
        self.conn.commit()
        print("添加成功")

    def delete(self):
        print("您选择的操作是【删除线报】")
        while True:
            find_id = input("请输入要删除的id：")
            if find_id.isdigit() is False:
                print("输入有误,请重新输入")
                continue
            find_id = int(find_id)
            if find_id == 999:
                return
            sql = "SELECT * FROM test where id=%d"
            self.cur.execute(sql % find_id)
            if self.cur.rowcount == 0:
                print("未找到,请重新输入")
                continue
            if self.cur.rowcount > 0:
                break
        sql_delete = "DELETE FROM test WHERE id=%s"
        self.cur.execute(sql_delete, find_id)
        self.conn.commit()
        print("删除成功")

    def search(self):
        print("您选择的操作是【查询线报】")
        while True:
            find_title = input("请输入要查询的线报：")
            break
        sql = "SELECT * FROM test where title LIKE '%%%s%%'"
        self.cur.execute(sql % find_title)
        if self.cur.rowcount == 0:
            print("未找到")
        if self.cur.rowcount > 0:
            # 打印执行结果的条数
            print('为您找到的线报条数为 %d' % self.cur.rowcount)
            print("id  链接                       时间      标题")
            rr = self.cur.fetchall()  # 将所有的结果放入rr中
            # 对结果进行处理
            for row in rr:
                print("%2d  %-25s  %s  %s" % row)
    def update(self):
        print("您选择的操作是【修改线报】")
        while True:
            find_id = input("请输入要修改的id：")
            if find_id.isdigit() is False:
                print("输入有误,请重新输入")
                continue
            find_id = int(find_id)
            if find_id == 999:
                return
            sql = "SELECT * FROM test where id=%d"
            self.cur.execute(sql % find_id)
            if self.cur.rowcount == 0:
                print("未找到,请重新输入")
                continue
            if self.cur.rowcount > 0:
                row = self.cur.fetchone()
                link_str = input("请输入要修改的链接：")
                time = input("请输入要修改的时间：")
                title_str = input("请输入要修改的标题：")
                link_str = "http://" + link_str
                if len(link_str) == 7:
                    link_str = row[1]
                if time == "":
                    time = row[2]
                if title_str == "":
                    title_str = row[3]
                card_dict = [link_str, time, title_str, int(find_id)]
                sql_update = "UPDATE test SET link=%s,time=%s,title=%s WHERE id=%s"
                self.cur.execute(sql_update, card_dict)
                self.conn.commit()
                print("修改成功")
                break

    def show(self):
        sql = "SELECT *FROM test"
        self.cur.execute(sql)
        # 打印执行结果的条数
        print('当前线报条数为 %d' % self.cur.rowcount)
        if self.cur.rowcount > 0:
            print("id  链接                       时间      标题")
        rr = self.cur.fetchall()  # 将所有的结果放入rr中
        # 对结果进行处理
        for row in rr:
            print("%2d  %-25s  %s  %s" % row)

    def exit_system(self):
        self.conn.close()
        self.cur.close()


person = Bym()
while True:
    print("**" * 23)
    str1 = ["欢迎使用【线报管理系统】ｖ1.0", "1. 增加线报", "2. 删除线报", "3. 查询线报",
            "4. 修改线报", "5. 显示所有", "6. 下载线报", "0. 退出系统"]
    for s in str1:
        print("|%s|" % s.center(25, "　"))
    print("**" * 23)
    print(">" * 8, end=" ")
    action_str = input("请选择希望执行的操作：")
    if action_str in ["1", "2", "3", "4", "5", "6"]:
        if action_str == "1":
            person.add()
        elif action_str == "2":
            person.delete()
        elif action_str == "3":
            person.search()
        elif action_str == "4":
            person.update()
        elif action_str == "5":
            person.show()
        elif action_str == "6":
            person.html()
    elif action_str == "0":
        person.exit_system()
        print("您选择的操作是【退出系统】")
        print("欢迎再次使用【线报管理系统】")
        break
    else:
        print(">" * 8, end=" ")
        print("您输入的不正确，请重新选择")
