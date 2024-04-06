# (c)2024 MoonWolf  
#『MoonWolfと学ぶPythonシリーズ　第２巻 オブジェクト指向プログラミング 超入門編 』

class iPhone:
    __IOS_VERSION = "14"  # Private定数
    _MODEL_NUMBER = "iPhone 12"  # Protected定数
    SCREEN_SIZE = "6.1 inches"  # Public定数
    
    def __init__(self, color, owner):
        self.__imei = "IMEI7732AA5334C5"  # Private変数
        self._color = color  # Protected変数
        self.owner = owner  # Public変数
    
    def __lock_phone(self):  # Privateメソッド
        return "Phone locked."
    
    def _update_ios(self, new_version):  # Protectedメソッド
        iPhone.__IOS_VERSION = new_version
    
    def make_call(self, number):  # Publicメソッド
        print(f"{self.owner}'s {iPhone._MODEL_NUMBER} calling {number}...")

# iPhoneクラスのインスタンス生成と使用
phone = iPhone("Black", "高坂桐乃")
phone.make_call("123-456-7890")
phone._update_ios("15")
phone.make_call("111-111-1111")
