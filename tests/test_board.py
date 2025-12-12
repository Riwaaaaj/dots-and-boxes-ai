import unittest

from dots_and_boxes import Board, EdgeOrientation, Move


class TestBoard(unittest.TestCase):
    def test_edge_counts_3x3(self) -> None:
        b = Board(rows=3, cols=3)
        # (rows+1)*cols = 4*3 = 12
        # rows*(cols+1) = 3*4 = 12
        self.assertEqual(b.edge_count(), (12, 12))

    def test_legal_moves_initial(self) -> None:
        b = Board(rows=1, cols=1)
        # 1x1 box -> 2 horizontal + 2 vertical edges
        self.assertEqual(len(b.legal_moves()), 4)

    def test_complete_single_box(self) -> None:
        b = Board(rows=1, cols=1)

        # top, left, right should not complete a box
        self.assertEqual(b.apply_move(Move(EdgeOrientation.HORIZONTAL, 0, 0)), [])
        self.assertEqual(b.apply_move(Move(EdgeOrientation.VERTICAL, 0, 0)), [])
        self.assertEqual(b.apply_move(Move(EdgeOrientation.VERTICAL, 0, 1)), [])

        # bottom completes the only box (0,0)
        completed = b.apply_move(Move(EdgeOrientation.HORIZONTAL, 1, 0))
        self.assertEqual(completed, [(0, 0)])

    def test_state_vector_roundtrip(self) -> None:
        b = Board(rows=2, cols=2)
        b.apply_move(Move(EdgeOrientation.HORIZONTAL, 0, 0))
        b.apply_move(Move(EdgeOrientation.VERTICAL, 0, 0))

        vec = b.state_vector()
        b2 = Board.from_state_vector(2, 2, vec)

        self.assertEqual(b2.rows, 2)
        self.assertEqual(b2.cols, 2)
        self.assertEqual(b2.state_vector(), vec)


if __name__ == "__main__":
    unittest.main()
