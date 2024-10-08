# RAG-TO-AWS
thank you original source code from https://github.com/pixegami/deploy-rag-to-aws . we can see detail at https://www.youtube.com/watch?v=ldFONBo2CR0

![alt text](https://github.com/CakeNuthep/RAG-TO-AWS/blob/main/document/image/FlowArchitect.png)

## Require
 - create new channel on Line Developers console
 - create AWS account
 - python 3.10.5
 - cdk 2.154.1
 - aws-cli/2.7.7
 - docker 27.1.1

### Configure AWS
You need to have an AWS account, and AWS CLI set up on your machine. You'll also need to have Bedrock enabled on AWS (and granted model access to Claude or whatever you want to use).

## Steps
### Update .env File with AWS Credentials
update credentials in a file named `image/.env`. Do NOT commit the file to .git. The file should have content like this:

```
AWS_ACCESS_KEY_ID=XXXXX
AWS_SECRET_ACCESS_KEY=XXXXX
AWS_DEFAULT_REGION=us-east-1
```

### Update line_model.py with Line Token
update `CHANNEL_SECRET` and `CHANNEL_ACCESS_TOKEN` in `image/src/line_model.py`.  Do NOT commit the file to .git. The file should have content like this:
```python
class LineModel():
    def __init__(self):
        self.CHANNEL_SECRET="XXXXX"
        self.CHANNEL_ACCESS_TOKEN="XXXXX"
```


### Installing Requirements

```sh
pip install -r image/requirements.txt
```

### Building the Vector DB
Put all the PDF source files you want into `image/src/data/source/` . Then go image and run:

```sh
# Use "--reset" if you want to overwrite an existing DB.
python populate_database.py --reset
```

### Deploy to AWS
I have put all the AWS CDK files into `rag-cdk-infra/`. Go into the folder and install the Node dependencies.
```sh
npm install
```

Then run this command to deploy it (assuming you have AWS CLI already set up, and AWS CDK already bootstrapped). I recommend deploying to `us-east-1` to start with (since all the AI models are there).
```sh
cdk deploy
```
# Result
![alt text](https://github.com/CakeNuthep/RAG-TO-AWS/blob/main/document/image/Result.jpg)

# Refference
- Origin source code: https://github.com/pixegami/deploy-rag-to-aws
- Rag video: https://www.youtube.com/watch?v=ldFONBo2CR0
