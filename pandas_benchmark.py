import pandas as pd                                                             
import numpy as np                                                              
import random                                                                   
from timeit import timeit                                                       

print('<table>')
print('<tr><th>Size</th><th>Python</th><th>Pandas</th><th>Numpy</th></tr>')
for size in [10, 100, 1000, 2500, 5000, 10000]:
    a = [random.randint(0, 100) for x in range(0, size)]                        
    b = [random.randint(0, 100) for x in range(0, size)]                        
                                                                                
    py_time = timeit(lambda: [x + y for x, y in zip(a, b)], number=1000)

    series_a, series_b = pd.Series(a), pd.Series(b)
    pd_time = timeit(lambda: series_a + series_b, number=1000)

    array_a, array_b = np.array(a), np.array(b)
    np_time = timeit(lambda: array_a + array_b, number=1000)
                                     
    print(f'<tr><td>{size}</td><td>{py_time:.2}s</td><td>{pd_time:.2}s</td><td>{np_time:.2}s</td></tr>')
print('</table>')
