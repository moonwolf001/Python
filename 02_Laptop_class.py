# (c)2024 MoonWolf  
#『MoonWolfと学ぶPythonシリーズ　第２巻 オブジェクト指向プログラミング 超入門編 』

class LaptopPC:
    __MANUFACTURER = "Sony"  # Private定数
    _HARD_DRIVE_TYPE = "SSD"  # Protected定数
    OS_VERSION = "Windows 10"  # Public定数
    
    def __init__(self, model, owner):
        self.__serial_number = "S11BE443793"  # Private変数
        self._model = model  # Protected変数
        self.owner = owner  # Public変数
    
    def __display_serial_number(self):  # Privateメソッド
        return f"Serial Number: {self.__serial_number}"
    
    def _update_os_version(self, new_version):  # Protectedメソッド
        LaptopPC.OS_VERSION = new_version
    
    def display_specs(self):  # Publicメソッド
        print(f"Owner: {self.owner}, Model: {self._model}, OS Version: {LaptopPC.OS_VERSION}")

# LaptopPCクラスのインスタンス生成と使用
laptop = LaptopPC("Sony Model X", "MoonWolf")
laptop.display_specs()
laptop._update_os_version("Windows 11")
laptop.display_specs()
