# Study Plan — by topic

A checklist of the problems and design questions in this repo, grouped by topic,
with the core pattern for each. Check items off as you solve them.

**Status legend:** `[ ]` todo · `[x]` done · 🎬 has a visual aid in `experiments/`

Solve a stub, then run the file directly (e.g. `python arrays/two_sum.py`) — it
prints `ok` when your solution passes the built-in self-checks.

---

## 1. Arrays & HashMap  (`arrays/`)
Core idea: trade space for time — a dict/set turns an O(n²) scan into O(n).

- [x] [Two Sum](https://leetcode.com/problems/two-sum/) — `arrays/two_sum.py`  *(solved — remove the leftover `raise NotImplementedError`)*
- [ ] [Group Anagrams](https://leetcode.com/problems/group-anagrams/) — `arrays/group_anagrams.py` · key = sorted string or char-count tuple
- [ ] [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) — `arrays/product_of_array_except_self.py` · prefix × suffix products, no division
- [ ] [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) — `arrays/top_k_frequent_elements.py` · `Counter` + heap or bucket sort

## 2. Sliding Window  (`sliding_window/`)
Core idea: a moving `[left, right]` window; expand right, shrink left on a
violation. Turns many substring/subarray problems into O(n).

- [ ] [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) — `sliding_window/longest_substring_without_repeating_characters.py` · set/dict of last-seen index
- [ ] [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) — `sliding_window/minimum_window_substring.py` · need/have counts, shrink when valid *(hard)*
- [ ] [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) — `sliding_window/sliding_window_maximum.py` · monotonic decreasing `deque` *(hard)*

## 3. Trees  (`trees/`)
Core idea: recursion (DFS) or a queue (BFS). Know pre/in/post-order and level-order cold.

- [ ] [Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) — `trees/validate_binary_search_tree.py` · pass down (min, max) bounds
- [ ] [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) — `trees/binary_tree_level_order_traversal.py` · BFS with a `deque`, one list per level
- [ ] [Lowest Common Ancestor](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) — `trees/lowest_common_ancestor_of_a_binary_tree.py` · post-order, bubble up finds
- [ ] [Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) — `trees/serialize_and_deserialize_binary_tree.py` · pre-order with null markers *(hard)*

## 4. Graphs  (`graphs/`)
Core idea: BFS/DFS over an adjacency list; watch a `visited` set. Topological sort for dependencies.

- [ ] [Clone Graph](https://leetcode.com/problems/clone-graph/) — `graphs/clone_graph.py` · DFS/BFS + `old→new` map
- [ ] [Course Schedule](https://leetcode.com/problems/course-schedule/) — `graphs/course_schedule.py` · cycle detection / topological sort (Kahn's)
- [ ] [Number of Islands](https://leetcode.com/problems/number-of-islands/) — `graphs/number_of_islands.py` · flood fill each unvisited land cell
- [ ] [Word Ladder](https://leetcode.com/problems/word-ladder/) — `graphs/word_ladder.py` · BFS for shortest path over word graph *(hard)*

## 5. Trie  (`trie/`)
Core idea: a tree of characters; each node has children + an end-of-word flag. Prefix ops in O(len).

- [ ] [Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/) — `trie/implement_trie_prefix_tree.py` · nested dict / node with children
- [ ] [Word Search II](https://leetcode.com/problems/word-search-ii/) — `trie/word_search_ii.py` · build a trie of words, then DFS the board *(hard)*

## 6. Design  (`design/`)
Core idea: pick data structures to hit the required complexity. Both below are **O(1)** — hash map + linked structure.

- [x] [LRU Cache](https://leetcode.com/problems/lru-cache/) — `design/lru_cache.py` 🎬 · dict + doubly linked list (also a production variant with TTL/stats)
- [x] [LFU Cache](https://leetcode.com/problems/lfu-cache/) — `design/lfu_cache.py` · dict + freq→bucket map + `min_freq` pointer

## 7. Concurrency  (`concurrency/`) — *not started*
Suggested topics: `threading.Lock`/`RLock`, producer–consumer with `queue.Queue`,
thread pools (`concurrent.futures`), `asyncio` basics, the GIL and when threads
help (I/O) vs. hurt (CPU). *(See the thread-safe cache in `design/lru_cache.py`.)*

## 8. System Design  (`system_design/`) — *not started*
Suggested topics: notes on caching, rate limiting, consistent hashing, load
balancing, queues, and how a distributed LRU/LFU differs from the in-process one.

---

## Visual aids & experiments  (`experiments/`)
Run these to build intuition:

- `python experiments/lru_cache_visualization.py` — animated LRU (hash map + DLL) 🎬
- `python experiments/doubly_linked_list_animation.py` — the DLL that powers LRU 🎬
- `python experiments/pi_simulation.py` — Monte Carlo vs. Leibniz π estimation

## Suggested order
1. **Arrays & HashMap** → **Sliding Window** (build the hashing/two-pointer muscle)
2. **Trees** → **Graphs** (recursion → BFS/DFS → topological sort)
3. **Trie** (specialized tree)
4. **Design** (LRU/LFU — already done; revisit to re-derive from scratch)
5. **Concurrency** → **System Design**

## Progress
Problems solved: **1 / 17**  ·  Design: **2 / 2**
_(update this line as you go)_
