# (c)2024 MoonWolf  
#『MoonWolfと学ぶPythonシリーズ　第２巻 オブジェクト指向プログラミング 超入門編 』

class Student:
    __SCHOOL_NAME = "地球防衛大学"  # Private定数
    _UNIVERSITY_YEAR = 4  # Protected定数
    DEGREE = "学士"  # Public定数
    
    def __init__(self, name, age):
        self.__id = "500287735"  # Private変数
        self._name = name  # Protected変数
        self.age = age  # Public変数
    
    def __display_id(self):  # Privateメソッド
        return f"Student ID: {self.__id}"
    
    def _increase_year(self):  # Protectedメソッド
        self.age += 1
    
    def display_info(self):  # Publicメソッド
        print(f"Name: {self._name}, Age: {self.age}, Degree: {Student.DEGREE}")

# Studentクラスのインスタンス生成と使用
student = Student("C215 メアリー", 20)
student.display_info()
student._increase_year() #管理者だけが操作できるもの
student.display_info()
