from utahchess import BLACK, WHITE

converter = {
    "Pawn": {BLACK: "Chess_pdt60.png", WHITE: "Chess_plt60.png"},
    "Knight": {BLACK: "Chess_ndt60.png", WHITE: "Chess_nlt60.png"},
    "Rook": {BLACK: "Chess_rdt60.png", WHITE: "Chess_rlt60.png"},
    "Bishop": {BLACK: "Chess_bdt60.png", WHITE: "Chess_blt60.png"},
    "Queen": {BLACK: "Chess_qdt60.png", WHITE: "Chess_qlt60.png"},
    "King": {BLACK: "Chess_kdt60.png", WHITE: "Chess_klt60.png"},
}


def piece_to_assetname(piece):
    piece_type = piece.piece_type
    piece_color = piece.color
    return converter[piece_type][piece_color]
