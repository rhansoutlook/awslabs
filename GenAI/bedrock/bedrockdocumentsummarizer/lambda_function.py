import json
import boto3
import os
import io
import logging

# --- Libraries ---
from pypdf import PdfReader
import docx
from odf.opendocument import load
from odf.text import P
from odf import teletype

# --- Setup Logging ---
log_level_str = os.environ.get('LOG_LEVEL', 'INFO').upper()
logger = logging.getLogger()
level = getattr(logging, log_level_str, logging.INFO)
logger.setLevel(level)

# --- Initialize Clients ---
s3_client = boto3.client('s3')
bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')

# --- Helper Functions (Text Extraction) ---

def extract_text_from_pdf(file_content):
    pdf_reader = PdfReader(io.BytesIO(file_content))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file_content):
    doc = docx.Document(io.BytesIO(file_content))
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_text_from_odt(file_content):
    f = io.BytesIO(file_content)
    textdoc = load(f)
    allparas = textdoc.getElementsByType(P)
    return "\n".join([teletype.extractText(p) for p in allparas])

# --- Core Logic (Process One File) ---

def process_single_file(file_name, bucket_name, source_folder, dest_folder, model_id, max_chars):
    """
    Returns a success message string or raises an exception.
    """
    logger.info(f"--- Processing: {file_name} ---")
    
    # 1. Download
    source_key = f"{source_folder}{file_name}"
    logger.debug(f"Downloading {source_key}...")
    response = s3_client.get_object(Bucket=bucket_name, Key=source_key)
    file_content = response['Body'].read()
    
    # 2. Extract Text
    file_ext = os.path.splitext(file_name)[1].lower()
    extracted_text = ""
    
    if file_ext == '.pdf':
        extracted_text = extract_text_from_pdf(file_content)
    elif file_ext == '.docx':
        extracted_text = extract_text_from_docx(file_content)
    elif file_ext == '.txt':
        extracted_text = file_content.decode('utf-8')
    elif file_ext == '.odt': 
         extracted_text = extract_text_from_odt(file_content)
    else:
        raise ValueError(f"Unsupported file type: {file_ext}")
    
    input_text = extracted_text[:max_chars]

    # 3. Call Bedrock
    payload = {
        "messages": [
            {
                "role": "user",
                "content": [{"text": f"Please summarize the following document:\n\n{input_text}"}]
            }
        ],
        "inferenceConfig": {
            "max_new_tokens": 1000
        }
    }
    
    logger.debug(f"Invoking Model for {file_name}...")
    response = bedrock_client.invoke_model(
        modelId=model_id,
        body=json.dumps(payload)
    )
    
    response_body = json.loads(response['body'].read())
    summary = response_body['output']['message']['content'][0]['text']
    
    # 4. Upload Summary (Fixed naming bug here)
    base_name = os.path.splitext(file_name)[0]  # Remove extension (e.g. 'report')
    summary_key = f"{dest_folder}{base_name}.summary.txt" # Result: 'summaries/report.txt'
    s3_client.put_object(
        Bucket=bucket_name,
        Key=summary_key,
        Body=summary
    )
    
    return f"Saved to {summary_key}"

# --- Main Handler (Batch Loop) ---

def lambda_handler(event, context):
    logger.info("Batch Job started.")
    
    # Load Config
    bucket_name = os.environ.get('BUCKET_NAME')
    source_folder = os.environ.get('SOURCE_PREFIX', 'documents/')
    dest_folder = os.environ.get('DEST_PREFIX', 'summaries/')
    model_id = os.environ.get('MODEL_ID')
    max_chars = int(os.environ.get('MAX_CHARS', '5000'))
    
    # Get List of Files
    # Expecting: {"files": ["a.pdf", "b.docx"]}
    files_to_process = event.get('files', [])
    
    if not files_to_process:
        return {"statusCode": 400, "body": "No files provided in 'files' list."}

    results = []

    # Loop through the list
    for file_name in files_to_process:
        try:
            status = process_single_file(file_name, bucket_name, source_folder, dest_folder, model_id, max_chars)
            results.append({"file": file_name, "status": "Success", "details": status})
            logger.info(f"Success: {file_name}")
        except Exception as e:
            # Log error but continue loop
            error_msg = str(e)
            results.append({"file": file_name, "status": "Error", "details": error_msg})
            logger.error(f"Failed: {file_name} - {error_msg}")

    # Return summary report
    return {
        "statusCode": 200,
        "body": json.dumps(results)
    }