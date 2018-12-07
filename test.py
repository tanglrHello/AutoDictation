def foo():
    sum = 0
    for i in range(10000000):
        sum += i
        return sum
import cProfile
if __name__ == "__main__":
    cProfile.run("foo()")
