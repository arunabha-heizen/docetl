FROM public.ecr.aws/lambda/python:3.11

# Install system dependencies if required by docling/docetl
# The AWS base image uses microdnf (Amazon Linux 2023) or yum (AL2)
RUN dnf update -y && dnf install -y mesa-libGL glib2 && dnf clean all

COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ${LAMBDA_TASK_ROOT}/app
COPY .env ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler
CMD [ "app.handler.lambda_handler" ]
