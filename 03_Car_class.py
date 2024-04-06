# (c)2024 MoonWolf  
#『MoonWolfと学ぶPythonシリーズ　第２巻 オブジェクト指向プログラミング 超入門編 』

class Car:
    __MAX_SPEED = 200  # Private定数
    _FUEL_TYPE = "ガソリン"  # Protected定数
    BRAND = "Toyota"  # Public定数
    
    def __init__(self, model, color):
        self.__engine_number = "EN123456"  # Private変数
        self._color = color  # Protected変数
        self.model = model  # Public変数
    
    def __start_engine(self):  # Privateメソッド
        return "Engine started."
    
    def _change_fuel(self, new_fuel_type):  # Protectedメソッド
        Car._FUEL_TYPE = new_fuel_type
    
    def drive(self):  # Publicメソッド
        print(f"Driving {self.model} - {self._color}, {Car.BRAND}")

# Carクラスのインスタンス生成と使用
car = Car("スープラZZZ", "白")
car.drive()
car._change_fuel("電気")
car.drive()
