from collections import defaultdict

from urh.awre.components.Component import Component

class Synchronization(Component):
    """
    Finding the synchronzation works by finding the first difference between two blocks.
    This is performed for all blocks and the most frequent first difference is chosen
    """


    def __init__(self, priority=1, predecessors=None, enabled=True, backend=None):
        super().__init__(priority, predecessors, enabled, backend)

    def _py_find_field(self, bitvectors, column_ranges, rows):
        possible_sync_pos = defaultdict(int)


        for i in range(0, len(rows)):
            bitvector_i = bitvectors[rows[i]]
            for j in range(i, len(rows)):
                bitvector_j = bitvectors[rows[j]]
                for col_range in column_ranges[i]:
                    start, end = col_range
                    bits_i = bitvector_i[start:end]
                    bits_j = bitvector_j[start:end]
                    try:
                        first_diff = next(k for k, (bit_i, bit_j) in enumerate(zip(bits_i, bits_j)) if bit_i != bit_j)
                    except StopIteration:
                        continue
                    start = 4 * (start // 4)
                    first_diff = start + 4 * (first_diff // 4) - 1
                    if start != first_diff:
                        possible_sync_pos[(start, first_diff)] += 1

        sync_interval = max(possible_sync_pos, key=possible_sync_pos.__getitem__)
        return sync_interval