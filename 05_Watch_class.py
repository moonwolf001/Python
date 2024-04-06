# (c)2024 MoonWolf  
#『MoonWolfと学ぶPythonシリーズ　第２巻 オブジェクト指向プログラミング 超入門編 』

class Watch:
    __MANUFACTURE_YEAR = "2020"  # Private定数
    _BRAND_NAME = "Seiko"  # Protected定数
    WATER_RESISTANT = True  # Public定数
    
    def __init__(self, model, owner):
        self.__serial_number = "SN123456"  # Private変数
        self._model = model  # Protected変数
        self.owner = owner  # Public変数
    
    def __display_manufacture_date(self):  # Privateメソッド
        return f"Manufactured in {Watch.__MANUFACTURE_YEAR}"
    
    def _change_battery(self):  # Protectedメソッド
        print("Battery changed.")
    
    def show_time(self):  # Publicメソッド
        print(f"{self.owner}'s {Watch._BRAND_NAME} {self._model} shows the time.")

# Watchクラスのインスタンス生成と使用
watch = Watch("Model S", "初音ミク")
watch.show_time()
watch._change_battery()
watch.show_time()
