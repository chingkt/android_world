TASK_NAME=SimpleSmsSendReceivedAddress

for i in {1..1}; do
python -u run.py \
  --suite_family=android_world \
  --agent_name=t3a_gemini_gcp \
  --n_task_combinations=10 \
  --tasks=$TASK_NAME \
| tee -a ${TASK_NAME}_after_refinement.txt
  sleep 5
  done

