from src.repository.node import _Node
import pickle


class ChainUsecase:

    def __init__(self, node: _Node) -> None:
        self.node = node

    def get_chain(self):
        chain_and_id = {
            'blockchain': self.node.blockchain.get_chain(),
            'id': self.node.node_info.id
        }

        chain_and_id_pickled = pickle.dumps(chain_and_id)

        return chain_and_id_pickled
