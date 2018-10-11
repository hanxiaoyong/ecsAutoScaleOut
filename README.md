# manual
## what is it used for
It is a Python 2 code, used for collect how many ECS tasks can be put in the remain spaces in the current ECS cluster. 

## knowledge needed
Know the basic knowledge of the following service: ECS, Lambda, Cloudwatch(Include Cloudwatch event, self defined metric, and Alarm), Auto Scaling Group

## operation steps
1. define your own namespace and metric name that will be created in cloudwatch. and replace the current value of nameSpace and metricName in the .py file.
2. use your ECS cluster name and ECS task definition name to replace the current value of clusterName and taskDefinition in the .py file.
3. create a lambda function which use python 2.7. And use cloudwatch scheduled event as the triger.
4. use the .py file as the lambda code. 
5. the lambda will run periodicly and the remain space for task will be sent to the cloudwathc metric you defined in step 1.  e.g. If the current space can only put 3 tasks, the code will send 3 to the metric.
6. create an alarm to the cloudwatch metric, e.g. you can define that when the metric is less than 3, then the alarm is triggered.
7. redefine the AuoScaling policy of the container instance auto scaling group in EC2 console, e.g. you can modify the trigger alarm for scaling out as the alarm defined in step 6.

