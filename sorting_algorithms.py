"""
排序算法模块

实现了五种经典排序算法：
- 冒泡排序 (Bubble Sort)
- 快速排序 (Quick Sort)
- 希尔排序 (Shell Sort)
- 堆排序   (Heap Sort)
- 基数排序 (Radix Sort)

所有算法都支持可视化回调函数，用于实时展示排序过程。
可视化回调会在适当的时机被调用，并传入当前的数组状态。
为了优化性能，可视化更新频率可通过 refresh_rate 参数控制。
"""

def bubble_sort(arr, draw_callback=None, refresh_rate=10):
    """
    冒泡排序算法实现
    
    :param arr: 待排序的数组
    :param draw_callback: 可视化回调函数，用于更新排序过程的展示
    :param refresh_rate: 可视化刷新频率，每处理多少轮刷新一次
    """
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        # 如果本轮没有发生交换，说明已排序完成
        if not swapped:
            if draw_callback:
                draw_callback(arr, None)
            break

        # 每隔若干轮才进行可视化刷新
        if draw_callback and i % refresh_rate == 0:
            draw_callback(arr, n-1-i)


def quick_sort(arr, draw_callback=None, low=0, high=None, refresh_rate=200, depth=0, stats=None):
    """
    快速排序算法实现（递归版本）
    
    :param arr: 待排序的数组
    :param draw_callback: 可视化回调函数
    :param low: 当前处理的左边界
    :param high: 当前处理的右边界
    :param refresh_rate: 可视化刷新频率
    :param depth: 递归深度（已废弃，保留参数是为了兼容性）
    :param stats: 用于跨递归层级统计操作次数的字典
    """
    if stats is None:
        stats = {"op_count": 0}
    
    if high is None:
        high = len(arr) - 1

    if low < high:
        pivot_index = partition(arr, low, high, draw_callback, refresh_rate, stats)
        quick_sort(arr, draw_callback, low, pivot_index - 1, refresh_rate, depth+1, stats)
        quick_sort(arr, draw_callback, pivot_index + 1, high, refresh_rate, depth+1, stats)


def partition(a, low, high, draw_callback=None, refresh_rate=200, stats=None):
    """
    快速排序的分区函数
    
    :param a: 待分区的数组
    :param low: 左边界
    :param high: 右边界
    :param draw_callback: 可视化回调函数
    :param refresh_rate: 可视化刷新频率
    :param stats: 操作统计字典
    :return: 分区点的索引
    """
    pivot = a[high]
    i = low - 1
    for j in range(low, high):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
            stats["op_count"] += 1
            if draw_callback and stats["op_count"] % refresh_rate == 0:
                draw_callback(a, j)
    
    a[i+1], a[high] = a[high], a[i+1]
    stats["op_count"] += 1
    if draw_callback and stats["op_count"] % refresh_rate == 0:
        draw_callback(a, i+1)
    
    return i + 1


def shell_sort(arr, draw_callback=None, refresh_rate=10):
    """
    希尔排序算法实现
    
    :param arr: 待排序的数组
    :param draw_callback: 可视化回调函数
    :param refresh_rate: 可视化刷新频率，每处理多少轮刷新一次
    """
    n = len(arr)
    gap = n // 2
    iteration = 0
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp

            # 仅在此处计数
            iteration += 1
            if draw_callback and iteration % refresh_rate == 0:
                draw_callback(arr, j)

        gap //= 2


def heap_sort(arr, draw_callback=None, refresh_rate=10):
    """
    堆排序算法实现
    
    :param arr: 待排序的数组
    :param draw_callback: 可视化回调函数
    :param refresh_rate: 可视化刷新频率，每多少次交换操作刷新一次
    """
    n = len(arr)

    def heapify(a, n, i, stats):
        """
        维护最大堆的辅助函数
        
        :param a: 待调整的数组
        :param n: 堆的大小
        :param i: 当前需要维护的节点索引
        :param stats: 操作统计字典
        """
        largest = i
        left = 2*i + 1
        right = 2*i + 2

        if left < n and a[left] > a[largest]:
            largest = left
        if right < n and a[right] > a[largest]:
            largest = right
        if largest != i:
            a[i], a[largest] = a[largest], a[i]
            stats["swap_count"] += 1
            if draw_callback and stats["swap_count"] % refresh_rate == 0:
                draw_callback(a, largest)
            heapify(a, n, largest, stats)

    # 构建大顶堆
    stats = {"swap_count": 0}
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, stats)

    # 依次取出堆顶元素并重建堆
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        stats["swap_count"] += 1
        if draw_callback and stats["swap_count"] % refresh_rate == 0:
            draw_callback(arr, i)
        heapify(arr, i, 0, stats)


def radix_sort(arr, draw_callback=None, refresh_rate=1000):
    """
    基数排序算法实现（LSD - 最低位优先）
    
    :param arr: 待排序的非负整数数组
    :param draw_callback: 可视化回调函数
    :param refresh_rate: 可视化刷新频率，每多少次元素移动操作刷新一次
    """
    if len(arr) == 0:
        return

    max_val = max(arr)
    exp = 1
    move_count = 0
    while max_val // exp > 0:
        buckets = [[] for _ in range(10)]
        for num in arr:
            digit = (num // exp) % 10
            buckets[digit].append(num)

        index = 0
        for bucket in buckets:
            for num in bucket:
                arr[index] = num
                index += 1
                move_count += 1
                if draw_callback and move_count % refresh_rate == 0:
                    draw_callback(arr, index-1)

        exp *= 10
