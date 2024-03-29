class EmbeddingFabric:

    @staticmethod
    def strategy_initialization(matrix, unknown_vector, word_indexer, embedding_dict):
        for word, i in word_indexer.get_element_to_index_dict().items():
            vector = unknown_vector

            if word in embedding_dict.keys():
                vector = embedding_dict[word]
            elif word.lower() in embedding_dict.keys():
                vector = embedding_dict[word.lower()]

            matrix[i] = vector

        return matrix

    EMBEDDING_STRATEGIES = {
        "strategy": lambda matrix, unknown_vector, word_indexer, embedding_dict: EmbeddingFabric.strategy_initialization(matrix, unknown_vector, word_indexer, embedding_dict)
    }

    @staticmethod
    def get_embedding_layer(word_indexer, embedding_dict, strategy='strategy'):
        import numpy as np
        import torch
        import torch.nn as nn

        matrix_len = word_indexer.size()
        embedding_dim = next(iter(embedding_dict.values())).shape[0]
        weights_matrix = np.zeros((matrix_len, embedding_dim))

        unknown_vector = np.random.randn(100)

        weights_matrix = EmbeddingFabric.EMBEDDING_STRATEGIES[strategy](weights_matrix,
                                                                        unknown_vector,
                                                                        word_indexer,
                                                                        embedding_dict)

        embedding = nn.Embedding(matrix_len, embedding_dim)
        embedding.load_state_dict({'weight': torch.from_numpy(weights_matrix)})

        return embedding
