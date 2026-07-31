# Question Bank

144 problems across 15 patterns, split into three tiers.

| Tier | Meaning | Count |
| --- | --- | --- |
| **Tier 1** | Must prepare — the core set. Do these first, then re-derive them cold. | 60 |
| **Tier 2** | Good to prepare — common follow-ups and the next-most-asked variants. | 56 |
| **Tier 3** | Prepare if you have time — hard or niche; skip until Tiers 1-2 are solid. | 28 |

Every file is a stub with the problem statement, a worked example, and runnable
self-checks. Solve the function, then run the file — it prints `ok` when the
assertions pass and raises `NotImplementedError` until you start.

```bash
python arrays/tier1/two_sum.py          # a single question
python -m compileall -q . -x '\.venv'   # syntax-check everything
```

Each file's docstring carries its own `Run:` line, so you never have to guess
the path.

## Suggested order

Work **Tier 1 across every pattern first** — breadth beats depth for interview
coverage, and the patterns reinforce each other. Only then go back for Tier 2.

| Pattern | Folder | Problems |
| --- | --- | --- |
| Arrays & Hashing | `arrays/` | 16 |
| Two Pointers | `two_pointers/` | 8 |
| Sliding Window | `sliding_window/` | 7 |
| Stack | `stack/` | 9 |
| Binary Search | `binary_search/` | 9 |
| Linked List | `linked_list/` | 10 |
| Trees | `trees/` | 15 |
| Tries | `trie/` | 3 |
| Heap / Priority Queue | `heap/` | 6 |
| Backtracking | `backtracking/` | 9 |
| Graphs | `graphs/` | 14 |
| Dynamic Programming | `dynamic_programming/` | 16 |
| Intervals | `intervals/` | 6 |
| Greedy | `greedy/` | 6 |
| Math & Bit Manipulation | `math_bits/` | 10 |

---

## Arrays & Hashing

**Tier 1 — must prepare**

