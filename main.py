import random
import math

# генерация случайных вероятностей появления символов
m = 10  # количество символов в источнике
p = [random.uniform(0.01, 1) for i in range(m)]
p_sum = sum(p)
p = [p[i] / p_sum for i in range(m)]  # нормировка вероятностей

# равномерное кодирование
uniform_code = ['{:b}'.format(i).zfill(math.ceil(math.log2(m))) for i in range(m)]
uniform_code_dict = {i: uniform_code[i] for i in range(m)}


# алгоритм Шеннона-Фано
def shannon_fano(p, code_dict, start, end):
    if start == end:
        return
    if start + 1 == end:
        code_dict[start] += '0'
        code_dict[end] += '1'
        return
    mid = start
    w1 = p[start]
    w2 = p[end]
    while mid < end - 1 and w1 < w2:
        mid += 1
        w1 += p[mid]
        w2 -= p[mid]
    if mid == start:
        for i in range(start, mid + 1):
            code_dict[i] += '0'
    else:
        for i in range(start, mid + 1):
            code_dict[i] += '1'
        for i in range(mid + 1, end + 1):
            code_dict[i] += '0'
    shannon_fano(p, code_dict, start, mid)
    shannon_fano(p, code_dict, mid + 1, end)


shannon_fano_code_dict = {i: '' for i in range(m)}
shannon_fano(p, shannon_fano_code_dict, 0, m - 1)


# алгоритм Хаффмана
class Node:
    def __init__(self, symbol=None, prob=None):
        self.symbol = symbol
        self.prob = prob
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.prob < other.prob

    def __eq__(self, other):
        return self.prob == other.prob


def huffman(p):
    queue = [Node(i, p[i]) for i in range(m)]
    while len(queue) > 1:
        queue.sort()
        node1 = queue.pop(0)
        node2 = queue.pop(0)
        new_node = Node(prob=node1.prob + node2.prob)
        new_node.left = node1
        new_node.right = node2
        queue.append(new_node)
    code_dict = {i: '' for i in range(m)}
    root = queue[0]

    def traverse(node, code):
        if node.symbol is not None:
            code_dict[node.symbol] = code
            return
        code += uniform_code_dict[node.symbol]

        if node.left is not None:
            traverse(node.left, code)


entropy = -sum([p[i] * math.log2(p[i]) for i in range(m)])
avg_code_len_uniform = sum([len(uniform_code_dict[i]) * p[i] for i in range(m)])
avg_code_len_shannon_fano = sum([len(shannon_fano_code_dict[i]) * p[i] for i in range(m)])
print("энтропия: ", entropy, '\n', "средняя длина кода равномерная: ", avg_code_len_uniform, '\n',"средняя длина Шаннон Фано: ", avg_code_len_shannon_fano)

