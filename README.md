# PreferredItemService
1. [Setup](#setup-instructions)
2. [Solution Implementation ](#solution-implementation)
3. [Architecture](#architecture)
4. [API schema](#api-schema)
5. [Future improvements](#future-improvements)

---
## Setup Instructions

Instructions for running api locally:

```bash
git clone {repo url}

#create a virtual env. 
pyhon3 -m venv .venv
cd preferred_item_service

#install requiremets
pip install -r requirements.txt

# run api 
uvicorn preferred_item_service.api.main:app --host 0.0.0.0 --port 80   
```
CDK instrcutions:
[cdk](infra_cdk/README.md)

Running tests:
```bash
pytest
```
Docker instructions:

```bash
docker build -t preferred_item_api .
docker run -p 8000:80 preferred_item_api:latest    
```

## Solution 
 The solution has been implemented using FAST API and Mangum, utilizing the serverless architecture with services such as API Gateway, Lambda, and authorization. Additionally, a Docker file has been included, which can be deployed on serverless platforms such as EKS and ECS. The implementation defines a FastAPI instance for a Preferred Item Service, which includes three routers from three different endpoint files, each with their respective prefixes and tags. 
 
 ### Usage
 - navigate to http://127.0.0.1:80/docs#/
 - ![instruction]("https://github.com/santhosh-aws/Assignment/blob/main/usage.gif")

## Architecture
### DataModel
- ![DataModel](https://github.com/santhosh-aws/Assignment/blob/main/brick.drawio.png)
### AWS Auth Flow
- ![aws](https://github.com/santhosh-aws/Assignment/blob/main/custom-auth-workflow.png)

### Service Flow
graph TD;
    A[Client]-->B[Uvicorn Server];
    D[Preferred Item Domain Service];
    B[Uvicorn Server]-->P;
    MD[Master Data Service]-->P;
    I[Item Service]-->P;
    D-->P[APPRouter];
    P-->D;

## Possible improvements
- Implement a score-based approach for determining the preferred item, considering the weight of price and status.
- Employ caching mechanisms such as Redis or Memcached to speed up data retrieval and reduce server load.
- Implement rate limiting to restrict the number of requests made to the service within a given period of time, preventing server overload.
- Implement an authorization framework such as Cognito or Open ID to enhance system security.
- Based on traffic patterns, choose the appropriate service model. For continuous traffic, services like EKS or EC2 Architecture may be suitable, while for unpredictable use, serverless models like ECS with Fargate or API Gateway with Lambda may be appropriate.
