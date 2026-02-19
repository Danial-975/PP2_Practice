class A:
    def __init__(self, **kwargs):
        print("A.__init__")
        super().__init__(**kwargs)

class B(A):
    def __init__(self, **kwargs):
        print("B.__init__")
        super().__init__(**kwargs)

class C(A):
    def __init__(self, **kwargs):
        print("C.__init__")
        super().__init__(**kwargs)

class D(B, C):
    def __init__(self, **kwargs):
        print("D.__init__")
        super().__init__(**kwargs)

d = D()