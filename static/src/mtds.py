

class A:
    """__doc__ of class A"""
    def __init__(self):
        self.value = "obj->A"

    def _print(self):
        print(f"{self.value} from {A._print.__name__} | class {A.__name__}")

    def _msg(self):
        print(f"{self.value} from {A._msg.__name__} | class {A.__name__}")


class B(A):
    """__doc__ of class B"""
    def __init__(self):
        self.value = "A->B"

    def _msg(self):
        print(f"{self.value} from {B._msg.__name__} | class {B.__name__}")
        return 2


class C(B):
    """__doc__ of class C"""
    def __init__(self):
        self.value = "B->C"

    def _msg(self):
        #if super()._msg() == 1:
        #    print("<override> _msg\treturn 2")
        #    return 2
        #else:
        print(f"""Message from {self.value} | class {C.__name__} | func {C._msg.__name__}""")

    def _print(self):
        super()._print()
        print(f"""Message from {self.value} | class {C.__name__} | func {C._print.__name__}""")


c = C()
c._msg()
c._print()

