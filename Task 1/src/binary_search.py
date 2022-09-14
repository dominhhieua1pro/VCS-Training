
def binary_search(arr, low, high, x):
    if high >= low:
        mid = (low + high) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] < x:
            return binary_search(arr, mid+1, high, x)
        else:
            return binary_search(arr, low, mid-1, x)
    else:
        return -1

if __name__ == "__main__":
    arr = [1,2,3,4,5,6,7,8,9,10]
    x = int(input("Nhap gia tri tim kiem: "))
    result = binary_search(arr, 0, len(arr)-1, x)
    if result != -1:
        print("Phan tu can tim co chi so la: ", result)
    else:
        print("Phan tu can tim khong ton tai trong mang")
