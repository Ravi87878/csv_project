# csv_api_app/views.py
import base64
from io import StringIO
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from .utils import get_work_dir,create_csv_file_in_dir
from csv_file_uploader.serializers import CSVUploadSerializer
from .models import CSVFile
from .serializers import CSVFileSerializer
from rest_framework.response import Response
from rest_framework import status

from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'page_size'
    max_page_size = 1000  
class CSVQueryView(APIView):

    def post(self,request):
        try:
            csv_file = request.FILES['file']
            file_name = csv_file.name
            dirs=get_work_dir()
            create_csv_file_in_dir(name=file_name,content=csv_file,dirs=dirs)
            data={}
            data['file_name']=file_name
            data['file_path']=dirs
            csv_serializer=CSVFileSerializer(data=data)
            if csv_serializer.is_valid():
                csv_serializer.save()
                return Response({"status":"csv stored succesffully"},status=status.HTTP_201_CREATED)
            else:
                return Response({"status":csv_serializer.errors},status=status.HTTP_400_BAD_REQUEST)
           
        except Exception as e:
            print(e)
            return Response({"status":"There some issue please upload in 2 or 3 minutes later"},status.HTTP_400_BAD_REQUEST)
        
        
    def get(self, request,pk):
        try:
            csv_object=CSVFile.objects.get(pk=pk)
        except CSVFile.DoesNotExist as e:
            print(e)
        try:
            chunk_size = 1000
            chunks = []
            for chunk in pd.read_csv(csv_object.file_path+"/"+csv_object.file_name, chunksize=chunk_size):
                chunks.append(chunk)
            # df = pd.read_csv(csv_object.file_path+"/"+csv_object.file_name)
            df = pd.concat(chunks, ignore_index=True)

        except FileNotFoundError:
            return Response({"error": "CSV file not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # records = df.to_dict(orient='records')

        query_params = request.query_params
        filtered_records = []
        mask = pd.Series(True, index=df.index)
        for param, value in query_params.items():
            if param in df.columns:
                if value.startswith('>') or value.startswith('<'):
                    # Handle greater than and less than searches
                    operator = value[0]
                    numeric_value = float(value[1:])
                    if operator == '>':
                        mask &= (df[param] > numeric_value)
                    elif operator == '<':
                        mask &= (df[param] < numeric_value)
                elif pd.api.types.is_numeric_dtype(df[param]):
                    # Handle numeric comparisons (e.g., total > 100)
                    mask &= (df[param] == float(value))
                elif pd.api.types.is_datetime64_any_dtype(df[param]):
                    # Handle date comparisons (e.g., date > '2023-01-01')
                    try:
                        date_value = pd.to_datetime(value)
                        mask &= (df[param] > date_value)
                    except ValueError:
                        return Response({"error": f"Invalid date format for '{param}'"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # Handle string searches
                    mask &= df[param].str.lower().str.contains(value.lower())
        filtered_df = df[mask]
        aggregate_queries = request.query_params.getlist('aggregate')
        if aggregate_queries:
            aggregates = {}
            for aggregate_query in aggregate_queries:
                agg_param, agg_func = aggregate_query.split(':')
                if agg_func == 'max':
                    aggregates[f'{agg_param}_max'] = filtered_df[agg_param].max()
                elif agg_func == 'min':
                    aggregates[f'{agg_param}_min'] = filtered_df[agg_param].min()
                elif agg_func == 'mean':
                    aggregates[f'{agg_param}_mean'] = filtered_df[agg_param].mean()
                elif agg_func == 'sum':
                    aggregates[f'{agg_param}_sum'] = filtered_df[agg_param].sum()
            return Response(aggregates, status=status.HTTP_200_OK)
        # filtered_records = df[mask].to_dict(orient='records')
        # for record in records:
        #     match = True
        #     for param, value in query_params.items():
        #         if param in df.columns:
        #             if pd.api.types.is_numeric_dtype(df[param]):
        #                 if record[param] != float(value):
        #                     match = False
        #                     break
        #             else:
        #                 if value.lower() not in str(record[param]).lower():
        #                     match = False
        #                     break
        #     if match:
        #         filtered_records.append(record)

        paginator = CustomPagination()
        paginated_data = paginator.paginate_queryset(filtered_records.to_dict(orient='records'), request)
        return paginator.get_paginated_response(paginated_data)
