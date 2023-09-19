# StreamTools

This was originally a Java app that I rewrote in Python. The original Java app was written in like 5 minutes and was a simple program to grab a random file based on a macro from touch portal. This version is one part me practicing with Python, one part upgrading the original, one part getting back into development, and one part "it seemed like a fun project to do".

StreamTools is a set of API commands intended to be usable mostly out-of-the-box but offer more power to those interested in using just the API.

Eventually connecting to multiple storage mediums is the endgoal- allowing users to access clips stored in cloud storage bucket like B2, S3, or MinIO; local filesystem storage; network storage like CIFS or NFS; and services like OneDrive or Google Drive. The ultimate endgame is something that can be hosted in the cloud, pointing to files stored in the cloud.