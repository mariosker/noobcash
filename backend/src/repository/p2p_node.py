import pickle

import requests
from config import config
from src.repository.node import _Node
from src.repository.ring import Ring, RingNode


class P2PNode(_Node):

    def __init__(self) -> None:
        super().__init__()
        self.node_info = self._get_node_info_from_bootstrap()

    def _get_node_info_from_bootstrap(self) -> RingNode:
        """ As a client request from Bootstrap to return the proper NodeInfo with updated ID

        Raises:
            ConnectionRefusedError: Request denied
        """

        tmp_node_info = RingNode(id=-1,
                                 host=config.HOST,
                                 port=config.PORT,
                                 utxos=self.wallet.unspent_transactions,
                                 public_key=self.wallet.public_key)

        ring_node_serial = pickle.dumps(tmp_node_info)

        resp = requests.post(config.BOOTSTRAP_HOST + ':' +
                             config.BOOTSTRAP_PORT + config.NODE_REGISTER_URL,
                             data=ring_node_serial)

        if resp.status_code != 200:
            raise ConnectionRefusedError("Cannot get uid from bootstrap")
        resp_content = pickle.loads(resp.content)
        return resp_content

    def set_ring(self, ring: Ring) -> None:
        self.ring = ring
