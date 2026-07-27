# learn-python

A workspace for learning Python and practicing interview-style problems.

## Getting started

```bash
# Activate the virtual environment
source .venv/bin/activate

# Run the hello world script
python hello.py
```

Or click the ▶ Run button in VS Code.

## Folder structure

```
learn-python/
│
├── .venv/            # Python virtual environment
├── arrays/           # Arrays & HashMap
├── sliding_window/   # Sliding window
├── trees/            # Tree & BST problems
├── graphs/           # Graph traversal & algorithms
├── trie/             # Trie / prefix tree
├── concurrency/      # Threading, async, parallelism
├── design/           # OOP / low-level design
├── system_design/    # High-level system design notes
├── tests/            # Unit tests
└── README.md
```

## Problem set

Each file has the problem link in its docstring, a stub function raising
`NotImplementedError`, and a quick `__main__` self-check. Fill in the stub, then
run the file directly (`python arrays/two_sum.py`) — it prints `ok` when correct.

### Arrays & HashMap
- [Two Sum](https://leetcode.com/problems/two-sum/) — `arrays/two_sum.py`
- [Group Anagrams](https://leetcode.com/problems/group-anagrams/) — `arrays/group_anagrams.py`
- [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) — `arrays/product_of_array_except_self.py`
- [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) — `arrays/top_k_frequent_elements.py`

### Sliding Window
- [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) — `sliding_window/longest_substring_without_repeating_characters.py`
- [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) — `sliding_window/minimum_window_substring.py`
- [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) — `sliding_window/sliding_window_maximum.py`

### Trees
- [Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) — `trees/validate_binary_search_tree.py`
- [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) — `trees/binary_tree_level_order_traversal.py`
- [Lowest Common Ancestor of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) — `trees/lowest_common_ancestor_of_a_binary_tree.py`
- [Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) — `trees/serialize_and_deserialize_binary_tree.py`

### Graphs
- [Clone Graph](https://leetcode.com/problems/clone-graph/) — `graphs/clone_graph.py`
- [Course Schedule](https://leetcode.com/problems/course-schedule/) — `graphs/course_schedule.py`
- [Number of Islands](https://leetcode.com/problems/number-of-islands/) — `graphs/number_of_islands.py`
- [Word Ladder](https://leetcode.com/problems/word-ladder/) — `graphs/word_ladder.py`

### Trie
- [Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/) — `trie/implement_trie_prefix_tree.py`
- [Word Search II](https://leetcode.com/problems/word-search-ii/) — `trie/word_search_ii.py`

## Running tests

```bash
python -m pytest tests/
```
