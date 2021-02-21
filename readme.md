# Restless Recurring Multi-Armed Bandit

## Introduction

This work explores  is a code base used to validate work for non-statioinary multi-armed bandit research.

## References

Gupta, N., Granmo, O. C., & Agrawala, A. (2011, December). Thompson sampling for dynamic multi-armed bandits. In 2011 10th International Conference on Machine Learning and Applications and Workshops (Vol. 1, pp. 484-489). IEEE.

Raj, V., & Kalyani, S. (2017). Taming non-stationary bandits: A Bayesian approach. arXiv preprint arXiv:1707.09727.

## ToDo

- Implement RExp3Policy
- Implement table with overall payout / regret by policy and machine
- Validate
  - DiscountedThompsonSamplingPolicy
  - DiscountedOptimisticThompsonSamplingPolicy
  - DynamicThompsonSamplingPolicy
  - GreedyPolicy
  - RandomPolicy
  - RecurringMemoryThompsonSamplingPolicy
  - REXP3Policy
  - ThompsonSamplingPolicy
  - UCBPolicy
- Implement non-cyclical machine
- Comment history file
- Comment MachineManager
