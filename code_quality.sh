#!/bin/bash
cq_result=$(radon cc --min D volmdlr)
echo $cq_result
if [[ "$cq_result" ]];
	then echo "Error in code quality check, run radon to simplify functions">&2;
fi;
