import settings
from dto.job import Job
from tasks.celeryapp import app


@app.task(name='process_data',
          autoretry_for=(Exception,),
          retry_backoff=10,
          retry_backoff_max=30,
          max_retries=2)
def process_data(job_id, job_type):
    job = Job(job_id, job_type)
    job_processor = settings.JOB_PROCESSORS[str(job.type)]()
    job_processor.process(job)
    print(f'Processed job with uid: {job_id}')
