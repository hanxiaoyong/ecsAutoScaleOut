import boto3

#cluster name and task definition
clusterName = 'testCluster'
taskDefinition = 'hello-world'

#cloudwatch metic name space and metric name
nameSpace = 'testNameSpace'
metricName = 'testName'

ecsClient = boto3.client('ecs')
cwClient = boto3.client('cloudwatch')

def getContainerInstances(clusterName):
    listContainerInstancesResponse = ecsClient.list_container_instances(
                    cluster=clusterName
                    )
    instances=listContainerInstancesResponse['containerInstanceArns']
    return instances


def getTaskContainers(taskDefinition):
    return ecsClient.describe_task_definition(
                    taskDefinition=taskDefinition
                    )['taskDefinition']['containerDefinitions']
                    
def getTaskCPU(taskDefinition):
    cpu = 0
    containers = getTaskContainers(taskDefinition)
    for i in range(len(containers)):
        cpu = cpu + containers[i]['cpu']
    return cpu
    
def getTaskCPUr(taskDefinition):
    return int(ecsClient.describe_task_definition(
                    taskDefinition=taskDefinition
                    )['taskDefinition']['cpu'])
 
def getTaskMem(taskDefinition):
    mem = 0
    containers = getTaskContainers(taskDefinition)
    for i in range(len(containers)):
        mem = mem + containers[i]['memory']
    return mem
    
'''
def getTaskMem(tastDefinition):
    mem = 0
    containers = getTaskContainers(taskDefinition)
    for i in range(len(containers)):
        mem = mem + containers[i]['memoryReservation']
    return mem
'''
    
def getTaskMemr(tastDefinition):
    return int(ecsClient.describe_task_definition(
                    taskDefinition=taskDefinition
                    )['taskDefinition']['memory'])


def getContainerInstanceRemainResource(clusterName, containerInstance):

    response = ecsClient.describe_container_instances(
                cluster=clusterName,
                containerInstances=[containerInstance]
                )['containerInstances'][0]['remainingResources']
    return response
    
def getContainerInstanceRemainTask(clusterName, containerInstance, taskDefinition):
    remainResource = getContainerInstanceRemainResource(clusterName,containerInstance)
    remainCPU = remainResource[0]['integerValue']
    remainMem = remainResource[1]['integerValue']
    neededCPU = getTaskCPUr(taskDefinition)
    neededMem = getTaskMemr(taskDefinition)
    
    c = remainCPU//neededCPU
    m = remainMem//neededMem

    return min(c,m)
 
 
def getClusterRemainTast(clusterName, taskDefinition):
    t = 0
    instances = getContainerInstances(clusterName)
    for i in range(len(instances)):
        r = getContainerInstanceRemainTask(clusterName, instances[i], taskDefinition)
        print('>>>>>>>in instance, ' + str(i) + ' there can add ' + str(r) + ' tasts')
        t = t + r
    return t 
    
    

def lambda_handler(event, context):
    clusterRemainTask = getClusterRemainTast(clusterName, taskDefinition)
    cwClient.put_metric_data(
        Namespace=nameSpace,
        MetricData=[
                    {
                        'MetricName': metricName,
                        'Value': clusterRemainTask,
    
                    }
                   ]
        )
    
    print (">>>>>>>One task requires cpu amount:" + str(getTaskCPUr(taskDefinition)))
    print (">>>>>>>One tast requires mem amount:" + str(getTaskMemr(taskDefinition)))
    print (">>>>>>>the num of container instances is:" + str(len(getContainerInstances(clusterName))))
    print ('>>>>>>>in the cluster,  there can add: ' + str((clusterRemainTask)) + 'tasks')
    print (">>>>>>> these are the container instances:")
    print (getContainerInstances(clusterName))

