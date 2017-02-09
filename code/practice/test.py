import numpy as np
import sys
import os
from cntk.device import cpu, set_default_device
from cntk import Trainer
from cntk.learner import sgd, learning_rate_schedule, UnitType
from cntk.ops import input_variable, cross_entropy_with_softmax, classification_error, sigmoid
from cntk.utils import ProgressPrinter

abs_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(abs_path, "..", "..", "Examples", "common"))
from nn import fully_connected_classifier_net