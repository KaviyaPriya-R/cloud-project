Outsourcing data to a third-party administrative control, as is done in cloud 
computing, gives rise to security concerns. The data compromise may occur due to attacks by other 
users and nodes within the cloud. Therefore, high security measures are required to protect data within 
the cloud. However, the employed security strategy must also take into account the optimization of 
the data retrieval time. 
 
 In this project, we propose division and replication of data in the cloud for optimal 
performance and security (DROPS) that collectively approaches the security and performance issues. 
In the DROPS (division and replication of data in cloud for optimal performance and security)
methodology, we divide a file into fragments, and replicate the fragmented data over the cloud nodes. 
Each of the nodes stores only a single fragment of a particular data file that ensures that even in case 
of a successful attack, no meaningful information is revealed to the attacker. Moreover, the nodes 
storing the fragments are separated with certain distance by means of graph T-coloring to prohibit an 
attacker of guessing the locations of the fragments. Furthermore, the DROPS methodology does not 
rely on the traditional cryptographic techniques for the data security; thereby relieving the system of 
computationally expensive methodologies. 
 
 We show that the probability to locate and compromise all of the nodes storing the 
fragments of a single file is extremely low. We also compare the performance of the DROPS 
methodology with 10 other schemes. The higher level of security with slight performance overhead 
was observe.

Modules:
  **Admin --** 
    view user,
    view user upload file list in encrpt form. 
  **User --**
    new user,
    upload file,
    view received file with private key