- [ ] [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) — `arrays/tier1/contains_duplicate.py`
- [ ] [Encode and Decode Strings](https://leetcode.com/problems/encode-and-decode-strings/) — `arrays/tier1/encode_and_decode_strings.py`
- [x] [Group Anagrams](https://leetcode.com/problems/group-anagrams/) — `arrays/tier1/group_anagrams.py`
- [ ] [Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) — `arrays/tier1/longest_consecutive_sequence.py`
- [ ] [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) — `arrays/tier1/product_of_array_except_self.py`
- [ ] [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) — `arrays/tier1/top_k_frequent_elements.py`
- [x] [Two Sum](https://leetcode.com/problems/two-sum/) — `arrays/tier1/two_sum.py`
- [ ] [Valid Anagram](https://leetcode.com/problems/valid-anagram/) — `arrays/tier1/valid_anagram.py`

**Tier 2 — good to prepare**

- [ ] [Majority Element](https://leetcode.com/problems/majority-element/) — `arrays/tier2/majority_element.py`
- [ ] [Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/) — `arrays/tier2/merge_sorted_array.py`
- [ ] [Sort Colors](https://leetcode.com/problems/sort-colors/) — `arrays/tier2/sort_colors.py`
- [ ] [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) — `arrays/tier2/subarray_sum_equals_k.py`
- [ ] [Valid Sudoku](https://leetcode.com/problems/valid-sudoku/) — `arrays/tier2/valid_sudoku.py`

**Tier 3 — prepare if you have time**

- [ ] [First Missing Positive](https://leetcode.com/problems/first-missing-positive/) — `arrays/tier3/first_missing_positive.py`
- [ ] [Insert Delete GetRandom O(1)](https://leetcode.com/problems/insert-delete-getrandom-o1/) — `arrays/tier3/insert_delete_getrandom_o1.py`
- [ ] [Longest String Chain](https://leetcode.com/problems/longest-string-chain/) — `arrays/tier3/longest_string_chain.py`

## Two Pointers

**Tier 1 — must prepare**

- [ ] [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) — `two_pointers/tier1/container_with_most_water.py`
- [ ] [3Sum](https://leetcode.com/problems/3sum/) — `two_pointers/tier1/three_sum.py`
- [ ] [Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) — `two_pointers/tier1/two_sum_ii_sorted.py`
- [ ] [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) — `two_pointers/tier1/valid_palindrome.py`

**Tier 2 — good to prepare**

- [ ] [Move Zeroes](https://leetcode.com/problems/move-zeroes/) — `two_pointers/tier2/move_zeroes.py`
- [ ] [Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) — `two_pointers/tier2/remove_duplicates_from_sorted_array.py`
- [ ] [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) — `two_pointers/tier2/trapping_rain_water.py`

**Tier 3 — prepare if you have time**

- [ ] [4Sum](https://leetcode.com/problems/4sum/) — `two_pointers/tier3/four_sum.py`

## Sliding Window

**Tier 1 — must prepare**

- [ ] [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) — `sliding_window/tier1/best_time_to_buy_and_sell_stock.py`
- [ ] [Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) — `sliding_window/tier1/longest_repeating_character_replacement.py`
- [ ] [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) — `sliding_window/tier1/longest_substring_without_repeating_characters.py`
- [ ] [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) — `sliding_window/tier1/minimum_window_substring.py`

**Tier 2 — good to prepare**

- [ ] [Permutation in String](https://leetcode.com/problems/permutation-in-string/) — `sliding_window/tier2/permutation_in_string.py`
- [ ] [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) — `sliding_window/tier2/sliding_window_maximum.py`

**Tier 3 — prepare if you have time**

- [ ] [Substring with Concatenation of All Words](https://leetcode.com/problems/substring-with-concatenation-of-all-words/) — `sliding_window/tier3/substring_with_concatenation_of_all_words.py`

## Stack

**Tier 1 — must prepare**

- [ ] [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) — `stack/tier1/daily_temperatures.py`
- [ ] [Min Stack](https://leetcode.com/problems/min-stack/) — `stack/tier1/min_stack.py`
- [ ] [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) — `stack/tier1/valid_parentheses.py`

**Tier 2 — good to prepare**

- [ ] [Car Fleet](https://leetcode.com/problems/car-fleet/) — `stack/tier2/car_fleet.py`
- [ ] [Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/) — `stack/tier2/evaluate_reverse_polish_notation.py`
- [ ] [Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) — `stack/tier2/generate_parentheses.py`
- [ ] [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) — `stack/tier2/largest_rectangle_in_histogram.py`

**Tier 3 — prepare if you have time**

- [ ] [Asteroid Collision](https://leetcode.com/problems/asteroid-collision/) — `stack/tier3/asteroid_collision.py`
- [ ] [Decode String](https://leetcode.com/problems/decode-string/) — `stack/tier3/decode_string.py`

## Binary Search

**Tier 1 — must prepare**

- [ ] [Binary Search](https://leetcode.com/problems/binary-search/) — `binary_search/tier1/binary_search.py`
- [ ] [Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) — `binary_search/tier1/find_minimum_in_rotated_sorted_array.py`
- [ ] [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) — `binary_search/tier1/koko_eating_bananas.py`
- [ ] [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) — `binary_search/tier1/search_in_rotated_sorted_array.py`

**Tier 2 — good to prepare**

- [ ] [Find First and Last Position of Element](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) — `binary_search/tier2/find_first_and_last_position.py`
- [ ] [Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/) — `binary_search/tier2/search_a_2d_matrix.py`
- [ ] [Time Based Key-Value Store](https://leetcode.com/problems/time-based-key-value-store/) — `binary_search/tier2/time_based_key_value_store.py`

**Tier 3 — prepare if you have time**

- [ ] [Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/) — `binary_search/tier3/median_of_two_sorted_arrays.py`
- [ ] [Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/) — `binary_search/tier3/split_array_largest_sum.py`

## Linked List

**Tier 1 — must prepare**

- [ ] [Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) — `linked_list/tier1/linked_list_cycle.py`
- [ ] [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) — `linked_list/tier1/merge_two_sorted_lists.py`
- [ ] [Remove Nth Node From End of List](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) — `linked_list/tier1/remove_nth_node_from_end.py`
- [ ] [Reorder List](https://leetcode.com/problems/reorder-list/) — `linked_list/tier1/reorder_list.py`
- [ ] [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) — `linked_list/tier1/reverse_linked_list.py`

**Tier 2 — good to prepare**

- [ ] [Add Two Numbers](https://leetcode.com/problems/add-two-numbers/) — `linked_list/tier2/add_two_numbers.py`
- [ ] [Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/) — `linked_list/tier2/copy_list_with_random_pointer.py`
- [ ] [Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) — `linked_list/tier2/merge_k_sorted_lists.py`

**Tier 3 — prepare if you have time**

- [ ] [Find the Duplicate Number](https://leetcode.com/problems/find-the-duplicate-number/) — `linked_list/tier3/find_the_duplicate_number.py`
- [ ] [Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/) — `linked_list/tier3/reverse_nodes_in_k_group.py`

## Trees

**Tier 1 — must prepare**

- [ ] [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) — `trees/tier1/binary_tree_level_order_traversal.py`
- [ ] [Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) — `trees/tier1/invert_binary_tree.py`
- [ ] [Lowest Common Ancestor of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) — `trees/tier1/lowest_common_ancestor_of_a_binary_tree.py`
- [ ] [Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/) — `trees/tier1/maximum_depth_of_binary_tree.py`
- [ ] [Same Tree](https://leetcode.com/problems/same-tree/) — `trees/tier1/same_tree.py`
- [ ] [Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) — `trees/tier1/validate_binary_search_tree.py`

**Tier 2 — good to prepare**

- [ ] [Balanced Binary Tree](https://leetcode.com/problems/balanced-binary-tree/) — `trees/tier2/balanced_binary_tree.py`
- [ ] [Binary Tree Right Side View](https://leetcode.com/problems/binary-tree-right-side-view/) — `trees/tier2/binary_tree_right_side_view.py`
- [ ] [Construct Binary Tree from Preorder and Inorder Traversal](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) — `trees/tier2/construct_binary_tree_from_preorder_and_inorder.py`
- [ ] [Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/) — `trees/tier2/diameter_of_binary_tree.py`
- [ ] [Kth Smallest Element in a BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) — `trees/tier2/kth_smallest_element_in_a_bst.py`
- [ ] [Subtree of Another Tree](https://leetcode.com/problems/subtree-of-another-tree/) — `trees/tier2/subtree_of_another_tree.py`

**Tier 3 — prepare if you have time**

- [ ] [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) — `trees/tier3/binary_tree_maximum_path_sum.py`
- [ ] [Count Good Nodes in Binary Tree](https://leetcode.com/problems/count-good-nodes-in-binary-tree/) — `trees/tier3/count_good_nodes_in_binary_tree.py`
- [ ] [Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) — `trees/tier3/serialize_and_deserialize_binary_tree.py`

## Tries

**Tier 1 — must prepare**

- [ ] [Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/) — `trie/tier1/implement_trie_prefix_tree.py`

**Tier 2 — good to prepare**

- [ ] [Design Add and Search Words Data Structure](https://leetcode.com/problems/design-add-and-search-words-data-structure/) — `trie/tier2/design_add_and_search_words.py`

**Tier 3 — prepare if you have time**

- [ ] [Word Search II](https://leetcode.com/problems/word-search-ii/) — `trie/tier3/word_search_ii.py`

## Heap / Priority Queue

**Tier 1 — must prepare**

- [ ] [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) — `heap/tier1/find_median_from_data_stream.py`
- [ ] [Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) — `heap/tier1/kth_largest_element_in_an_array.py`

**Tier 2 — good to prepare**

- [ ] [K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) — `heap/tier2/k_closest_points_to_origin.py`
- [ ] [Last Stone Weight](https://leetcode.com/problems/last-stone-weight/) — `heap/tier2/last_stone_weight.py`
- [ ] [Task Scheduler](https://leetcode.com/problems/task-scheduler/) — `heap/tier2/task_scheduler.py`

**Tier 3 — prepare if you have time**

- [ ] [Design Twitter](https://leetcode.com/problems/design-twitter/) — `heap/tier3/design_twitter.py`

## Backtracking

**Tier 1 — must prepare**

- [ ] [Combination Sum](https://leetcode.com/problems/combination-sum/) — `backtracking/tier1/combination_sum.py`
- [ ] [Permutations](https://leetcode.com/problems/permutations/) — `backtracking/tier1/permutations.py`
- [ ] [Subsets](https://leetcode.com/problems/subsets/) — `backtracking/tier1/subsets.py`
- [ ] [Word Search](https://leetcode.com/problems/word-search/) — `backtracking/tier1/word_search.py`

**Tier 2 — good to prepare**

- [ ] [Combination Sum II](https://leetcode.com/problems/combination-sum-ii/) — `backtracking/tier2/combination_sum_ii.py`
- [ ] [Letter Combinations of a Phone Number](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) — `backtracking/tier2/letter_combinations_of_a_phone_number.py`
- [ ] [Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/) — `backtracking/tier2/palindrome_partitioning.py`
- [ ] [Subsets II](https://leetcode.com/problems/subsets-ii/) — `backtracking/tier2/subsets_ii.py`

**Tier 3 — prepare if you have time**

- [ ] [N-Queens](https://leetcode.com/problems/n-queens/) — `backtracking/tier3/n_queens.py`

## Graphs

**Tier 1 — must prepare**

- [ ] [Clone Graph](https://leetcode.com/problems/clone-graph/) — `graphs/tier1/clone_graph.py`
- [ ] [Course Schedule](https://leetcode.com/problems/course-schedule/) — `graphs/tier1/course_schedule.py`
- [ ] [Number of Islands](https://leetcode.com/problems/number-of-islands/) — `graphs/tier1/number_of_islands.py`
- [ ] [Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow/) — `graphs/tier1/pacific_atlantic_water_flow.py`

**Tier 2 — good to prepare**

- [ ] [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) — `graphs/tier2/course_schedule_ii.py`
- [ ] [Graph Valid Tree](https://leetcode.com/problems/graph-valid-tree/) — `graphs/tier2/graph_valid_tree.py`
- [ ] [Number of Connected Components](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/) — `graphs/tier2/number_of_connected_components.py`
- [ ] [Redundant Connection](https://leetcode.com/problems/redundant-connection/) — `graphs/tier2/redundant_connection.py`
- [ ] [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) — `graphs/tier2/rotting_oranges.py`
- [ ] [Surrounded Regions](https://leetcode.com/problems/surrounded-regions/) — `graphs/tier2/surrounded_regions.py`

**Tier 3 — prepare if you have time**

- [ ] [Alien Dictionary](https://leetcode.com/problems/alien-dictionary/) — `graphs/tier3/alien_dictionary.py`
- [ ] [Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/) — `graphs/tier3/cheapest_flights_within_k_stops.py`
- [ ] [Network Delay Time](https://leetcode.com/problems/network-delay-time/) — `graphs/tier3/network_delay_time.py`
- [ ] [Word Ladder](https://leetcode.com/problems/word-ladder/) — `graphs/tier3/word_ladder.py`

## Dynamic Programming

**Tier 1 — must prepare**

- [ ] [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) — `dynamic_programming/tier1/climbing_stairs.py`
- [ ] [Coin Change](https://leetcode.com/problems/coin-change/) — `dynamic_programming/tier1/coin_change.py`
- [ ] [House Robber](https://leetcode.com/problems/house-robber/) — `dynamic_programming/tier1/house_robber.py`
- [ ] [Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) — `dynamic_programming/tier1/longest_common_subsequence.py`
- [ ] [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) — `dynamic_programming/tier1/longest_increasing_subsequence.py`
- [ ] [Word Break](https://leetcode.com/problems/word-break/) — `dynamic_programming/tier1/word_break.py`

**Tier 2 — good to prepare**

- [ ] [Decode Ways](https://leetcode.com/problems/decode-ways/) — `dynamic_programming/tier2/decode_ways.py`
- [ ] [House Robber II](https://leetcode.com/problems/house-robber-ii/) — `dynamic_programming/tier2/house_robber_ii.py`
- [ ] [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) — `dynamic_programming/tier2/longest_palindromic_substring.py`
- [ ] [Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/) — `dynamic_programming/tier2/maximum_product_subarray.py`
- [ ] [Palindromic Substrings](https://leetcode.com/problems/palindromic-substrings/) — `dynamic_programming/tier2/palindromic_substrings.py`
- [ ] [Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) — `dynamic_programming/tier2/partition_equal_subset_sum.py`
- [ ] [Unique Paths](https://leetcode.com/problems/unique-paths/) — `dynamic_programming/tier2/unique_paths.py`

**Tier 3 — prepare if you have time**

- [ ] [Burst Balloons](https://leetcode.com/problems/burst-balloons/) — `dynamic_programming/tier3/burst_balloons.py`
- [ ] [Edit Distance](https://leetcode.com/problems/edit-distance/) — `dynamic_programming/tier3/edit_distance.py`
- [ ] [Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/) — `dynamic_programming/tier3/regular_expression_matching.py`

## Intervals

**Tier 1 — must prepare**

- [ ] [Insert Interval](https://leetcode.com/problems/insert-interval/) — `intervals/tier1/insert_interval.py`
- [ ] [Merge Intervals](https://leetcode.com/problems/merge-intervals/) — `intervals/tier1/merge_intervals.py`
- [ ] [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) — `intervals/tier1/non_overlapping_intervals.py`

**Tier 2 — good to prepare**

- [ ] [Meeting Rooms](https://leetcode.com/problems/meeting-rooms/) — `intervals/tier2/meeting_rooms.py`
- [ ] [Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/) — `intervals/tier2/meeting_rooms_ii.py`

**Tier 3 — prepare if you have time**

- [ ] [Minimum Interval to Include Each Query](https://leetcode.com/problems/minimum-interval-to-include-each-query/) — `intervals/tier3/minimum_interval_to_include_each_query.py`

## Greedy

**Tier 1 — must prepare**

- [ ] [Jump Game](https://leetcode.com/problems/jump-game/) — `greedy/tier1/jump_game.py`
- [ ] [Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) — `greedy/tier1/maximum_subarray.py`

**Tier 2 — good to prepare**

- [ ] [Gas Station](https://leetcode.com/problems/gas-station/) — `greedy/tier2/gas_station.py`
- [ ] [Hand of Straights](https://leetcode.com/problems/hand-of-straights/) — `greedy/tier2/hand_of_straights.py`
- [ ] [Jump Game II](https://leetcode.com/problems/jump-game-ii/) — `greedy/tier2/jump_game_ii.py`

**Tier 3 — prepare if you have time**

- [ ] [Partition Labels](https://leetcode.com/problems/partition-labels/) — `greedy/tier3/partition_labels.py`

## Math & Bit Manipulation

**Tier 1 — must prepare**

- [ ] [Counting Bits](https://leetcode.com/problems/counting-bits/) — `math_bits/tier1/counting_bits.py`
- [ ] [Missing Number](https://leetcode.com/problems/missing-number/) — `math_bits/tier1/missing_number.py`
- [ ] [Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/) — `math_bits/tier1/number_of_1_bits.py`
- [ ] [Reverse Bits](https://leetcode.com/problems/reverse-bits/) — `math_bits/tier1/reverse_bits.py`

**Tier 2 — good to prepare**

- [ ] [Rotate Image](https://leetcode.com/problems/rotate-image/) — `math_bits/tier2/rotate_image.py`
- [ ] [Set Matrix Zeroes](https://leetcode.com/problems/set-matrix-zeroes/) — `math_bits/tier2/set_matrix_zeroes.py`
- [ ] [Spiral Matrix](https://leetcode.com/problems/spiral-matrix/) — `math_bits/tier2/spiral_matrix.py`
- [ ] [Sum of Two Integers](https://leetcode.com/problems/sum-of-two-integers/) — `math_bits/tier2/sum_of_two_integers.py`

**Tier 3 — prepare if you have time**

- [ ] [Happy Number](https://leetcode.com/problems/happy-number/) — `math_bits/tier3/happy_number.py`
- [ ] [Pow(x, n)](https://leetcode.com/problems/powx-n/) — `math_bits/tier3/pow_x_n.py`
