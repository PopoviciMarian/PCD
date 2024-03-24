import os

COMPILER_SUB = 'projects/tidal-reactor-418113/subscriptions/compiler-sub'
CERT_PATH = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', "/usr/src/app/src/tidal-reactor-418113-86d7469fd70b.json")
BUCKET_NAME = 'binaries_solutions'
EXECUTOR_TOPIC = 'projects/tidal-reactor-418113/topics/executor'