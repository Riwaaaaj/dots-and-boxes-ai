from dots_and_boxes import Board, EdgeOrientation, Move


def main() -> None:
    b = Board(rows=3, cols=3)

    print(b)
    print("Horizontal edges:", len(b.horizontal_edges))
    print("Vertical edges:", len(b.vertical_edges))

    move = Move(EdgeOrientation.HORIZONTAL, 0, 0)
    completed = b.apply_move(move)

    print("Applied:", move)
    print("Boxes completed:", completed)
    print("State vector length:", len(b.state_vector()))


if __name__ == "__main__":
    main()
