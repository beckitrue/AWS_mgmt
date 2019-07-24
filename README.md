# AWS_mgmt

=========

Repository for my scritpts to manage my AWS infrastructure. It's just a couple of Pyhon scripts I'm running in Lambda right now.  

I'm shutting down all spot instances and any on demand instances that don't have a Stage:prod tag. I trigger these with a CloudWatch schedule to run at the end of every day.

Requirements
------------    

Python 3.7 (that's what I'm using in Lambda - you could probably use an older version)

Site Variables
--------------
none

Dependencies
------------
AWS Lambda  
AWS IAM  (Role permissions. You'll need to be able to describe instances and tags and be able to terminate and stop instances)    
AWS CloudWatch (to trigger the Lambda functions on a schedule)  

Example
----------------
terminate the spot instances first: stopEC2Spot.py  
shut down the non-prod instances: stopEC2NonProd.py

License
-------

none

Author Information
------------------

Becki True
becki@beckitrue.com

