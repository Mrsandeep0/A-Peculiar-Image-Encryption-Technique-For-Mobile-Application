import gzip
f_in = open('/home/joe/file.txt')
f_out = gzip.open('/home/joe/file.txt.gz', 'wb')
f_out.writelines(f_in)
f_out.close()
f_in.close()