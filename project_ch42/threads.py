import threading


def sum_range(thread_id, start, end, result):
    result[thread_id] = sum(range(start, end + 1))

def main(ranges):
    thread_count = len(ranges)

    threads = []

    result = [0] * thread_count

    for i in range(thread_count):
        t = threading.Thread(target=sum_range, args=(i, ranges[i][0], ranges[i][1], result))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print(result)
    print(sum(result)) 


if __name__ == "__main__":
    ranges = [
        [10, 20],
        [1, 5],
        [70, 80],
        [27, 92],
        [0, 16]
    ]

    main(ranges)