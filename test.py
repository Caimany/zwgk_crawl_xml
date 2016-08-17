from multiprocessing.dummy import Pool as ThreadPool
import time
from functools import partial

def print_pool(name1,name2):
    time.sleep(10)
    print name1,name2

def gen_name():
    for i in range(10):
        yield i

# Make the Pool of workers
pool = ThreadPool(4)
# Open the urls in their own threads
# and return the results

partial_print_pool = partial(print_pool,name2=0)
results = pool.map(partial_print_pool, gen_name())
#close the pool and wait for the work to finish
pool.close()
pool.join()
