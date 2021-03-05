import numpy as np
from scipy.sparse import csr_matrix

class Concatenator:

    def __init__(self, filling_value=10.):
        self.filling_value = filling_value

    def concat(self, include_layer:np.ndarray, exclude_layer:np.ndarray):
        if (isinstance(include_layer, csr_matrix)):
            include_layer = include_layer.todense()

        # 점수를 0~1점으로 표준화
        include_layer = self._normalize(include_layer)
        include_layer = self._flip(include_layer)

        # 제외할 부분은 np.inf로 처리
        exclude_layer = self._mask_exclusion(exclude_layer)

        # 두 레이어를 병합
        return self._merge(include_layer, exclude_layer)

    def _normalize(self, layer: np.ndarray):
        return layer / layer.max()

    def _flip(self, layer:np.ndarray):
        return 1 - layer

    def _mask_exclusion(self, layer:np.ndarray):
        layer = layer.astype(np.float)
        layer[layer > 0.] = np.inf
        return layer

    def _merge(self, include_layer:np.ndarray, exclude_layer:np.ndarray):
        exclude_layer[include_layer < 1] = 0
        merged_layer = (include_layer + exclude_layer)
        merged_layer[merged_layer == 1.] = self.filling_value
        return merged_layer