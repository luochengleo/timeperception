import matplotlib.pyplot as plt

plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt


# Example data
people = ('Q1: document relevance',
          'Q2: impact of relevance',
          'Q3: impact of time trial',
          'Q5: confidence of estimation',
          'Q7: document difficulty',
          'Q8: difficult of summary',
          'Q9: interest',
          'Q10: tired')
y_pos = np.arange(len(people))
performance = (6.25, 4.833333333, 5.041666667, 2.75, 2.791666667, 3.045454545, 4.958333333, 3.625)
error = (0.896854406, 1.659404468, 1.654484464, 0.846989554, 1.020620726, 0.998917163, 0.954584666, 1.244553351)

plt.barh(y_pos, performance, xerr=error, align='center', alpha=0.4)
plt.yticks(y_pos, people,multialignment='left')
plt.xlabel('Score')

plt.show()
