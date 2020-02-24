import pandas as pd

import numpy as np
s= pd.Series([3, -5, 7, 4])
print(s,type(s),s.shape,s.name)
dates = pd.date_range('20130101', periods=6)
print(dates)
df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
print(df)
print(df.mean())