import re
import os
import tkinter as tk
from tkinter import filedialog


def main(origin_path, to_path, file_name, add_name):
    with open(os.path.join(origin_path, file_name), mode="r", encoding="utf-8") as f:
        s = f.read()

    def add(match) -> str:
        address = match.group()
        addition = r"{{ url_for('static', filename='" + address + r"') }}"
        return addition

    # repl 如果它是可调用的函数对象，则传递match对象，并且必须返回要使用的替换字符串
    x = re.sub(r'assets/.*?(\.css+|\.png|\.jpg|\.js)', add, s)
    # print(x)

    if not os.path.exists(to_path):
        os.makedirs(to_path)
        print("创建新的文件夹")

    with open(os.path.join(to_path, add_name + file_name), mode="w", encoding="utf-8") as f:
        f.write(x)
        return True


def cmd():
    while True:
        path = input("Path: ")
        state = main(path)
        if state:
            print("SUCCESS!")


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.files, self.folders = None, None
        self.paths = []
        self.title("html url_for interpreter")  # #窗口标题
        # self.geometry("600x300")

        tk.Button(self, text='打开文件', width=20, command=self.select_file).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(self, text='打开文件夹', width=20, command=self.select_folder).grid(row=1, column=1, padx=5, pady=5)

        self.listbox = tk.Listbox(self, setgrid=True, width=60, selectmode=tk.EXTENDED)
        self.listbox.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
        # 删除选项
        delete_button = tk.Button(self, text='删除', width=10, command=self.delete)
        delete_button.grid(row=1, column=2, padx=5, pady=5)

        tk.Label(self, text="\t\t前缀").grid(row=3, column=0, pady=10)
        self.entry_text = tk.StringVar(self, value="inter_")
        tk.Entry(self, textvariable=self.entry_text).grid(row=3, column=1, pady=10)

        self.check_path = tk.IntVar(self, value=1)
        c1 = tk.Checkbutton(self, text="使用原文件路径", variable=self.check_path, onvalue=1, offvalue=0)
        c1.grid(row=4, column=0, pady=10)
        tk.Button(self, text="--> 转义", command=self.trans, width=20, height=2).grid(
            row=4, column=1, columnspan=1, pady=10)

    def delete(self):
        delete_tuple = self.listbox.curselection()
        delete_list = list(delete_tuple)
        delete_list.reverse()
        # print(delete_tuple, len(self.paths))
        for item in delete_list:
            del self.paths[item]
        self.listbox.delete(first=delete_tuple[0], last=delete_tuple[-1])

    def select_file(self):
        self.files = filedialog.askopenfilenames()  # 选择打开什么文件，返回文件名
        self.inter()

    def select_folder(self):
        self.folders = filedialog.askdirectory()  # 选择打开什么文件，返回文件名
        self.inter()

    def inter(self):
        def add_path(path):
            path = os.path.abspath(path)
            if path not in self.paths:
                self.paths.append(path)
            else:
                self.listbox.delete(self.paths.index(path))

        if self.files:
            for path in self.files:
                add_path(path)
        if self.folders:
            for filepath, dirnames, filenames in os.walk(self.folders):
                for filename in filenames:
                    add_path(os.path.join(filepath, filename))
        for i in self.paths:
            self.listbox.insert(tk.END, i)

    def trans(self):
        state = None

        def decompose(content: str):
            """ p_file为加上前一个文件目录的str """
            file, path = "", ""
            content = content.split("\\")
            file = content[-1]
            p_file = content[-2]
            del content[-1]
            content[0] += "\\"
            for i in content:
                path = os.path.join(path, i)
            return file, path, p_file

        if self.check_path.get() == 1:
            for ori in self.paths:
                file_name, origin_path, _ = decompose(ori)
                state = main(origin_path, origin_path, file_name, self.entry_text.get())
        else:
            save_path = filedialog.askdirectory(title="选择保存的文件夹")
            print(save_path)
            for ori in self.paths:
                file_name, origin_path, p_file = decompose(ori)
                to_path = os.path.join(save_path, "/_inter/", p_file)
                state = main(origin_path, to_path, file_name, self.entry_text.get())
        if state:
            tk.Message(self, text="转义成功").grid()


if __name__ == "__main__":
    root = GUI()
    root.mainloop()
