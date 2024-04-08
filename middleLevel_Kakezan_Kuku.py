for i in range(2, 10):
    for j in range(1, 10):
        print(f"{i}x{j}={i*j}", end=" ")
        if j == 9:
            print()  # 改行を出力
        else:
            result_length = len(str(i*j))
            if result_length == 1:
                print(" ", end="") 
            print(" ", end="")  
