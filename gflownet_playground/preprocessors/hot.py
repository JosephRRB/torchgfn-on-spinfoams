from gflownet_playground.preprocessors.base import Preprocessor
from torch.nn.functional import one_hot
import torch
from einops import rearrange


class OneHotPreprocessor(Preprocessor):
    "Use One Hot Preprocessing for environment with enumerable states"
    @property
    def output_dim(self):
        return self.env.n_states

    def preprocess(self, states):
        state_indices = self.env.get_states_indices(states)
        return one_hot(state_indices, self.output_dim).float()


class KHotPreprocessor(Preprocessor):
    "Use K Hot Preprocessing for environment with enumerable states with a grid structure"
    @property
    def output_dim(self):
        output_dim = (self.env.n_states ** (1 / self.env.ndim)) * self.env.ndim
        print(output_dim)
        assert output_dim.is_integer(), "The environment does not support K Hot preprocessing"
        return int(output_dim)

    def preprocess(self, states):
        hot = one_hot(states.states, int(
            self.output_dim / self.env.ndim)).float()
        hot = rearrange(hot, '... a b -> ... (a b)')
        return hot
