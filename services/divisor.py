class DivisorCounter:
    @staticmethod
    def count_distinct_divisors(num):
        num = abs(int(num))
        if num <= 0:
            return 0
        count = 0
        for i in range(1, int(num**0.5) +1):
            if num % i ==0:
                if i == num//i:
                    count += 1
                else:
                    count += 2
        return count