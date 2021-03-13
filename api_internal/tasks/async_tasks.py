import settings
from dto.job import Job
from tasks.celeryapp import app


@app.task(name='process_data',
          autoretry_for=(Exception,),
          retry_backoff=60,
          retry_backoff_max=300,
          max_retries=5)
def process_data(job_id, job_type):
    job = Job(job_id, job_type)
    data_processor = settings.JOB_PROCESSORS[str(job_type)]()
    data_processor.process(job)
    print(f'Processed job with uid: {job_id}')
