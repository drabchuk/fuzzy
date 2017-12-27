import fuzzy_utils as fu
import numpy as np

t_norm = 'min'
small = fu.GaussianFuzzyNumber(-1.0, 1.0, 1.0, t_norm=t_norm)
medium = fu.GaussianFuzzyNumber(0.0, 1.0, 1.0, t_norm=t_norm)
big = fu.GaussianFuzzyNumber(1.0, 1.0, 1.0, t_norm=t_norm)
x1 = 1.0
x2 = 0.0
x3 = -1.0
x4 = 0.5
print(x1, 'is small', small.mu(x1))
print(x1, 'is medium', medium.mu(x1))
print(x1, 'is big', big.mu(x1))

#has return fuzzy bool
is_small_x3 = small.has(x3)
is_medium_x2 = medium.has(x2)
is_big_x1 = big.has(x1)
print(x3, 'is small', small.has(x3).degree)
print(x2, 'is medium', medium.has(x2).degree)
print(x1, 'is big', big.has(x1).degree)

rule_firing_level_1 = is_big_x1 & is_medium_x2 & is_small_x3
print('rule 1 fl: ', rule_firing_level_1.degree)

is_small_x1 = small.has(x1)
is_medium_x2 = medium.has(x2)
is_big_x3 = big.has(x3)
print(x1, 'is small', small.has(x1).degree)
print(x2, 'is medium', medium.has(x1).degree)
print(x3, 'is big', big.has(x1).degree)

rule_firing_level_2 = is_big_x3 & is_medium_x2 & is_small_x1
print('rule 2 fl: ', rule_firing_level_2.degree)
