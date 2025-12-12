from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Sequence, Tuple


class EdgeOrientation(str, Enum):
    HORIZONTAL = "H"
    VERTICAL = "V"


@dataclass(frozen=True, slots=True)
class Move:
    """A move is placing a single edge.

    Coordinate system is in *edge space*:
    - Horizontal edges: (r, c) where r in [0..rows], c in [0..cols-1]
    - Vertical edges:   (r, c) where r in [0..rows-1], c in [0..cols]
    """

    orientation: EdgeOrientation
    r: int
    c: int


class IllegalMove(ValueError):
    pass


class Board:
    """Dots and Boxes board state.

    The board is defined by a grid of `rows x cols` *boxes*.

    Storage:
    - horizontal_edges: length (rows + 1) * cols
    - vertical_edges:   length rows * (cols + 1)

    Each edge is stored as int 0/1 (empty/filled) to keep it ML-friendly.
    """

    def __init__(
        self,
        rows: int = 3,
        cols: int = 3,
        horizontal_edges: Sequence[int] | None = None,
        vertical_edges: Sequence[int] | None = None,
    ) -> None:
        if rows <= 0 or cols <= 0:
            raise ValueError("rows and cols must be positive")

        self.rows = int(rows)
        self.cols = int(cols)

        expected_h = (self.rows + 1) * self.cols
        expected_v = self.rows * (self.cols + 1)

        if horizontal_edges is None:
            self.horizontal_edges: List[int] = [0] * expected_h
        else:
            if len(horizontal_edges) != expected_h:
                raise ValueError(f"horizontal_edges must have length {expected_h}")
            self.horizontal_edges = [int(x) for x in horizontal_edges]

        if vertical_edges is None:
            self.vertical_edges: List[int] = [0] * expected_v
        else:
            if len(vertical_edges) != expected_v:
                raise ValueError(f"vertical_edges must have length {expected_v}")
            self.vertical_edges = [int(x) for x in vertical_edges]

    # ---------- indexing helpers ----------

    def _h_index(self, r: int, c: int) -> int:
        if not (0 <= r <= self.rows and 0 <= c < self.cols):
            raise IndexError("horizontal edge out of bounds")
        return r * self.cols + c

    def _v_index(self, r: int, c: int) -> int:
        if not (0 <= r < self.rows and 0 <= c <= self.cols):
            raise IndexError("vertical edge out of bounds")
        return r * (self.cols + 1) + c

    def edge_count(self) -> Tuple[int, int]:
        return (len(self.horizontal_edges), len(self.vertical_edges))

    def get_edge(self, move: Move) -> int:
        if move.orientation == EdgeOrientation.HORIZONTAL:
            return self.horizontal_edges[self._h_index(move.r, move.c)]
        if move.orientation == EdgeOrientation.VERTICAL:
            return self.vertical_edges[self._v_index(move.r, move.c)]
        raise ValueError(f"Unknown orientation: {move.orientation}")

    def is_legal(self, move: Move) -> bool:
        try:
            return self.get_edge(move) == 0
        except IndexError:
            return False

    def legal_moves(self) -> List[Move]:
        moves: List[Move] = []

        for r in range(self.rows + 1):
            for c in range(self.cols):
                if self.horizontal_edges[self._h_index(r, c)] == 0:
                    moves.append(Move(EdgeOrientation.HORIZONTAL, r, c))

        for r in range(self.rows):
            for c in range(self.cols + 1):
                if self.vertical_edges[self._v_index(r, c)] == 0:
                    moves.append(Move(EdgeOrientation.VERTICAL, r, c))

        return moves

    # ---------- box completion ----------

    def _box_is_complete(self, br: int, bc: int) -> bool:
        """Check if the box at (br, bc) has all 4 edges."""
        if not (0 <= br < self.rows and 0 <= bc < self.cols):
            raise IndexError("box out of bounds")

        top = self.horizontal_edges[self._h_index(br, bc)]
        bottom = self.horizontal_edges[self._h_index(br + 1, bc)]
        left = self.vertical_edges[self._v_index(br, bc)]
        right = self.vertical_edges[self._v_index(br, bc + 1)]
        return (top + bottom + left + right) == 4

    def boxes_completed_by_move(self, move: Move) -> List[Tuple[int, int]]:
        """Return list of box coordinates (br, bc) completed *after* applying this move.

        This assumes the edge has already been set.
        """
        candidates: List[Tuple[int, int]] = []

        if move.orientation == EdgeOrientation.HORIZONTAL:
            # affects box above (r-1, c) and below (r, c)
            if move.r - 1 >= 0:
                candidates.append((move.r - 1, move.c))
            if move.r < self.rows:
                candidates.append((move.r, move.c))
        else:
            # VERTICAL affects box left (r, c-1) and right (r, c)
            if move.c - 1 >= 0:
                candidates.append((move.r, move.c - 1))
            if move.c < self.cols:
                candidates.append((move.r, move.c))

        completed: List[Tuple[int, int]] = []
        for br, bc in candidates:
            if 0 <= br < self.rows and 0 <= bc < self.cols and self._box_is_complete(br, bc):
                completed.append((br, bc))

        return completed

    def apply_move(self, move: Move) -> List[Tuple[int, int]]:
        """Apply a move.

        Returns:
            List of box coordinates (br, bc) that became completed due to this move.

        Raises:
            IllegalMove: if move is out of bounds or edge already set.
        """
        if not self.is_legal(move):
            raise IllegalMove(f"Illegal move: {move}")

        if move.orientation == EdgeOrientation.HORIZONTAL:
            self.horizontal_edges[self._h_index(move.r, move.c)] = 1
        else:
            self.vertical_edges[self._v_index(move.r, move.c)] = 1

        return self.boxes_completed_by_move(move)

    # ---------- AI helpers ----------

    def state_vector(self) -> List[int]:
        """Concatenate edges into a single flat vector: [H..., V...]."""
        return [*self.horizontal_edges, *self.vertical_edges]

    @classmethod
    def from_state_vector(cls, rows: int, cols: int, vec: Sequence[int]) -> "Board":
        expected_h = (rows + 1) * cols
        expected_v = rows * (cols + 1)
        if len(vec) != expected_h + expected_v:
            raise ValueError(
                f"state vector must have length {expected_h + expected_v} for rows={rows}, cols={cols}"
            )
        h = vec[:expected_h]
        v = vec[expected_h:]
        return cls(rows=rows, cols=cols, horizontal_edges=h, vertical_edges=v)

    def copy(self) -> "Board":
        return Board(
            rows=self.rows,
            cols=self.cols,
            horizontal_edges=list(self.horizontal_edges),
            vertical_edges=list(self.vertical_edges),
        )

    def __repr__(self) -> str:
        return (
            f"Board(rows={self.rows}, cols={self.cols}, "
            f"horizontal_edges={sum(self.horizontal_edges)}/{len(self.horizontal_edges)}, "
            f"vertical_edges={sum(self.vertical_edges)}/{len(self.vertical_edges)})"
        )
