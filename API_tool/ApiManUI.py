import tkinter as tk
from APIManModule import APIManModule


class ApiManUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("接口管理工具")
        self.create_widgets()

        # 初始化ApiManModule对象
        self.api_man = APIManModule()

    def create_widgets(self):
        # 创建标签和输入框，用于输入接口信息
        tk.Label(self.master, text="接口名称：").grid(row=0)
        self.name_entry = tk.Entry(self.master)
        self.name_entry.grid(row=0, column=1)
        tk.Label(self.master, text="请求方式：").grid(row=1)
        self.method_entry = tk.Entry(self.master)
        self.method_entry.grid(row=1, column=1)
        tk.Label(self.master, text="请求URL：").grid(row=2)
        self.url_entry = tk.Entry(self.master)
        self.url_entry.grid(row=2, column=1)
        tk.Label(self.master, text="请求头信息：").grid(row=3)
        self.headers_entry = tk.Entry(self.master)
        self.headers_entry.grid(row=3, column=1)
        tk.Label(self.master, text="请求参数：").grid(row=4)
        self.params_entry = tk.Entry(self.master)
        self.params_entry.grid(row=4, column=1)

        # 创建按钮，用于提交接口信息和查询接口信息
        self.add_button = tk.Button(self.master, text="提交", command=self.add_api)
        self.add_button.grid(row=5, column=0)
        self.query_button = tk.Button(self.master, text="查询", command=self.query_api)
        self.query_button.grid(row=5, column=1)

        # 创建文本框，用于显示查询结果
        self.result_text = tk.Text(self.master, width=60, height=10)
        self.result_text.grid(row=6, columnspan=2)

    def add_api(self):
        # 获取用户输入的接口信息
        name = self.name_entry.get()
        method = self.method_entry.get()
        url = self.url_entry.get()
        headers = self.headers_entry.get()
        params = self.params_entry.get()

        # 调用ApiManModule中的add_api方法添加接口信息
        self.api_man.add_api(name, method, url, headers, params)

    def query_api(self):
        # 获取用户输入的接口名称
        name = self.name_entry.get()

        # 调用ApiManModule中的query_api方法查询接口信息
        result = self.api_man.query_api(name)

        # 将查询结果显示在文本框中
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)


if __name__ == '__main__':
    root = tk.Tk()
    app = ApiManUI(root)
    app.mainloop()
