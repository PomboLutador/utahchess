converter = {
    "Pawn": {"black": "Chess_pdt60.png", "white": "Chess_plt60.png"},
    "Knight": {"black": "Chess_ndt60.png", "white": "Chess_nlt60.png"},
    "Rook": {"black": "Chess_rdt60.png", "white": "Chess_rlt60.png"},
    "Bishop": {"black": "Chess_bdt60.png", "white": "Chess_blt60.png"},
    "Queen": {"black": "Chess_qdt60.png", "white": "Chess_qlt60.png"},
    "King": {"black": "Chess_kdt60.png", "white": "Chess_klt60.png"},
}


def piece_to_assetname(piece):
    piece_type = piece.piece_type
    piece_color = piece.color
    return converter[piece_type][piece_color]
