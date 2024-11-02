# account/tasks.py

import pandas as pd
from io import BytesIO
from celery import shared_task
from django.core.files import File
from django.db.models import F
from django.utils import timezone
from apps.dataset.models import Dataset, DatasetReport
from apps.text.models import Tag  

@shared_task
def generate_operator_performance_report():
    # Loop through each dataset to generate a report
    datasets = Dataset.active_objects.active()
    
    for dataset in datasets:
        # Fetch tag data for the current dataset using values()
        tags_data = (
            Tag.objects
            .filter(text__dataset=dataset)
            .select_related('user', 'text', 'category')
            .values(
                username=F('user__username'),
                text_pk=F('text__id'),
                text_content=F('text__content'),
                category_name=F('category__name'),
                created_at=F('created_time')
            )
        )
        if tags_data.exists():

            # Prepare data for the DataFrame directly from the queryset
            data = list(tags_data)  # Convert the QuerySet to a list of dictionaries

            # Create a DataFrame for the dataset
            df = pd.DataFrame(data)

            # Use BytesIO to save the DataFrame to a CSV file in memory
            csv_buffer = BytesIO()
            df.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)  # Move to the beginning of the buffer

            # Create a file name for the dataset report
            file_name = f"{dataset.name}_report_{timezone.now().date()}.csv"

            # Save the report file to the DatasetReport model
            dataset_report = DatasetReport(dataset=dataset)
            dataset_report.report_file.save(file_name, File(csv_buffer))

    return f"Reports generated for {datasets.count()} datasets"

