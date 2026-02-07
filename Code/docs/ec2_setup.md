# AWS EC2 Provisioning & Setup Guide

This guide details the steps to manually provision an EC2 instance and prepare it for hosting the AI Summarizer application.

## 1. Provision EC2 Instance

1.  **Login to AWS Console** and navigate to **EC2**.
2.  **Launch Instance**:
    - **Name**: `ai-summarizer-prod`
    - **OS Image**: Ubuntu Server 22.04 LTS (HVM), SSD Volume Type.
    - **Instance Type**: `t2.micro` (free tier) or `t3.small` (recommended for ML models).
    - **Key Pair**: Create a new key pair (e.g., `ai-summarizer-key.pem`) and download it.
3.  **Network Settings**:
    - Allow SSH traffic from your IP (or Anywhere `0.0.0.0/0` for testing).
    - Allow HTTP traffic from the internet.
    - **Security Group**: Create a new one.
        - Add Rule: Type `Custom TCP`, Port `8000` (Backend), Source `0.0.0.0/0`.
        - Add Rule: Type `Custom TCP`, Port `8501` (Frontend), Source `0.0.0.0/0`.
4.  **Storage**: 8 GB (default) is likely enough, but 20 GB is safer for Docker images.
5.  **Launch Instance**.

## 2. Connect to Instance

Open your terminal (PowerShell or Git Bash):

```bash
# Set permissions for key (Linux/Mac/Git Bash)
chmod 400 "path/to/ai-summarizer-key.pem"

# Connect
ssh -i "path/to/ai-summarizer-key.pem" ubuntu@<EC2_PUBLIC_IP>
```

## 3. Install Docker & Docker Compose

Run the following commands on the EC2 instance:

```bash
# Update packages
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg

# Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Set up the repository
echo \
  "deb [arch=\"$(dpkg --print-architecture)\" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  \"$(. /etc/os-release && echo "$VERSION_CODENAME")\" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add ubuntu user to docker group (so you don't need sudo)
sudo usermod -aG docker param
# NOTE: Log out and log back in for this to take effect!
exit
```

## 4. Install AWS CLI (Optional but recommended for CloudWatch)

```bash
sudo apt-get install -y unzip
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

## 5. Configure CloudWatch Permissions

1.  Go to AWS IAM.
2.  Create a Role for EC2 with `CloudWatchAgentServerPolicy` or `CloudWatchLogsFullAccess`.
3.  Attach this IAM Role to your EC2 instance (Actions -> Security -> Modify IAM Role).

## 6. AWS Secrets Manager Setup (Optional but Recommended)

Instead of a `.env` file, you can store secrets in AWS.

1.  Go to **Secrets Manager**.
2.  **Store a new secret** -> "Other type of secret".
3.  Key/Values:
    - `POSTGRES_USER`: ...
    - `POSTGRES_PASSWORD`: ...
    - `POSTGRES_DB`: ...
    - `DOCKER_USERNAME`: ...
    - `DOCKER_PASSWORD`: ...
4.  Secret Name: `prod/ai-summarizer/env`
5.  Update your IAM Role to allow `secretsmanager:GetSecretValue` for this secret.

Now your server is ready for deployment!
