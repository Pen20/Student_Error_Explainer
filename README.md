# Student_Error_Explainer

1. Create a virtual environment

```
conda create -n explainer python=3.10 -y
```

2. Install dependencies

```
pip install -r requirements.txt
```

3. Run streamlit app

```
streamlit run app.py
```

# Deploying an OpenAI Streamlit Python app on AWS EC2

1. Go EC2 and launch the instance
2. Give the name like "StudentExplainer"
3. Stay with Amazon linux 2023 AMI (free tier eligible)
4. Instance type: stay with t2.micro (free tier eligible)
5. create a new key pair (e.g explainer)
6. In Network settings, click Edit and configure:
   a. Click on add security group rule
   b. for Type info: Custom TCP, we range port should be 8501
   c. Select for source type: Anywhere
   d. Then click on launch instance
   e. After success click on hyper link to go to EC2 instance

7. Click on InstanceID and then on connect twice
8. On terminal we run:
   a. sudo su
   b. yum update
   c. yum install git
   d. clone the repo using git clone https link
   e. ls, cd Student_Error_Explainer
   f. run:
   `yum install pip
python3 -m pip install --ignore-installed streamlit
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py`
9. To make the brower never be stoped go back to the user root (ec2-user) and run the following command

```
ls
cd Student_Error_explainer
nohup python3 -m streamlit run app.py
```

NB: To modify a file, visit the directory and tape nano <filename>

10. If you want to stop that service we need to connect up to root main and tap 'ps aux' or 'ps -ef' like

```
[ec2-user@ip-172-31-22-171 ~]$ ps aux
[ec2-user@ip-172-31-22-171 ~]$ ps -ef
``
11. Go to root user and tap 'kill <PID>'
```

[ec2-user@ip-172-31-22-171 ~]$ sudo su
[ec2-user@ip-172-31-22-171 ec2-user]$ kill <PID>
``
