# squid-report

## adding a new rule (checklist)

1. add a new unit-test module for your rule in `tests/rules/`
1. (optional: add positive and negative log files)
1. add a new module in `squidreport/rules`
1. subclass BaseRule and make sure it has a unique `code` property
1. import your new rule in `squidreport/rules/__init__.py`
1. add your new rule in `ALL_RULES`
