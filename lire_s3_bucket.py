import boto3
def list_buckets():
  # Retrieve the list of existing buckets
  s3 = boto3.client('s3')
  response = s3.list_buckets()

  # Output the bucket names
  print('Existing buckets:')
  for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')
  
def lire_objet_s3(bucket_name,object_name):
  ''' lire un objet depuis un bucket S3 '''
  s3=boto3.client("s3")
  response = s3.get_object(Bucket=bucket_name,Key=object_name)
  content = response["Body"].read()
  return (content) # renvoi le contenu binaire de l'objet lu

list_buckets()