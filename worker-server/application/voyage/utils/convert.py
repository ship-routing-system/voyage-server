from scipy.sparse import csr_matrix


def sparse2dict(matrix: csr_matrix):
    """ csr_matrix을 dictionary format으로 변환
    """
    coo = matrix.tocoo()
    return dict(
        data=coo.data.tolist(),
        row=coo.row.tolist(),
        col=coo.col.tolist(),
        shape=coo.shape
    )


def dict2sparse(data: dict):
    """ dictionary format을 csr_matrix으로 변환
    """
    return csr_matrix((data['data'], (data['row'], data['col'])), shape=data['shape'])
