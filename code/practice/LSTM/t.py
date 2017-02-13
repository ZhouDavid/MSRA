import numpy as np
import cntk as C
from cntk import ops

x = C.input_variable(shape=	(1,3))
x0 = np.reshape(np.arange(48.0,dtype = np.float32),(4,4,1,3))
print x0
first_seq = C.sequence.first(x)
print first_seq.eval({x:x0})