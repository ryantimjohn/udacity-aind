import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on BIC scores

        best_score, best_model = float("inf"), None
        for n_components in range(self.min_n_components, self.max_n_components + 1):
            try:
                model = self.base_model(n_components)
                logL = model.score(self.X, self.lengths)
                p = n_components * (n_components - 1) + 2 * self.X.shape[1] * n_components
                logN = np.log(self.X.shape[0])
                BIC = -2 * logL + p * logN
                if BIC < best_score:
                    best_score, best_model = BIC, model
            except Exception as e:
                continue
        if best_model:
            return best_model
        return self.base_model(self.n_constant)


class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    https://pdfs.semanticscholar.org/ed3d/7c4a5f607201f3848d4c02dd9ba17c791fc2.pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on DIC scores
        best_score, best_model = float("-inf"), None
        for n_components in range(self.min_n_components, self.max_n_components + 1):
            try:
                log_P_X_i = self.base_model(n_components).score(self.X, self.lengths)
                sum = 0.0
                words = list(self.words.keys())
                M = len(words)
                for word in words:
                    try:
                        model_selector = ModelSelector(self.words, self.hwords,
                            word, self.n_constant, self.min_n_components,
                            self.max_n_components, self.random_state, self.verbose)
                        sum += model_selector.base_model(n_components).score(
                            model_selector.X, model_selector.lengths)
                    except Exception as e:
                        M = M - 1
                DIC = log_P_X_i - sum/(M-1)
                if DIC > best_score:
                    best_score, best_model = DIC, n_components
            except Exception as e:
                continue
        if best_model:
            return self.base_model(best_model)
        return self.base_model(self.n_constant)


class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    """
    Inherit:
    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None
    """

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection using CV
        splits = 3
        best_score, best_model = float("-inf"), None
        for n_components in range(self.min_n_components, self.max_n_components + 1):
            scores = []
            model, logL = None, None
            if(len(self.sequences) < splits):
                break
            split_method = KFold(random_state=self.random_state, n_splits=splits)
            for cv_train_loc, cv_test_loc in split_method.split(self.sequences):
                X_train, lengths_train = combine_sequences(cv_train_loc, self.sequences)
                X_test, lengths_test = combine_sequences(cv_test_loc, self.sequences)
                model = GaussianHMM(n_components=n_components, n_iter=1000,
                                    random_state=self.random_state).fit(X_train, lengths_train)
                logL = model.score(X_test, lengths_test)
                scores.append(logL)
            if len(scores) > 0:
                average = np.average(scores)
                if average > best_score:
                    best_score, best_model = average, model

        if best_model:
            return best_model
        return self.base_model(self.n_constant)
