import pandas as pd
import numpy as np


def data_from(t, f):
	fun = "from_"+ t
	if hasattr(pd.DataFrame, fun):
		func = getattr(pd.DataFrame, fun)
		return func(f)

