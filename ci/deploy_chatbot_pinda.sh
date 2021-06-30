#!/bin/sh

# Aws credentials
export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID_PINDA
export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY_PINDA
export AWS_INSTANCE_STATE=running
export AWS_INSTANCE_NAME=chatbotPinda

echo " "
echo "Getting instance Id..."
echo "=================================================================================="
echo " "

instanceid=`aws ec2 describe-instances --region $AWS_REGION_PINDA --filters Name=tag:Name,Values=$AWS_INSTANCE_NAME Name=instance-state-name,Values=$AWS_INSTANCE_STATE --output text --query 'Reservations[*].Instances[*].InstanceId'`

echo " "
echo "Instance Id = " $instanceid
echo " "
echo "Terminating instance..."
echo "=================================================================================="
echo " "

aws ec2 terminate-instances --region $AWS_REGION_PINDA --instance-id $instanceid
echo " "
echo "Done!"
