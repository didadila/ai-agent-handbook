"""Deterministic boundary tests and small exhaustive/random oracle comparisons."""
import ast
import itertools
import random
import re
import unittest
from pathlib import Path

from algorithms import *
from acm_pairs import solve


class AlgorithmsTest(unittest.TestCase):
    def test_python_and_sort(self):
        self.assertEqual(read_pairs(' 1 2\n\n-3 4\n'), [(1, 2), (-3, 4)])
        self.assertEqual(solve('1 2\n-3 4'), '3\n1')
        self.assertEqual(solve(''), '')
        with self.assertRaises(ValueError):
            read_pairs('1 2 3')
        records = [('b', 1), ('a', 1), ('z', 0)]
        self.assertEqual(stable_rank(records), [('z', 0), ('b', 1), ('a', 1)])
        self.assertEqual(records[0], ('b', 1))

    def test_arrays_against_enumeration(self):
        for n in range(6):
            for values in itertools.product((-1, 0, 1), repeat=n):
                nums = list(values)
                self.assertEqual(prefix_sums(nums), [sum(nums[:i]) for i in range(n + 1)])
                for target in (-2, 0, 2):
                    expected = sum(sum(nums[i:j]) == target for i in range(n) for j in range(i + 1, n + 1))
                    self.assertEqual(subarray_count(nums, target), expected)
                    pair = two_sum(nums, target)
                    possible = any(nums[i] + nums[j] == target for i in range(n) for j in range(i + 1, n))
                    self.assertEqual(pair is not None, possible)
                    if pair:
                        self.assertNotEqual(*pair)
                        self.assertEqual(sum(nums[i] for i in pair), target)
                    sorted_nums = sorted(nums)
                    pair = sorted_pair(sorted_nums, target)
                    self.assertEqual(pair is not None, possible)
                    if pair:
                        self.assertLess(*pair)
                        self.assertEqual(sum(sorted_nums[i] for i in pair), target)
                    self.assertEqual(lower_bound(sorted_nums, target), sum(x < target for x in sorted_nums))

    def test_window_against_bruteforce(self):
        for n in range(7):
            for chars in itertools.product('ab', repeat=n):
                text = ''.join(chars)
                expected = max((j-i for i in range(n+1) for j in range(i, n+1) if len(set(text[i:j])) == j-i), default=0)
                self.assertEqual(longest_unique(text), expected)
        self.assertEqual(longest_unique('abba'), 2)
        self.assertEqual(longest_unique('你我你'), 2)

    def test_grid_preserves_input(self):
        grid = [[1, 0], [0, 1]]
        self.assertEqual(islands(grid), 2)
        self.assertEqual(grid, [[1, 0], [0, 1]])
        for data in ([], [[]], [[0, 0]]):
            self.assertEqual(islands(data), 0)
        self.assertEqual(islands([[1, 1], [1, 1]]), 1)
        with self.assertRaises(ValueError):
            islands([[1], []])

    def test_linked_identity_and_cycle(self):
        a, b, c = ListNode(1), ListNode(1), ListNode(3)
        a.next, b.next = b, c
        self.assertFalse(has_cycle(a))
        head = reverse_list(a)
        self.assertIs(head, c)
        self.assertIs(c.next, b)
        self.assertIs(b.next, a)
        self.assertIsNone(a.next)
        a.next = b
        self.assertTrue(has_cycle(c))
        self.assertIsNone(reverse_list(None))

    def test_stack_oracle(self):
        rng = random.Random(13)
        for n in range(30):
            values = [rng.randrange(5) for _ in range(n)]
            expected = [next((j-i for j in range(i+1,n) if values[j]>values[i]), 0) for i in range(n)]
            self.assertEqual(daily_temperatures(values), expected)
        for text in ('', '([])', '{}[]'):
            self.assertTrue(valid_brackets(text))
        for text in ('([)]', '(', ')', 'a'):
            self.assertFalse(valid_brackets(text))

    def test_heap_repeats_and_invalid_k(self):
        rng = random.Random(7)
        for n in range(1, 30):
            values = [rng.randrange(-5, 6) for _ in range(n)]
            original = values.copy()
            for k in range(1, n + 1):
                self.assertEqual(kth_largest(values, k), sorted(values, reverse=True)[k-1])
            self.assertEqual(values, original)
        for k in (0, 4):
            with self.assertRaises(ValueError):
                kth_largest([1, 2, 3], k)

    def test_trie_word_end_not_prefix(self):
        trie = Trie()
        self.assertTrue(trie.starts_with(''))
        self.assertFalse(trie.contains(''))
        for word in ('apple', 'app', '#', '', 'apple'):
            trie.insert(word)
        for word in ('apple', 'app', '#', ''):
            self.assertTrue(trie.contains(word))
        self.assertFalse(trie.contains('ap'))
        self.assertTrue(trie.starts_with('ap'))

    def test_trees_global_bounds_and_depth(self):
        tree = TreeNode(10, TreeNode(5, None, TreeNode(12)))
        self.assertFalse(valid_bst(tree))
        self.assertEqual(level_order(tree), [[10], [5], [12]])
        self.assertFalse(valid_bst(TreeNode(1, TreeNode(1))))
        self.assertTrue(valid_bst(None))
        self.assertEqual(level_order(None), [])
        root = None
        for value in range(2000):
            root = TreeNode(value, root)
        self.assertTrue(valid_bst(root))
        self.assertEqual(len(level_order(root)), 2000)

    def test_graph_and_topology(self):
        self.assertEqual(bfs_distances([[1, 2], [3], [3], [], []], 0), [0, 1, 1, 2, -1])
        self.assertEqual(topological_order(0, []), [])
        self.assertIsNone(topological_order(2, [(0, 1), (1, 0)]))
        edges = [(0, 1), (0, 1), (1, 3), (2, 3)]
        order = topological_order(4, edges)
        pos = {v:i for i,v in enumerate(order)}
        self.assertEqual(set(order), set(range(4)))
        self.assertTrue(all(pos[u] < pos[v] for u,v in edges))
        with self.assertRaises(ValueError):
            topological_order(2, [(0, 2)])

    def test_dsu(self):
        dsu = DSU(4)
        self.assertTrue(dsu.union(0, 1))
        self.assertTrue(dsu.union(2, 3))
        self.assertFalse(dsu.union(1, 0))
        self.assertEqual(dsu.components, 2)
        self.assertNotEqual(dsu.find(0), dsu.find(2))
        self.assertTrue(dsu.union(1, 3))
        self.assertEqual(dsu.components, 1)
        with self.assertRaises(IndexError):
            dsu.find(-1)

    def test_dijkstra_against_bellman_ford(self):
        rng = random.Random(17)
        for n in range(1, 9):
            for _ in range(10):
                adj = [[(v, rng.randrange(5)) for v in range(n) if rng.random() < .3] for _ in range(n)]
                expected = [float('inf')] * n
                expected[0] = 0
                for _ in range(n-1):
                    for u, row in enumerate(adj):
                        for v, w in row:
                            expected[v] = min(expected[v], expected[u] + w)
                self.assertEqual(dijkstra(adj, 0), expected)
        with self.assertRaises(ValueError):
            dijkstra([[(1, -1)], []], 0)
        self.assertEqual(dijkstra([[(1,10),(2,1)],[],[(1,1)]],0), [0,2,1])

    def test_subsets_unique_and_unshared(self):
        values = [1, 2, 2]
        result = unique_subsets(values)
        expected = {tuple(sorted(values[i] for i in range(len(values)) if mask>>i&1)) for mask in range(1<<len(values))}
        self.assertEqual({tuple(s) for s in result}, expected)
        self.assertEqual(len(result), len(expected))
        result[0].append(99)
        self.assertTrue(all(99 not in s for s in result[1:]))
        self.assertEqual(values, [1,2,2])

    def test_dp_against_enumeration(self):
        self.assertEqual(min_coins([1,3,4], 6), 2)
        self.assertEqual(min_coins([2],3), -1)
        self.assertEqual(min_coins([],0), 0)
        with self.assertRaises(ValueError):
            min_coins([0], 3)
        rng = random.Random(19)
        for n in range(7):
            weights = [rng.randrange(1,5) for _ in range(n)]
            values = [rng.randrange(-2,8) for _ in range(n)]
            for cap in range(9):
                expected = max(sum(values[i] for i in range(n) if mask>>i&1) for mask in range(1<<n) if sum(weights[i] for i in range(n) if mask>>i&1)<=cap)
                self.assertEqual(knapsack01(weights, values, cap), expected)
        self.assertEqual(knapsack01([1],[3],2), 3)

    def test_coin_change_against_shortest_path_search(self):
        # Independent oracle: each additional coin traverses one unweighted edge.
        for mask in range(1 << 4):
            coins = [i + 1 for i in range(4) if mask >> i & 1]
            for amount in range(13):
                queue, visited, expected = deque([(0, 0)]), {0}, -1
                while queue:
                    total, count = queue.popleft()
                    if total == amount:
                        expected = count
                        break
                    for coin in coins:
                        next_total = total + coin
                        if next_total <= amount and next_total not in visited:
                            visited.add(next_total)
                            queue.append((next_total, count + 1))
                self.assertEqual(min_coins(coins, amount), expected)

    def test_lcs_against_independent_subsequence_sets(self):
        words = [''.join(chars) for n in range(5) for chars in itertools.product('ab', repeat=n)]
        def subsequences(word):
            return {''.join(word[i] for i in range(len(word)) if mask >> i & 1)
                    for mask in range(1 << len(word))}
        sets = {word: subsequences(word) for word in words}
        for a in words:
            for b in words:
                expected = max(map(len, sets[a] & sets[b]))
                self.assertEqual(lcs_length(a, b), expected)

    def test_explained_boundary_counterexamples(self):
        self.assertEqual(sorted_pair([1, 4, 2], 5), None)
        self.assertIsNotNone(two_sum([1, 4, 2], 5))
        self.assertEqual(topological_order(2, [(1, 0)]), [1, 0])
        self.assertEqual(knapsack01([2], [3], 4), 3)
        self.assertEqual(lis_length([2, 3, 1]), 2)
        self.assertEqual((-1).bit_count(), 1)
        self.assertEqual((-1 & 255).bit_count(), 8)
        # Positive-only shrink-until-below-threshold loses the optimum here.
        values, target = [1, -1, 3], 3
        left, total, best = 0, 0, len(values) + 1
        for right, value in enumerate(values):
            total += value
            while total >= target:
                best = min(best, right - left + 1)
                total -= values[left]
                left += 1
        oracle = min(j - i for i in range(len(values)) for j in range(i + 1, len(values) + 1)
                     if sum(values[i:j]) >= target)
        self.assertEqual((best, oracle), (3, 1))

    def test_sequence_against_subsequence_enumeration(self):
        for n in range(6):
            for nums in itertools.product((0,1,2), repeat=n):
                sequences = [tuple(nums[i] for i in range(n) if mask>>i&1) for mask in range(1<<n)]
                expected = max(len(s) for s in sequences if all(a<b for a,b in zip(s,s[1:])))
                self.assertEqual(lis_length(nums), expected)
        for a,b,expected in [('abcde','ace',3),('aaa','aa',2),('','abc',0)]:
            self.assertEqual(lcs_length(a,b),expected)

    def test_greedy_against_reachability(self):
        self.assertFalse(can_jump([]))
        for n in range(1,7):
            for nums in itertools.product((0,1,2), repeat=n):
                reachable = {0}
                for i in range(n):
                    if i in reachable:
                        reachable.update(range(i+1, min(n,i+nums[i]+1)))
                self.assertEqual(can_jump(nums), n-1 in reachable)

    def test_intervals_and_bits(self):
        data = [(5,7),(1,2),(2,3),(6,6)]
        self.assertEqual(merge_intervals(data), [(1,3),(5,7)])
        self.assertEqual(data[0], (5,7))
        self.assertEqual(merge_intervals([]), [])
        with self.assertRaises(ValueError):
            merge_intervals([(3,1)])
        self.assertEqual(single_number([-7,2,2,3,3]), -7)
        self.assertEqual(single_number([0]), 0)

    def test_textbook_code_matches_tested_implementations(self):
        root = Path(__file__).resolve().parents[1]
        implementations = {node.name: ast.dump(node, include_attributes=False) for node in ast.parse((root/'examples/algorithms.py').read_text()).body if isinstance(node,(ast.FunctionDef,ast.ClassDef))}
        for path in root.glob('[0-9][0-9]-*.md'):
            for code in re.findall(r'```python\n(.*?)```',path.read_text(),re.S):
                for node in ast.parse(code).body:
                    self.assertEqual(ast.dump(node,include_attributes=False),implementations[node.name],path.name)


if __name__ == '__main__':
    unittest.main()
