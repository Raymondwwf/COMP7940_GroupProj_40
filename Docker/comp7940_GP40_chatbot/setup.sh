set -e
  
echo 'loading'
export GOOGLE_APPLICATION_CREDENTIALS=secert.json
python3 app/main.py