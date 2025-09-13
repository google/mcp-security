# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import markdown
import datetime
from google.cloud import storage
from google.genai import types
from google.adk.tools.tool_context import ToolContext
import os
import logging

async def store_file(tool_context:ToolContext,**kwargs)->dict:
   """
   Stores the file on the disk and adds it to the artifactservice

   Input:

   Following arguments should come in **kwargs
   markdown_text
   file_name
   
   Returns:
   json response with 
   result - success / failure
   message - message

   """
   html_output = markdown.markdown(kwargs["markdown_text"], extensions=['extra'])
   file_name=kwargs["file_name"]
   html_file_name=file_name+".html"
   # write to the disk and then save into the artifact service
   # writing to disk is totally optional
   with open(f"{os.environ.get('LOCAL_DIR_FOR_FILES','/tmp')}/{file_name}.html", "w", encoding="utf-8") as f:
        f.write(html_output)

   file_artifact = types.Part.from_bytes( # from_text is available but does not work with GCS.
        data=html_output.encode('utf-8'),
        mime_type="text/html" # https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/MIME_types/Common_types
    )
   filename = html_file_name
   version = await tool_context.save_artifact(filename=f"user:{filename}", artifact=file_artifact) 
   print(f"Successfully saved file artifact '{filename}' as version {version}.")
   return{
      "result":"success",
      "message":f"file {file_name} written to file {html_file_name}"
   } 

async def list_files(tool_context:ToolContext,**kwargs)->dict:
   """
   list files available to the user

   Input:
   None 
   
   Returns:
   json response with 
   result - success / error
   message - message
   file_list - list of files

   """
   # list_artifacts actually returns list of keys which are generally file names
   artifacts = await tool_context.list_artifacts()
   return{
      "result":"success",
      "message":f"Fetched the files successfully",
      "file_list": artifacts
   }


# We could have used the same tool context and kwargs as inputs here
# but this should also work based on the prompt and the docstring.
def get_file_link(user_name:str,file_name:str)->dict:
    """Provides link to download the file

   Inputs:
   user_name
   file_name
        
   Returns:
   json response with 
   result - success / error
   message - message
   links - a list of jsons with keys are file_name, file_version and file_link
    """

    if os.environ.get("ARTIFACT_SERVICE","in_memory") != "gcs":
        return {
            "result":"error",
            "message":f"Download link provided only for GCS backed artifacts",
            "links": ""
        }
    # https://stackoverflow.com/questions/46540894/blob-generate-signed-url-failing-to-attributeerror
    if os.environ.get("GCS_SA_JSON","not_provided") == "not_provided":
        return {
            "result":"error",
            "message":f"Need SA JSON, Please check https://cloud.google.com/storage/docs/access-control/signing-urls-with-helpers",
            "links": ""
        }

    # make sure that the file name has user scope and html extension
    # as we always add files to artifact registry in user scope 
    # and with an html extension.
    
    if not file_name.startswith("user:"):
        file_name = "user:" + file_name
    if not file_name.endswith(".html"):
        file_name = file_name + ".html"        

    try:
        storage_client = storage.Client.from_service_account_json(os.environ.get("GCS_SA_JSON"))
        bucket_name = os.environ.get("GCS_ARTIFACT_SERVICE_BUCKET")
        ultimate_directory = f"{os.environ.get('APP_NAME')}/{user_name}/user/{file_name}"
        # GCS stores files as versions (not GCS versions but file named 0,1,2,3 within the ultimate folder)
        blobs = storage_client.list_blobs(bucket_name, prefix=ultimate_directory)

        signed_urls=[]
        print(f"Listing files in bucket '{bucket_name}' (with prefix '{ultimate_directory}' if specified):")
        for blob in blobs:
            logging.info(f"Start - Generating URL for {bucket_name}/{blob.name}")
            # Get the bucket and blob (object)
            # blob name already has everything except the bucket name in its path
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_name=f"{blob.name}")
            file_version = blob.name.split("/")[-1]
            # Generate the signed URL
            # For a v4 signed URL, you must specify the expiration as a datetime object.
            # url valid for 10 minutes
            expiration_seconds=int(os.environ.get("SIGNED_URL_DURATION_MIN",10)) * 60
            expiration_time = datetime.timedelta(seconds=expiration_seconds)
            signed_url = blob.generate_signed_url(
                version="v4",
                expiration=expiration_time,
                method="GET"  # Use "GET" for downloading, "PUT" for uploading
            )
            signed_urls.append({"file_name":file_name,"file_version":file_version,"file_link":signed_url})  
            logging.info(f"Done - Generating URL for {bucket_name}/{blob.name}")      

        return {
            "result":"success",
            "message":f"Link created successfully",
            "links": signed_urls
        }

    except Exception as e:
        print(f"An error occurred: {e}")
        return {
            "result":"error",
            "message":f"Error occured during link generation",
            "link": ""
        }
