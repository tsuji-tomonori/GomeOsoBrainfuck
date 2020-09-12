import sys

class Machine:

    def __init__(self, N, cmd_lst):
        self.tape = [0 for n in range(N)]
        self.ptr = 0
        self.cmd_lst = cmd_lst
        self.head = 0
        self._cmd2lambda = {
            ">": self._inc_ptr,
            "<": self._dec_ptr,
            "+": self._inc_ptr_value,
            "-": self._dec_ptr_value,
            ".": self._print_ptr,
            ",": self._input_ptr,
            "[": self._while_start,
            "]": self._while_end
        }

    def __call__(self):
        self._cmd2lambda[self.cmd_lst[self.head]]()
        self.head += 1

    def is_accept(self):
        return len(self.cmd_lst) == self.head

    def __bool__(self):
        return self.is_accept()

    def _inc_ptr(self):
        self.ptr += 1

    def _dec_ptr(self):
        self.ptr -= 1

    def _inc_ptr_value(self):
        self.tape[self.ptr] += 1

    def _dec_ptr_value(self):
        self.tape[self.ptr] -= 1

    def _print_ptr(self):
        print(chr(self.tape[self.ptr]), end="", flush=True)

    def _input_ptr(self):
        c = sys.stdin.buffer.read(1)
        self.tape[self.ptr] = ord(c)

    def _while_start(self):
        if self.tape[self.ptr] != 0:
            return
        count = 1
        while count != 0:
            self.head += 1
            if self.head == len(self.cmd_lst):
                raise KeyError("']' is missing")
            if self.cmd_lst[self.head] == "[":
                count += 1
            elif self.cmd_lst[self.head] == "]":
                count -= 1

    def _while_end(self):
        if self.tape[self.ptr] == 0:
            return
        count = 1
        while count != 0:
            self.head -= 1
            if self.head < 0:
                raise KeyError("'[' is missing")
            if self.cmd_lst[self.head] == "]":
                count += 1
            elif self.cmd_lst[self.head] == "[":
                count -= 1