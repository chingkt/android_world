TASK_NAME=SystemBluetoothTurnOnVerify

for i in {1..1}; do
python -u run.py \
  --suite_family=android_world \
  --agent_name=t3a_gemini_gcp \
  --n_task_combinations=3 \
  --tasks=$TASK_NAME \
| tee -a ${TASK_NAME}.txt
  sleep 5
  done

