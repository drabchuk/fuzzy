import numpy as np


#Supposed that universum is R
#is fuzzy singleton by default

class FuzzyBool(object):

    def __init__(self, degree, t_norm):
        self.degree = degree
        self.t_norm = t_norm

    def __and__(self, other):
        if self.t_norm == 'min':
            return FuzzyBool(
                degree=np.min((self.degree, other.degree)),
                t_norm=self.t_norm
            )
        elif self.t_norm == 'mult':
            return FuzzyBool(
                degree=self.degree * other.degree,
                t_norm=self.t_norm
            )
        else:
            raise Exception('t_norm is not specified or unknown try min or mult')

    def __or__(self, other):
        if self.t_norm == 'min':
            return FuzzyBool(
                degree=np.max((self.degree, other.degree)),
                t_norm=self.t_norm
            )
        elif self.t_norm == 'mult':
            other_mu = other.degree
            return FuzzySingleton(
                degree=1.0 - self.degree - other_mu + self.degree * other_mu,
                t_norm=self.t_norm
            )
        else:
            raise Exception('t_norm is not specified or unknown try min or mult')

    def __invert__(self):
        return FuzzyBool(degree=1.0 - self.degree, t_norm=self.t_norm)

class FuzzyNumber(object):

    def __init__(self, number, t_norm='min'):
        self.number = number
        self.t_norm = t_norm

    def mu(self, x):
        return 1.0 if x == self.number else 0.0

    def has(self, x):
        return FuzzyBool(degree=self.mu(x), t_norm=self.t_norm)

    def __and__(self, other):
        raise NotImplementedError()

    def __or__(self, other):
        raise NotImplementedError

    def __invert__(self):
        raise NotImplementedError


class FuzzySingleton(FuzzyNumber):

    def __init__(self, number, degree=1.0, t_norm='min'):
        super().__init__(number, t_norm)
        self.degree = degree

    def mu(self, x):
        return self.degree if x == self.number else 0.0

    def __and__(self, other):
        if self.t_norm == 'min':
            return FuzzySingleton(
                self.number,
                degree=np.min((self.degree, other.mu(self.number))),
                t_norm=self.t_norm
            )
        elif self.t_norm == 'mult':
            return FuzzySingleton(
                self.number,
                degree=self.degree * other.mu(self.number),
                t_norm=self.t_norm
            )
        else:
            raise Exception('t_norm is not specified or unknown try min or mult')

    def __or__(self, other):
        if self.t_norm == 'min':
            return FuzzySingleton(
                self.number,
                degree=np.max((self.degree, other.mu(self.number))),
                t_norm=self.t_norm
            )
        elif self.t_norm == 'mult':
            other_mu = other.mu(self.number)
            return FuzzySingleton(
                self.number,
                degree=1.0 - self.degree - other_mu + self.degree * other_mu,
                t_norm=self.t_norm
            )
        else:
            raise Exception('t_norm is not specified or unknown try min or mult')

    def __invert__(self):
        raise NotImplementedError('Wow, are you sure inverting singleton? Not implemented yet.')


class GaussianFuzzyNumber(FuzzyNumber):

    def __init__(self, number, std, degree, t_norm):
        super().__init__(number, t_norm)
        self.std = std

    def mu(self, x):
        return np.exp(-((self.number - x) / self.std) ** 2 / 2.0)

    def __and__(self, other):
        raise NotImplementedError()

    def __or__(self, other):
        raise NotImplementedError()

    def __invert__(self):
        raise NotImplementedError()


class TriangularFuzzyNumber(FuzzyNumber):

    def __init__(self, number, left, right):
        super().__init__(number)
        self.left = left
        self.right = right

    def mu(self, x):
        return np.max((0.0,
                      (x - self.left) / (self.number - self.left)
                      if x < self.number else
                      (self.right - x) / (self.right - self.number)))

    def __and__(self, other):
        raise NotImplementedError()

    def __or__(self, other):
        raise NotImplementedError()

    def __invert__(self):
        raise NotImplementedError()
