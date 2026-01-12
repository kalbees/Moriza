import requests
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

MAIN_URL = "https://api.open5e.com/"

class SearchView(APIView):
    # TODO: Implement multiple result respone support 
    
    def get(self, request, type, *args): 
        # Get query params
        search = request.query_params.get("search", None)

        # Handle blank searches
        if not search: 
            return Response({"error": "Missing search parameter"}, status = status.HTTP_400_BAD_REQUEST)
        
        # Call Open5e 
        try:
            response = requests.get(f"{MAIN_URL}{type}/", params = {"search": search})
            # If type doesn't exist
            if response.status_code == 404: 
                return Response({"error": "Search category does not exist"}, status = status.HTTP_404_NOT_FOUND) 
            
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            return Response({"error": "Open5e External API error"}, status = status.HTTP_502_BAD_GATEWAY)
        
        results = response.json().get("results")

        if results is None: 
            return Response({"error": f"{type} term \"{search}\" does not exist"}, status = status.HTTP_404_NOT_FOUND)
        
        # Return first result found 
        return Response(results[0], status = status.HTTP_200_OK)
        



