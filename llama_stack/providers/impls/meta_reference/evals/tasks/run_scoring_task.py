# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.
from llama_stack.distribution.registry.datasets import DatasetRegistry
from llama_stack.distribution.registry.scorers import ScorerRegistry

from llama_stack.providers.impls.meta_reference.evals.scorer.aggregate_scorer import *  # noqa: F403
from llama_stack.providers.impls.meta_reference.evals.scorer.basic_scorers import *  # noqa: F403

from llama_stack.apis.evals import *  # noqa: F403
from llama_stack.apis.inference import *  # noqa: F403
from termcolor import cprint


class RunScoringTask(BaseTask):
    """
    RunScoringTask - only run scoring (F3) based on dataset and scoring config
    """

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

    def transform_score_input_sample(
        self, dataset: BaseDataset
    ) -> List[ScorerInputSample]:
        scorer_inputs = []
        for x in dataset:
            expected_answer = x.data["expected_answer"]
            generated_answer = x.data["generated_answer"]

            scorer_inputs.append(
                ScorerInputSample(
                    expected_answer=expected_answer,
                    generated_answer=generated_answer,
                )
            )

        return scorer_inputs

    async def run(
        self,
        dataset_config: EvaluateDatasetConfig,
        eval_scoring_config: EvaluateScoringConfig,
        *args,
        **kwargs,
    ) -> EvalResult:
        print(
            f"Running scoring task w/ dataset={dataset_config} scoring={eval_scoring_config}"
        )

        dataset = DatasetRegistry.get(dataset_config.dataset_identifier)
        dataset.load(n_samples=dataset_config.row_limit)
        print(f"Running on {len(dataset)} samples")

        # transform dataset into
        postprocessed = self.transform_score_input_sample(dataset)
        cprint(postprocessed, "blue")

        # F3 - scorer
        scorer_config_list = eval_scoring_config.scorer_config_list
        scorer_list = []
        for s_conf in scorer_config_list:
            scorer = ScorerRegistry.get(s_conf.scorer_name)
            scorer_list.append(scorer())

        scorer = AggregateScorer(
            scorers=scorer_list,
        )

        scorer_results = scorer.score(postprocessed)
        cprint(scorer_results, "magenta")
        eval_result = scorer.aggregate_results(scorer_results)

        return eval_result