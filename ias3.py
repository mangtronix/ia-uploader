#!/opt/local/bin/python2.6

import boto

S3_HOST='s3.us.archive.org'

def uploadFile(access_key, secret_key, bucket_name, filename, s3filename = None, callback=None, num_callbacks = 10, do_derive = False):
    conn = boto.connect_s3(access_key, secret_key, is_secure=False, host=S3_HOST)
    bucket = boto.s3.bucket.Bucket(conn, name=bucket_name)
    print 'Uploading %s to S3 bucket %s' % (filename, bucket_name)
  
    headers = {}
    if not do_derive:
        headers['x-archive-queue-derive'] = '0'
        
    if not s3filename:
        s3filename = filename
        
    key = boto.s3.key.Key(bucket)
    key.key = s3filename # $$$ normalize
    key.set_contents_from_filename(filename, headers=headers, cb=callback, num_cb=num_callbacks)    

